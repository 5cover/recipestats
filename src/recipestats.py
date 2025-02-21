#!/bin/env python3

from gtceu import chain, Chain, Resource, Type, Recipe, recipe, Machine, TIER
from lines import print_box

R = {
    'Cobalt Dust': Resource(Type.ITEM, 'Cobalt Dust', 100),
    'Sulfur Dust': Resource(Type.ITEM, 'Sulfur Dust', 25),
    'Stone Dust': Resource(Type.ITEM, 'Stone Dust', 5),
    'Sodium Persulfate': Resource(Type.FLUID, 'Sodium Persulfate', .9),
    'Water': Resource(Type.FLUID, 'Water', 0),
    'Distilled Water': Resource(Type.FLUID, 'Distilled Water', .001),
    'Cobalt Ingot': Resource(Type.ITEM, 'Cobalt Ingot', 1),
    'Cobaltite Dust': Resource(Type.ITEM, 'Cobaltite Dust', 1),
    'Crushed Cobaltite Ore': Resource(Type.ITEM, 'Crushed Cobaltite Ore', 1),
    'Impure Pile of Cobaltite Dust': Resource(Type.ITEM, 'Impure Pile of Cobaltite Dust', 1),
    'Purified Cobaltite Ore': Resource(Type.ITEM, 'Purified Cobaltite Ore', 1),
    'Purified Pile of Cobaltite Dust': Resource(Type.ITEM, 'Purified Pile of Cobaltite Dust', 1),
    'Raw Cobaltite': Resource(Type.ITEM, 'Raw Cobaltite', 1),
    'Refined Cobaltite Ore': Resource(Type.ITEM, 'Refined Cobaltite Ore', 1),

    'Raw Sapphire': Resource(Type.ITEM, 'Raw Sapphire', 1),
    'Sapphire': Resource(Type.ITEM, 'Sapphire', 1),
    'Crushed Sapphire Ore': Resource(Type.ITEM, 'Crushed Sapphire Ore', 1),
    'Aluminium Dust': Resource(Type.ITEM, 'Aluminium Dust', 100),
    'Purified Sapphire Ore': Resource(Type.ITEM, 'Purified Sapphire Ore', 1),
    'Exquisite Sapphire': Resource(Type.ITEM, 'Exquisite Sapphire', 1),
    'Flawless Sapphire': Resource(Type.ITEM, 'Flawless Sapphire', 1),
    'Purified Pile of Sapphire Dust': Resource(Type.ITEM, 'Purified Pile of Sapphire Dust', 1),
    'Impure Pile of Sapphire Dust': Resource(Type.ITEM, 'Impure Pile of Sapphire Dust', 1),
    'Green Sapphire Dust': Resource(Type.ITEM, 'Green Sapphire Dust', 1),
    'Sapphire Dust': Resource(Type.ITEM, 'Sapphire Dust', 1),
    'Small Pile of Sapphire Dust': Resource(Type.ITEM, 'Small Pile of Sapphire Dust', 1),
    'Refined Sapphire Ore': Resource(Type.ITEM, 'Refined Sapphire Ore', 1),
    'Oxygen Gas': Resource(Type.FLUID, 'Oxygen Gas', 1),
    'Lubricant': Resource(Type.FLUID, 'Lubricant', 1),
    'Sapphire Lens': Resource(Type.ITEM, 'Sapphire Lens', 1),

    # 'Dynamite': Resource(Type.ITEM, 'Dynamite', 1),
    # 'Paper': Resource(Type.ITEM, 'Paper', 1),
    # 'Glyceryl Trinitrate': Resource(Type.FLUID, 'Glyceryl Trinitrate', 1),
    # 'TNT': Resource(Type.ITEM, 'TNT', 1),
    # 'Powderbarrel': Resource(Type.ITEM, 'Powderbarrel', 1),
}

SMELTING_SECS = 10
'Seconds taken per smelting operation'
SMELTING_EU = 6400
'EUs spent per smelting operation'


def chance(probability: float, boost: float) -> float:
    return probability + boost * TIER.value


