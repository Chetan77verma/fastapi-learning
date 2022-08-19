from configparser import SectionProxy
from pydantic import BaseSettings


class Setting(BaseSettings):
    database_hostname:str
    database_port: str
    database_username:str
    database_password:str
    database_name:str
    secret_key:str
    algorithm:str
    access_token_expire_minute:int

    class Config:
        env_file = ".env"

settings = Setting()