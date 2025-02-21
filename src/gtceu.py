from dataclasses import dataclass
from enum import Enum
from collections.abc import Iterable, Mapping, Sequence
from functools import cache
from lines import Line
from valuedset import ValuedSet
import re


class Oc(Enum):
    """Energy tiers"""
    ULV = 0
    LV = 0
    MV = 1
    HV = 2
    EV = 3
    IV = 4
    LuV = 5
    ZPM = 6
    UV = 7
    UHV = 8
    UEV = 9
    UIV = 10
    UXV = 11
    OpV = 12
    MAX = 13


TIER = Oc.LV
# todo: tier chance bonues


class Type(Enum):
    ITEM = 'Item'
    'units'
    FLUID = 'Fluid'
    'millibuckets (mb)'


class Machine(Enum):
    CENTRIFUGE = 'Centrifuge'
    PACKER = 'Packer'
    CUTTER = 'Cutter'
    ELECTROLYZER = 'Electrolyzer'
    LATHE = 'Lathe'
    MACERATOR = 'Macerator'
    ORE_CRUSHING = 'Ore Crushing (~Forge Hammer)'
    ORE_GRINDING = 'Ore Grinding (~Macerator)'
    ORE_TREATING = 'Ore Treating (~Chemical Bath)'
    ORE_WASHER = 'Ore Washer'
    PART_GRINDING = 'Part Grinding'
    SIFTER = 'Sifter'
    SMELTING = 'Smelting'
    THERMAL_CENTRIFUGE = 'Thermal Centrifuge'
    IMPLOSION_COMPRESSOR = 'Implosion Compressor'


@dataclass(frozen=True)
class Resource:
    type: Type
    name: str
    value: float

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Recipe:
    id: int
    machine: Machine
    inputs: ValuedSet[Resource]
    outputs: ValuedSet[Resource]
    duration: float
    'seconds'
    energy: float
    'eu'
    circuit_config_no: int | None
    times: float

    def __mul__(self, times: float):
        return Recipe(
            self.id,
            self.machine,
            self.inputs * times,
            self.outputs * times,
            self.duration * times,
            self.energy * times,
            self.circuit_config_no,
            times,
        )

    def to_lines(self, index: int) -> Sequence[Line]:
        def flow_lines(flows: ValuedSet[Resource]):
            return (Line.fixed(f'{round(quantity, 3):g} {resource}') for resource, quantity in flows.items())

        return (Line.space_between(f'{index}. {self.times:g}x Recipe {self.id}', self.machine.value + ('' if self.circuit_config_no is None else f', config {self.circuit_config_no}')),
                *flow_lines(self.inputs),
                Line.fixed('\u21a7'),
                *flow_lines(self.outputs),
                Line.space_between(f'{self.energy:g}EU', f'{self.duration:g}s'))


_recipe_id = 0


def recipe(machine: Machine, inputs: Mapping[Resource, float],
           outputs: Mapping[Resource, float],
           duration: float, energy: float, circuit_config_no: int | None = None):
    if machine is not Machine.SMELTING:
        mult = 2 ** TIER.value
        energy = min(131072, energy * mult)
        duration = max(.05, duration / mult)
    global _recipe_id
    return Recipe(
        _recipe_id := _recipe_id + 1,
        machine,
        ValuedSet(inputs),
        ValuedSet(outputs),
        duration,
        energy,
        circuit_config_no,
        1,
    )


@dataclass(frozen=True)
class Chain:
    recipes: Sequence[Recipe]
    flows: ValuedSet[Resource]

    @property
    @cache
    def cost(self):
        return sum(rs.value * -qty for rs, qty in self.flows.items() if qty < 0)

    @property
    @cache
    def value(self):
        return sum(rs.value * qty for rs, qty in self.flows.items() if qty > 0)

    @property
    @cache
    def energy(self):
        return sum(r.energy for r in self.recipes)

    @property
    @cache
    def duration(self):
        return sum(r.duration for r in self.recipes)

    @property
    @cache
    def id(self):
        return ','.join(str(r.id) for r in self.recipes)

    def __len__(self):
        return len(self.recipes)

    def print_mermaid(self) -> None:
        print('---')
        print(f'title: Chain {self.id}')
        print('---')
        print('flowchart TD')

        input_flows = {k: v for k, v in self.flows.items() if v < 0}
        output_flows = {k: v for k, v in self.flows.items() if v > 0}

        # define inputs
        for rs, qty in self.flows.items():
            nodeid = slugify(rs.name)
            assert qty != 0
            print(f'i{nodeid}(["{rs.name} x{-qty:g}"])'
                  if qty < 0 else
                  f'o{nodeid}(["{rs.name} x{qty:g}"])')

        for i, recipe in enumerate(self.recipes):
            nodeid_recipe = f'r{i}'
            print(
                f'{nodeid_recipe}["{recipe.times}x Recipe {recipe.id}<br>{recipe.machine.value}<br>{recipe.energy}EU {recipe.duration}s"]')

            for rs, qty in (recipe.inputs & input_flows).items():
                label = '' if qty == -input_flows[rs] else f'|"x{qty:g} ({qty/-input_flows[rs]:.2%})"|'
                print(f'i{slugify(rs.name)}-->{label}{nodeid_recipe}')

            for rs, qty in (recipe.outputs & output_flows).items():
                label = '' if qty == output_flows[rs] else f'|"x{qty:g} ({qty/output_flows[rs]:.2%})"|'
                print(f'{nodeid_recipe}-->{label}o{slugify(rs.name)}')
            for rs, qty in recipe.outputs.exclude(output_flows).items():
                print(f'r{i}-->|{rs.name} x{qty:g}|r{i+1}')


def slugify(s: str):
    return re.sub(r'\W+', '-', s).strip('-').lower()


def chain(recipes: Iterable[Recipe]):
    final_recipes: list[Recipe]=[]

    flows=ValuedSet[Resource]()

    prev_recipe: Recipe | None=None
    for recipe in recipes:
        if prev_recipe:
            misflows=prev_recipe.outputs.delta(recipe.inputs)
            if len(misflows) != 0:
                r=misflows.single()[0]
                recipe *= (prev_recipe.outputs[r] / recipe.inputs[r])
        prev_recipe=recipe

        flows -= recipe.inputs
        flows += recipe.outputs

        final_recipes.append(recipe)

    return Chain(tuple(final_recipes), flows)