RECIPES = (
    # Cobaltite processing

    recipe(Machine.SMELTING,
           {R['Raw Cobaltite']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.ORE_CRUSHING,
           {R['Raw Cobaltite']: 1},
           {R['Crushed Cobaltite Ore']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Raw Cobaltite']: 1},
           {R['Crushed Cobaltite Ore']: 2,
            R['Sulfur Dust']: chance(.1, .03),
            R['Stone Dust']: chance(.5, .01)},
           20, 800),

    recipe(Machine.SMELTING,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    #!recipe(Machine.ORE_TREATING,
    #!       {R['Crushed Cobaltite Ore']: 1,
    #!        R['Sodium Persulfate']: 100},
    #!       {R['Purified Cobaltite Ore']: 1,
    #!        R['Cobalt Dust']: chance(.7, .058),
    #!        R['Stone Dust']: chance(.4, .065)},
    #!       10, 6000),
    recipe(Machine.ORE_CRUSHING,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Impure Pile of Cobaltite Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Impure Pile of Cobaltite Dust']: 1,
            R['Sulfur Dust']: chance(.14, .085)},
           20, 800),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Water']: 1000},
           {R['Purified Cobaltite Ore']: 1,
            R['Sulfur Dust']: 1/3,
            R['Stone Dust']: 1},
           20, 6400, 1),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Distilled Water']: 100},
           {R['Purified Cobaltite Ore']: 1,
            R['Sulfur Dust']: 1/3,
            R['Stone Dust']: 1},
           10, 3200),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Cobaltite Ore']: 1,
            R['Water']: 100},
           {R['Purified Cobaltite Ore']: 1},
           .4, 32, 2),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Crushed Cobaltite Ore']: 1},
           {R['Refined Cobaltite Ore']: 1,
            R['Cobalt Dust']: 1/3,
            R['Stone Dust']: 1},
           20, 12000),

    recipe(Machine.SMELTING,
           {R['Purified Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.ORE_CRUSHING,
           {R['Purified Cobaltite Ore']: 1},
           {R['Purified Pile of Cobaltite Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Purified Cobaltite Ore']: 1},
           {R['Purified Pile of Cobaltite Dust']: 1,
            R['Cobalt Dust']: chance(.14, .085)},
           20, 800),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Purified Cobaltite Ore']: 1},
           {R['Refined Cobaltite Ore']: 1,
            R['Cobalt Dust']: 1/3},
           20, 12000),

    recipe(Machine.SMELTING,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.ORE_CRUSHING,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobaltite Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Refined Cobaltite Ore']: 1},
           {R['Cobaltite Dust']: 1,
            R['Cobalt Dust']: chance(.14, .085)},
           20, 800),

    recipe(Machine.SMELTING,
           {R['Impure Pile of Cobaltite Dust']: 1},
           {R['Cobalt Ingot']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.CENTRIFUGE,
           {R['Impure Pile of Cobaltite Dust']: 1},
           {R['Cobaltite Dust']: 1,
            R['Sulfur Dust']: 1/9},
           11, 5280),
    recipe(Machine.ORE_WASHER,
           {R['Impure Pile of Cobaltite Dust']: 1,
            R['Water']: 100},
           {R['Cobaltite Dust']: 1},
           .4, 32),

    recipe(Machine.CENTRIFUGE,
           {R['Purified Pile of Cobaltite Dust']: 1},
           {R['Cobaltite Dust']: 1,
            R['Cobalt Dust']: 1/9},
           5, 500),
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
           2.95, 118),

    # Sapphire ore processing

    recipe(Machine.SMELTING,
           {R['Raw Sapphire']: 1},
           {R['Sapphire']: 1},
           SMELTING_SECS, SMELTING_EU),
    recipe(Machine.ORE_CRUSHING,
           {R['Raw Sapphire']: 1},
           {R['Sapphire']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Raw Sapphire']: 1},
           {R['Crushed Sapphire Ore']: 2, R['Aluminium Dust']: .1, R['Stone Dust']: .05},
           20, 800),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Sapphire Ore']: 1, R['Water']: 1000},
           {R['Purified Sapphire Ore']: 1, R['Aluminium Dust']: 1/3, R['Stone Dust']: 1},
           20, 6400, 1),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Sapphire Ore']: 1, R['Water']: 000},
           {R['Purified Sapphire Ore']: 1},
           20, 6400, 2),
    recipe(Machine.ORE_WASHER,
           {R['Crushed Sapphire Ore']: 1, R['Distilled Water']: 100},
           {R['Purified Sapphire Ore']: 1, R['Aluminium Dust']: 1/3, R['Stone Dust']: 1},
           20, 6400),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Crushed Sapphire Ore']: 1},
           {R['Refined Sapphire Ore']: 1, R['Green Sapphire Dust']: 1/3, R['Stone Dust']: 1},
           20, 12000),
    recipe(Machine.ORE_GRINDING,
           {R['Crushed Sapphire Ore']: 1},
           {R['Impure Pile of Sapphire Dust']: 1, R['Aluminium Dust']: chance(.14, .085)},
           20, 800),
    recipe(Machine.ORE_CRUSHING,
           {R['Crushed Sapphire Ore']: 1},
           {R['Impure Pile of Sapphire Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_WASHER,
           {R['Impure Pile of Sapphire Dust']: 1, R['Water']: 100},
           {R['Sapphire Dust']: 1},
           .4, 32, 2),
    recipe(Machine.CENTRIFUGE,
           {R['Impure Pile of Sapphire Dust']: 1},
           {R['Sapphire Dust']: 1, R['Aluminium Dust']: 1},
           4, 1920),
    recipe(Machine.SIFTER,
           {R['Purified Sapphire Ore']: 1},
           {R['Exquisite Sapphire']: chance(.05, .015),
            R['Flawless Sapphire']: chance(.15, .02),
            R['Sapphire']: chance(.5, .1),
            R['Purified Pile of Sapphire Dust']: chance(.25, .05)},
           20, 6400),
    recipe(Machine.THERMAL_CENTRIFUGE,
           {R['Purified Sapphire Ore']: 1},
           {R['Refined Sapphire Ore']: 1, R['Green Sapphire Dust']: 1/3},
           20, 12000),
    recipe(Machine.ORE_GRINDING,
           {R['Purified Sapphire Ore']: 1},
           {R['Purified Pile of Sapphire Dust']: 1, R['Green Sapphire Dust']: chance(.14, .085)},
           20, 800),
    recipe(Machine.ORE_CRUSHING,
           {R['Purified Sapphire Ore']: 1},
           {R['Purified Pile of Sapphire Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_GRINDING,
           {R['Refined Sapphire Ore']: 1},
           {R['Sapphire Dust']: 1, R['Green Sapphire Dust']: chance(.14, .085)},
           20, 800),
    recipe(Machine.ORE_CRUSHING,
           {R['Refined Sapphire Ore']: 1},
           {R['Sapphire Dust']: 1},
           .5, 160),
    recipe(Machine.ORE_WASHER,
           {R['Purified Pile of Sapphire Dust']: 1, R['Water']: 100},
           {R['Sapphire Dust']: 1},
           .4, 32, 2),
    recipe(Machine.CENTRIFUGE,
           {R['Purified Pile of Sapphire Dust']: 1},
           {R['Sapphire Dust']: 1, R['Green Sapphire Dust']: 1/9},
           5, 500),
    recipe(Machine.ELECTROLYZER,
           {R['Green Sapphire Dust']: 5},
           {R['Aluminium Dust']: 2},
           5, 3000),
    recipe(Machine.ELECTROLYZER,
           {R['Sapphire Dust']: 5},
           {R['Aluminium Dust']: 2},
           5, 3000),
    recipe(Machine.CUTTER,
           {R['Exquisite Sapphire']: 1, R['Lubricant']: 1},
           {R['Flawless Sapphire']: 2},
           1, 320),
    recipe(Machine.CUTTER,
           {R['Exquisite Sapphire']: 1, R['Water']: 4},
           {R['Flawless Sapphire']: 2},
           2, 640),
    recipe(Machine.CUTTER,
           {R['Exquisite Sapphire']: 1, R['Distilled Water']: 3},
           {R['Flawless Sapphire']: 2},
           1.5, 480),
    recipe(Machine.LATHE,
           {R['Exquisite Sapphire']: 1},
           {R['Sapphire Lens']: 1, R['Sapphire Dust']: 2},
           120, 72000),
    recipe(Machine.PART_GRINDING,
           {R['Exquisite Sapphire']: 1},
           {R['Sapphire Dust']: 4},
           4, 160),
    recipe(Machine.PART_GRINDING,
           {R['Sapphire Lens']: 1},
           {R['Small Pile of Sapphire Dust']: 3},
           .75, 30),
    recipe(Machine.PACKER,
           {R['Small Pile of Sapphire Dust']: 4},
           {R['Sapphire Dust']: 1},
           .5, 120, 1)
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


def value_over_cost(chain: Chain):
    return chain.value / chain.cost


def cost_over_value(chain: Chain):
    return chain.cost / chain.value


def cost_minus_value(chain: Chain):
    return chain.cost - chain.value


def print_chain(c: Chain):
    for i, r in enumerate(c.recipes, 1):
        print_box(r.to_lines(i), indent=2)
    print(f'chain {c.id}')
    print()
    for resource, quantity in sorted(c.flows.items(), key=lambda kv: kv[1]):
        print(f'* {round(quantity, 3):g} {resource}')
    print(f'value: {c.value:g}')
    print(f'cost: {c.cost:g}')
    print(f'energy: {c.energy:g}EU')
    print(f'duration: {c.duration:g}s')


if __name__ == '__main__':
    target = R['Aluminium Dust']
    chains = map(chain, get_chains(target))
    
    c = max(chains, key=lambda x: resource_efficiency(x, target))
    #print_chain(c)
    c.print_mermaid()
