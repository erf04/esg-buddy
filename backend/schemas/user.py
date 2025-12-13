from pydantic import BaseModel, ConfigDict



class UserOut(BaseModel):
    id : str 
    first_name : str | None = None
    last_name : str | None = None
    email : str

    model_config = ConfigDict(from_attributes=True)