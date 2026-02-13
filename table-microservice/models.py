from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class Table(BaseModel):
    bodovi: int
    postignutiPogodci: int
    primljeniPogodci: int
    odigraniDvoboji: int
    grb: str
    liga: ObjectIdStr
    klub: ObjectIdStr
    korisnik: ObjectIdStr