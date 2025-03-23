from pydantic import BaseModel

class MusicModel(BaseModel):
    name: str 
    playlist: str
    user_id: str