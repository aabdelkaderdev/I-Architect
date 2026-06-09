from __future__ import annotations

from typing import Literal

MergeStrategy = Literal["overwrite", "append", "append_unique", "merge_by_key", "never"]

OVERWRITE: MergeStrategy = "overwrite"
APPEND: MergeStrategy = "append"
APPEND_UNIQUE: MergeStrategy = "append_unique"
MERGE_BY_KEY: MergeStrategy = "merge_by_key"
NEVER: MergeStrategy = "never"
