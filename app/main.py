from fastapi import FastAPI

from app.database import init_db

app = FastAPI()
# initialize database
init_db(app)


# add endpoints here
@app.get('/')
def ping():
    return "Root path"
