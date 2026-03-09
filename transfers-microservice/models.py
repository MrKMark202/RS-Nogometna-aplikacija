from pydantic import BaseModel, Field
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern=r"^[a-fA-F0-9]{24}$")]

class Transfer(BaseModel):
    igracId: str
    stariKlubId: str
    noviKlubId: str
    datumTransfera: str
    korisnikEmail: str
    transakcijaHash: str # Blockchain transaction hash
    vrijednost: int = 0
