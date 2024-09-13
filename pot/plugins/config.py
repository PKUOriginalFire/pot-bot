from pydantic import BaseModel


class Config(BaseModel):
    account: int
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int = 25
    mailto: str
