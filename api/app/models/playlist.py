from pydantic import BaseModel

class PlaylistModel(BaseModel):
    name: str 
    user_id: str