from pydantic import BaseModel

class SMSRequest(BaseModel):
    message: str