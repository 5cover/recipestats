#!/bin/env python3

from gtceu import chain, Chain, Resource, Type, Recipe, recipe, Machine, Oc, TIER
from lines import print_box

R = {
    'Cobalt Dust': Resource(Type.ITEM, 'Cobalt Dust', 100),
    'Sulfur Dust': Resource(Type.ITEM, 'Sulfur Dust', 25),
    'Stone Dust': Resource(Type.ITEM, 'Stone Dust', 5),
    'Sodium Persulfate': Resource(Type.FLUID, 'Sodium Persulfate', .67),
    'Water': Resource(Type.FLUID, 'Water', .002),
    'Distilled Water': Resource(Type.FLUID, 'Distilled Water', .025),
    'Cobalt Ingot': Resource(Type.ITEM, 'Cobalt Ingot', 0),
    'Cobaltite Dust': Resource(Type.ITEM, 'Cobaltite Dust', 0),
    'Crushed Cobaltite Ore': Resource(Type.ITEM, 'Crushed Cobaltite Ore', 0),
    'Impure Pile of Cobaltite Dust': Resource(Type.ITEM, 'Impure Pile of Cobaltite Dust', 0),
    'Purified Cobaltite Ore': Resource(Type.ITEM, 'Purified Cobaltite Ore', 0),
    'Purified Pile of Cobaltite Dust': Resource(Type.ITEM, 'Purified Pile of Cobaltite Dust', 0),
    'Raw Cobaltite': Resource(Type.ITEM, 'Raw Cobaltite', 0),
    'Refined Cobaltite Ore': Resource(Type.ITEM, 'Refined Cobaltite Ore', 0),
}

SMELTING_SECS = 10
'Seconds taken per smelting operation'
SMELTING_EU = 6400
'EUs spent per smelting operation'


def chance(probability: float, boost: float) -> float:
    return probability + boost * TIER.value


