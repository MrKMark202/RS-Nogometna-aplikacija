from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class Match(BaseModel):
    kolo: int
    stadionNaziv: str
    mjestoIgranja: str
    gledateljiBroj: int
    datum: str
    satUpisa: str
    domacinGol: int
    gostiGol: str
    liga: ObjectIdStr
    domacin: ObjectIdStr
    gost: ObjectIdStr
    korisnik: ObjectIdStr