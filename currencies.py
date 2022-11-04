from dataclasses import dataclass


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Currency:
    name: str
    symbol: str
    value: float

    # TODO: Implement – gets all currencies from the database
    #  Should raise an exception if the operation fails
    @classmethod
    def get_currencies(cls) -> list["Currency"]:
        return []

    # TODO: Implement converting, needs to round a value (can't have 2.9203 of a beer)
    def convert_to(self, other_currency: "Currency") -> int:
        return 0

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self) -> str:
        return ""

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        return ""
