# Overlap Bridging Contracts

The overlap bridging node must compare group centroids and select shared base requirements.
The bridging score must be calculated using multiplicative scoring ($S_1 \times S_2$).
No more than `3` bridge requirements may be selected for any adjacent pair.
Bridge mappings must be stored in the state's `bridge_requirements` registry dictionary under lexicographically sorted pair keys.
Selected bridge requirements must be injected into both corresponding batch requirements lists.
