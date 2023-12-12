import pydantic

from pydantic import BaseModel


class Input(BaseModel):
    number: int
    string: string
