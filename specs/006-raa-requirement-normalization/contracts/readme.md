# Requirement Normalization Contract

Any implementation of the normalization node must preserve the field keys and types of the output dictionary.
Missing quality attributes and condition fields in non-ASR inputs must default to `[]` and `None` respectively, instead of being omitted.
If an input requirement ID does not match any entry in the parent requirements mapping, a `KeyError` must be thrown.
