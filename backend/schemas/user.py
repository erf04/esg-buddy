from pydantic import BaseModel,EmailStr, ConfigDict



class UserOut(BaseModel):
    id : str 
    first_name : str | None = None
    last_name : str | None = None
    email : EmailStr

    model_config = ConfigDict(from_attributes=True)