RECIPES = (
    recipe(Machine.SMELTING,
           {R['Raw Cobaltite']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.FORGE_HAMMER,
           {R['Raw Cobaltite']: 1},
           {R['Crushed Cobaltite Ore']: 1},
           .5, 160, Oc.LV),
    recipe(Machine.MACERATOR,
           {R['Raw Cobaltite']: 1},
           {R['Crushed Cobaltite Ore']: 2,
            R['Sulfur Dust']: chance(.1, .03),
            R['Stone Dust']: chance(.5, .01)},
           20, 800, Oc.LV),

    recipe(Machine.SMELTING,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    #!recipe(Machine.CHEMICAL_BATH,
    #!       {R['Crushed Cobaltite Ore']: 1,
    #!        R['Sodium Persulfate']: 100},
    #!       {R['Purified Cobaltite Ore']: 1,
    #!        R['Cobalt Dust']: chance(.7, .058),
    #!        R['Stone Dust']: chance(.4, .065)},
    #!       10, 6000, Oc.LV),
    recipe(Machine.FORGE_HAMMER,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Impure Pile of Cobaltite Dust']: 1},
           .5, 160, Oc.LV),
    recipe(Machine.MACERATOR,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Impure Pile of Cobaltite Dust']: 1,
            R['Sulfur Dust']: chance(.14, .085)},
           20, 800, Oc.LV),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Water']: 1000},
           {R['Purified Cobaltite Ore']: 1,
            R['Sulfur Dust']: 1/3,
            R['Stone Dust']: 1},
           20, 6400, Oc.LV),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Distilled Water']: 100},
           {R['Purified Cobaltite Ore']: 1,
            R['Sulfur Dust']: 1/3,
            R['Stone Dust']: 1},
           10, 3200, Oc.LV),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Water']: 100},
           {R['Purified Cobaltite Ore']: 1},
           .4, 32, Oc.LV),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Refined Cobaltite Ore']: 1,
            R['Cobalt Dust']: 1/3,
            R['Stone Dust']: 1},
           20, 12000, Oc.LV),

    recipe(Machine.SMELTING,
           {R['Purified Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.FORGE_HAMMER,
           {R['Purified Cobaltite Ore']: 1},
           {R['Purified Pile of Cobaltite Dust']: 1},
           .5, 160, Oc.LV),
    recipe(Machine.MACERATOR,
           {R['Purified Cobaltite Ore']: 1},
           {R['Purified Pile of Cobaltite Dust']: 1,
            R['Cobalt Dust']: chance(.14, .085)},
           20, 800, Oc.LV),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Purified Cobaltite Ore']: 1},
           {R['Refined Cobaltite Ore']: 1,
            R['Cobalt Dust']: 1/3},
           20, 12000, Oc.LV),

    recipe(Machine.SMELTING,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.FORGE_HAMMER,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobaltite Dust']: 1},
           .5, 160, Oc.LV),
    recipe(Machine.MACERATOR,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobaltite Dust']: 1,
            R['Cobalt Dust']: chance(.14, .085)},
           20, 800, Oc.LV),

    recipe(Machine.SMELTING,
           {R['Impure Pile of Cobaltite Dust']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.CENTRIFUGE,
           {R['Impure Pile of Cobaltite Dust']: 1},
           {R['Cobaltite Dust']: 1,
            R['Sulfur Dust']: 1/9},
           11, 5280, Oc.LV),
    recipe(Machine.ORE_WASHER,
           {R['Impure Pile of Cobaltite Dust']: 1,
            R['Water']: 100},
           {R['Cobaltite Dust']: 1},
           .4, 32),

    recipe(Machine.CENTRIFUGE,
           {R['Purified Pile of Cobaltite Dust']: 1},
           {R['Cobaltite Dust']: 1,
            R['Cobalt Dust']: 1/9},
           5, 500, Oc.LV),
    recipe(Machine.ORE_WASHER,
           {R['Purified Pile of Cobaltite Dust']: 1,
            R['Water']: 100},
           {R['Cobaltite Dust']: 1},
           .4, 32),

    recipe(Machine.SMELTING,
           {R['Cobaltite Dust']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),

    recipe(Machine.MACERATOR,
           {R['Cobalt Ingot']: 1},
           {R['Cobalt Dust']: 1},
           2.95, 118, Oc.LV)
)


def get_chains(goal: Resource):
    chains: list[tuple[Recipe, ...]] = []
    for goal_recipe in (r for r in RECIPES if goal in r.outputs):

        prev_chains: set[tuple[Recipe, ...]] = set()
        for r in goal_recipe.inputs:
            prev_chains.update(get_chains(r))

        if prev_chains:
            chains.extend(c + (goal_recipe,) for c in prev_chains)
        else:
            chains.append((goal_recipe,))
    return chains


def resource_efficiency(chain: Chain, goal: Resource):
    cobalt_inputs = sum(qty for res, qty in chain.flows.items() if res == goal and qty < 0)
    cobalt_outputs = sum(qty for res, qty in chain.flows.items() if res == goal and qty > 0)

    return cobalt_outputs / (abs(cobalt_inputs) if cobalt_inputs else 1)


def value_minus_cost(chain: Chain):
    return chain.value - chain.cost


if __name__ == '__main__':
    chains = map(chain, get_chains(R['Cobalt Dust']))
    c = max(chains, key=lambda x: resource_efficiency(x, R['Cobalt Dust']))
    for i, r in enumerate(c.recipes, 1):
        print_box(r.to_lines(i), indent=2)
    for resource, quantity in sorted(c.flows.items(), key=lambda kv: kv[1]):
        print(f'* {round(quantity, 3):g} {resource}')
    print(f'value: {c.value:g}')
    print(f'cost: {c.cost:g}')
    print(f'energy: {c.energy:g}')
    print(f'duration: {c.duration:g}')
