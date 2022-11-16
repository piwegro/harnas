from dataclasses import dataclass


@dataclass
class Error:
    message: str

    @classmethod
    def from_exception(cls, e: Exception) -> "Error":
        return cls(str(e))

    def __str__(self):
        return self.message

    def to_json(self):
        escaped_message = self.message.replace('"', '\\"')
        return f'{{"error": "{escaped_message}"}}'
