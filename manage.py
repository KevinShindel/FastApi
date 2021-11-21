from typing import Optional

from fastapi import FastAPI, status
import uvicorn
from starlette.background import BackgroundTasks

from app.models import Base
from settings.database import engine, get_db
from app.tasks import write_notification


Base.metadata.create_all(bind=engine)
app = FastAPI()
get_db()


@app.get(path="/", status_code=status.HTTP_200_OK, tags=['root'], summary="Initial url", description="Just send json")
def index() -> dict:
    """
    Simple GET response
    :return: dict
    """
    return {"message": "Hello world!"}


@app.post(path="/send-notification/{email}", status_code=status.HTTP_200_OK)
async def send_notification(email: str, background_tasks: BackgroundTasks) -> dict:
    """
       Create an item with all the information:

       - **name**: each item must have a name
       - **description**: a long description
       - **price**: required
       - **tax**: if the item doesn't have tax, you can omit this
       - **tags**: a set of unique tag strings for this item
       """

    """
    Run async task
    from requests import post
    url = 'http://localhost:8000/send-notification/email=shindel'
    result = post(url=url)
    :param email: email user
    :param background_tasks: None
    :return: Message
    """

    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@app.get(path="/items/", status_code=status.HTTP_200_OK)
async def read_item(skip: int = 0, limit: int = 10):
    'Query Parameters test'
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip: skip + limit]


@app.get(path="/items/{item_id}", status_code=status.HTTP_200_OK)
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
