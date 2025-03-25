from sqlalchemy import and_
from fastapi import FastAPI
from sqlalchemy import select
from api.app.database.schemas.schemas import User, Playlist, Music
from api.app.database.db.db import getSession
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.app.models.playlist import PlaylistModel
from api.app.models.music import MusicModel
app = FastAPI()


@app.get("/api/get/user/{userName}")
def getUser(userName: str):
    session = getSession()
    
    # Buscar o primeiro resultado ou retornar None
    user = session.execute(select(User).where(User.name == userName)).scalar().first()

    if user is None:
        return {"message": f"User {userName} not found"}
    return user.name


@app.get("/api/get/playlist/{userName}/{playlistName}")
def getUserPlaylists(userName: str, playlistName: str):
    session = getSession()
    
    playlist = session.execute(select(Playlist)
                               .where(Playlist.name == playlistName)
                               .where(Playlist.user_id == userName)
                               ).scalars().first()

    if playlist is None:
        return {"message": f"Playlist {playlistName} for user {userName} not found"}
    
    return playlist

@app.get("/api/get/userplaylists/{userName}")
def getUserPlaylists(userName: str):
    session = getSession()
    
    playlists = session.execute(select(Playlist).where(Playlist.user_id == userName)).scalars().all()

    if not playlists:
        return {"message": f"Playlists for user {userName} not found"}

    playlist_list = [playlist.as_dict() for playlist in playlists]
    
    return playlist_list


@app.post('/api/post/addMusicPlaylist')
def addMusicToPlaylist(music: MusicModel):
    "USUÁRIO DEVE FORNECER O NOME DA PLAYLIST E O NOME DA MÚSICA PARA SER ADICIONADA NA PLAYLIST"

    session = getSession()
    #get user's id first
    try:
        user = session.execute(select(User).where(User.name == music.user_id)).scalar()
        playlist = session.execute(select(Playlist).where(Playlist.name == music.playlist and Playlist.user_id == music.user_id)).scalar()

        if user != None and playlist != None:
            newMusic = Music(name=music.name, playlist_id=playlist.id)
            session.add(newMusic)
            session.commit()
        return {"message": f"música {music.name} adicionada a playlist {playlist.name} do usuário {user.name}"}
    except Exception as e:
        if 'NoneType object has no attribute':
            raise HTTPException(status_code=400, detail="Playlist não encontrada para esse usuário!")
        

@app.post("/api/post/createPlaylist")
def createPlaylist(playlist: PlaylistModel):
    session = getSession()

    # Tentar buscar o usuário pelo nome
    try:
        user = session.execute(select(User).where(User.name == playlist.user_id)).scalar()
        dbPlaylist = session.execute(select(Playlist).where(Playlist.name == playlist.name).where(Playlist.user_id == playlist.user_id)).scalar()
        
        if user is None:
            user = User(name=playlist.user_id)
            session.add(user)
        
        if dbPlaylist is not None:
            # Lançando uma exceção HTTP com status 400 (Bad Request) e a mensagem de erro
            raise HTTPException(status_code=400, detail="Playlist com o mesmo nome já pertence a esse usuário!")
        
        newPlaylist = Playlist(name=playlist.name, user_id=playlist.user_id)
        session.add(newPlaylist)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar a playlist: {str(e)}")

    # Adicionar a playlist ao banco de dados
    session.add(newPlaylist)

    try:
        session.commit()
        return {"message": f"Playlist {playlist.name} criada com sucesso!"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar a playlist: {str(e)}")
