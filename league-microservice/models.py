from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class League(BaseModel):
    naziv: str
    godinaOsnivanja: str
    drzava: str
    grbLige: str
    korisnik: ObjectIdStr