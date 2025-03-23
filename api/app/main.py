from fastapi import FastAPI
from sqlalchemy import select
from app.database.schemas.schemas import User, Playlist, Music
from app.database.db.db import getSession
from app.models.playlist import PlaylistModel
from app.models.music import MusicModel
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
    
    # Buscar a playlist do usuário específico
    playlist = session.execute(select(Playlist)
                               .where(Playlist.name == playlistName)
                               .where(Playlist.user_id == userName)
                               ).scalars().first()

    if playlist is None:
        return {"message": f"Playlist {playlistName} for user {userName} not found"}
    
    return playlist

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
        return f'erro: {e}'

from sqlalchemy import and_

@app.post("/api/post/createPlaylist")
def createPlaylist(playlist: PlaylistModel):
    session = getSession()

    try:
        # Buscar o usuário pelo nome
        user = session.execute(select(User).where(User.name == playlist.user_id)).scalars().first()

        # Se o usuário não existir, criar um novo
        if user is None:
            user = User(name=playlist.user_id)
            session.add(user)
            session.commit()  # Salva o usuário no banco para gerar o ID

        # Verificar se já existe uma playlist com o mesmo nome para esse usuário
        dbPlaylist = session.execute(
            select(Playlist).where(and_(Playlist.name == playlist.name, Playlist.user_id == user.name))
        ).scalars().first()

        # Se a playlist já existir, retornar uma mensagem de erro
        if dbPlaylist is not None:
            return {"erro": "Playlist com o mesmo nome já pertence a esse usuário!"}

        # Criar uma nova playlist
        newPlaylist = Playlist(name=playlist.name, user_id=user.name)
        session.add(newPlaylist)

    except Exception as e:
        return {"error": f"Erro ao criar a playlist: {e}"}

    # Adicionar a playlist ao banco de dados
    try:
        session.commit()
        return {"message": f"Playlist {playlist.name} criada com sucesso"}
    except Exception as e:
        session.rollback()
        return {"error": f"Erro ao salvar a playlist: {e}"}
