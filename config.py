from dataclasses import dataclass
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

@dataclass
class Config:
    client_id: str = environ.get("CLIENT_ID")
    client_secret: str = environ.get("CLIENT_SECRET")
    url: str = environ.get("URL")
    username: str = environ.get("USERNAME")
    password: str = environ.get("PASSWORD")