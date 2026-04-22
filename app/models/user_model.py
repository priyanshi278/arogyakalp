from pydantic import BaseModel, Field

class User(BaseModel):
    imr_number: str = Field(..., description="Indian Medical Registration Number")
    name: str = Field(..., description="Full Name of the Doctor")
    phone_number: str = Field(..., description="Contact Phone Number")

class UserLogin(BaseModel):
    imr_number: str
    phone_number: str
