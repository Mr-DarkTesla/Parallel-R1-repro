# Batch 4 repair notes

Retained 3 of 4 newly rejected raw 4B rollouts.

- `gsm8k-train/1856`: omitted. The sister's 15 slices are directly stated, so a second sibling calculation would be tautological or contrived.
- `gsm8k-train/4374`: used two complete, nonduplicative calculations: total servings divided by jar capacity, and days covered by one jar.
- `math-train/7012`: derived the direction-vector component and base-point component separately.
- `math-train/1366`: derived each quadratic-formula branch completely inside its own path; no root sum is stated before the block.

Each response has one numbered `<Parallel>` block within `<think>`, two substantive paths, a Conclusion using both paths, and a Final Answer matching its gold value.
