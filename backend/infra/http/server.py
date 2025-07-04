from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv(dotenv_path='.env')

app = FastAPI()
