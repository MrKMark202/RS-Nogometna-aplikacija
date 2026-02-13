from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    ime: str
    prezime: str
    datumRodenja: str
    email: EmailStr
    password: str = Field(min_length=6)
    profilnaSlika: str
    pin: int
