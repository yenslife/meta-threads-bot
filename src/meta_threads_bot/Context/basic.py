from pydantic import BaseModel


class PostContent(BaseModel):
    csrf_token: str
    session_id: str
    ds_user_id: str
    username: str
    password: str
