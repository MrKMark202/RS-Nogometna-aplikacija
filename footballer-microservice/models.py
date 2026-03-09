from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class Footballer(BaseModel):
    ime: str
    datumRodjenja: str
    drzavljanstvo: str
    slikaIgraca: str
    klub: ObjectIdStr
    korisnikEmail: str
    blockchainPlayerId: int
    initialValue: int = 0

