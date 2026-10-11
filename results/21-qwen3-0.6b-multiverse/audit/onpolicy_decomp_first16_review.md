# Blind semantic review: onpolicy decomposition first16

| ID / seed | Verdict | Reason |
| --- | --- | --- |
| `math-train/110` / 0 | reject | Paths correctly and independently obtain 15 and 17, and external 255 is correct. But Conclusion is internally inconsistent: it calls the first grouped factor 15 and the third factor 17, then falsely states that the second factor is 17 twice. The actual middle factor is 5. Strict acceptance requires a correct internally consistent Conclusion. |
| `gsm8k-train/2528` / 0 | reject | Paths and external answer 7 are correct, but setup before `<Parallel>` already computes both areas and the final difference `25-18=7`. The block therefore adds no work and violates the no-precomputed-answer criterion. |

**Result: accept 0/2, reject 2/2.**
