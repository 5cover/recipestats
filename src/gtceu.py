from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterable, Mapping, Sequence
from functools import cache
from lines import Line
from valuedset import ValuedSet


class Oc(Enum):
    ULV = 0
    LV = 1
    MV = 2
    HV = 3
    EV = 4


TIER = Oc.LV


class Type(Enum):
    ITEM = 'Item'
    'units'
    FLUID = 'Fluid'
    'millibuckets (mb)'


class Machine(Enum):
    MACERATOR = 'Macerator'
    ORE_WASHER = 'Ore Washer'
    CHEMICAL_BATH = 'Chemical Bath'
    THERMAL_CENTRIFUGE = 'Thermal Centrifuge'
    CENTRIFUGE = 'Centrifuge'
    SMELTING = 'Smelting'
    FORGE_HAMMER = 'Forge Hammer'


@dataclass(frozen=True)
class Resource:
    type: Type
    name: str
    value: float

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Recipe:
    machine: Machine
    inputs: ValuedSet[Resource]
    outputs: ValuedSet[Resource]
    duration: float
    'seconds'
    energy: float
    'eu'
    times: float

    def __mul__(self, other: float):
        return Recipe(self.machine, self.inputs * other, self.outputs * other, self.duration * other, self.energy * other, other)

    def to_lines(self, index: int) -> Sequence[Line]:
        def flow_lines(flows: ValuedSet[Resource]):
            return (Line.fixed(f'{round(quantity, 3):g} {resource}') for resource, quantity in flows.items())

        return (Line.space_between(f'Recipe {index} ({self.times:g}x)', self.machine.value),
                *flow_lines(self.inputs),
                Line.fixed('\u21a7'),
                *flow_lines(self.outputs),
                Line.space_between(f'{self.energy:g}EU', f'{self.duration:g}s'))


def recipe(machine: Machine, inputs: Mapping[Resource, float],
           outputs: Mapping[Resource, float],
           duration: float, energy: float, start_oc: Oc | None = None):
    'start_oc: the OC after which efficiency increases'
    if start_oc is not None:
        mult = 2 ** (TIER.value - start_oc.value)
        energy *= mult
        duration /= mult
    return Recipe(machine, ValuedSet(inputs), ValuedSet(outputs), duration, energy, 1)


@dataclass(frozen=True)
class Chain:
    recipes: Sequence[Recipe]
    flows: ValuedSet[Resource]

    @property
    @cache
    def cost(self):
        return sum(r.value * -q for r, q in self.flows.items() if q < 0)

    @property
    @cache
    def value(self):
        return sum(r.value * q for r, q in self.flows.items() if q > 0)

    @property
    @cache
    def energy(self):
        return sum(r.energy for r in self.recipes)

    @property
    @cache
    def duration(self):
        return sum(r.duration for r in self.recipes)


def chain(recipes: Iterable[Recipe]):
    final_recipes: list[Recipe] = []

    flows = ValuedSet[Resource]()

    prev_recipe: Recipe | None = None
    for recipe in recipes:
        if prev_recipe:
            misflows = prev_recipe.outputs & recipe.inputs
            if len(misflows) != 0:
                r = misflows.single()[0]
                recipe *= (prev_recipe.outputs[r] / recipe.inputs[r])
        prev_recipe = recipe

        flows -= recipe.inputs
        flows += recipe.outputs

        final_recipes.append(recipe)

    return Chain(tuple(final_recipes), flows)
