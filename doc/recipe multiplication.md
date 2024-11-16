# Recipe multiplication

{2 CCO, .13 SD, .51 StD}
{1 CCO}

intersection o difference = {1 CCO}

so the resource CCO overflows

we see the remaining output resources partially consumed by the next recipe
now what?
we need to find X the multiplier of the next recipe to fully consume the previous recipe's output

Previous Output / Next Output
{2 CCO} / {1 CCO}
= 2

---

{2 IPCD, .45 SD}
{2 IPCD}

intersection o difference = {}

---

Okay but what if we have a more complex situation?

M_A output = {2 CCO, 2 Grass}
M_B input = {1 CCO, 2 Grass}
intersection o difference = {1 CCO}

What to do?

M_B x2: {2 CCO, 4 Grass}
Adds chain input of 2 Grass

Okay but what if we have a more complex situation, involving multiple overflowing outputs?

M_A output = {3 CCO, 2 Grass}
M_B input = {1 CCO, 1 Grass}
intersection o difference = {2 CCO, 1 Grass}

What to do?

M_B x2 = {2 CCO, 2 Grass}
Adds chain output of 1 CCO

M_B x3 = {3 CCO, 3 Grass}
Adds chain input of 1 Grass

Can the CCO be processed in a branch of the chain? Or be used by a further recipe?

Is inputting Grass more costly than the added value of multipling M_B by 3 instead of 2?

(Can we multiply previous recipes to get more Grass?)

FUCK

Although I don't need to handle this kind of complex scenario here. Since the recipes form a tree, it's only about finding the best path from Raw Cobaltite to Cobalt Dust. No recipes have the above pattern, thankfully.

A sane approach would be to look at further recipes:

- If one of them has a CCO input that is not supplied by the previous recipe, then do Mb_x2
- If one of them has a Grass output that is not consumed by the next recipe, then do Mb_x3

## Conclusion

1. Implement the ValuedSet intersection o difference operation (find a better name for it)
2. In the flow property loop, before anything else, check the intersection o differennce between prev_recipe's output and recipe's input (save it in a variable named `misflows` (overflows or underflows))
3. If non-empty, assert that len == 1 (this should never happen with our current recipe set)
