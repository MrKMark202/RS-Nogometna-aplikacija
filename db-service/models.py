from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]


class User(BaseModel):
    ime: str
    prezime: str
    datumRodenja: str
    email: EmailStr
    password: str = Field(min_length=6)
    profilnaSlika: str
    pin: int
    
class League(BaseModel):
    naziv: str
    godinaOsnivanja: str
    drzava: str
    grbLige: str
    korisnik: ObjectIdStr
    
class Club(BaseModel):
    naziv: str
    godinaOsnivanja: str
    drzava: str
    grbKluba: str
    liga: ObjectIdStr
    korisnik: ObjectIdStr
    
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
    
class Table(BaseModel):
    bodovi: int
    postignutiPogodci: int
    primljeniPogodci: int
    odigraniDvoboji: int
    grb: str
    liga: ObjectIdStr
    klub: ObjectIdStr
    korisnik: ObjectIdStr