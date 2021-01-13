from pydantic.main import BaseModel


class Destination(BaseModel):
    id: int
    name: str
    height: float
    isOpen: bool = True

    def __hash__(self) -> int:
        return self.id
