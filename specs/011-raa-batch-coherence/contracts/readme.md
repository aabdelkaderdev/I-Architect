# Batch Coherence Gate Contracts

The coherence gate node must evaluate incoming requirement batches.
The coherence score threshold is exactly `0.55`.
Batches below this threshold must trigger a split.
Splits must be computed using a deterministic clustering algorithm (such as K-Means initialized with the two furthest vectors in the batch).
If either sub-batch remains incoherent (< 0.55), the original batch must be routed to the incoherent list with the flag `reduced_confidence = true`.
Small batches (length <= 2) must automatically pass the coherence gate.
