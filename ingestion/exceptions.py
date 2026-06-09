class EmptyFileError(ValueError):
    """Raised when the input file is 0 bytes."""
    pass

class UnsupportedFormatError(ValueError):
    """Raised when the file extension does not match any supported format."""
    pass

class ExtractionError(RuntimeError):
    """Raised when a format-specific extractor finds no extractable text."""
    pass

class EmptyRequirementsError(ValueError):
    """Raised when the final requirement set contains zero entries."""
    pass

class NonStandardJSONError(ValueError):
    """Raised when a JSON file fails schema validation."""
    def __init__(self, reason: str, offending_keys: list[str] | None = None):
        self.reason = reason
        self.offending_keys = offending_keys or []
        msg = f"Non-standard JSON format — {reason}: keys {self.offending_keys}"
        super().__init__(msg)

class FormatMismatchError(ValueError):
    """Raised when a file's extension does not match its content."""
    pass
