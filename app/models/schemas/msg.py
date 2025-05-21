from pydantic import BaseModel

# Schema cho thông báo chung
class Msg(BaseModel):
    message: str