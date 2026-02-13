from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class Club(BaseModel):
    naziv: str
    godinaOsnivanja: str
    drzava: str
    grbKluba: str
    liga: ObjectIdStr
    korisnik: ObjectIdStr