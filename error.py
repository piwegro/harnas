from dataclasses import dataclass


@dataclass
class Error:
    message: str

    @classmethod
    def from_exception(cls, e: Exception) -> "Error":
        return cls(str(e))
