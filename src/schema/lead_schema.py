from pydantic import BaseModel, EmailStr
from typing import Optional


class LeadSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    serviceType: Optional[str]
    zipCode: Optional[str]
    projectDescription: Optional[str]


class GetLeadSchema(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    serviceType: Optional[str]
    zipCode: Optional[str]
    projectDescription: Optional[str]