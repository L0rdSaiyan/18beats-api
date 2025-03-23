from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import registry, mapped_column, Mapped, relationship

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "Users"
    # Definindo a coluna 'name' como chave primária
    name: Mapped[str] = mapped_column(String, primary_key=True)

    # Relacionamento de um-para-muitos com Playlist
    playlists: Mapped[list["Playlist"]] = relationship("Playlist", back_populates="user", default_factory=list)

@table_registry.mapped_as_dataclass
class Playlist:
    __tablename__ = "Playlists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(255))

    # Chave estrangeira para User (um usuário pode ter várias playlists)
    user_id: Mapped[str] = mapped_column(ForeignKey("Users.name"))

    # Relacionamento de muitos-para-um com User
    user: Mapped["User"] = relationship("User", back_populates="playlists", init=False)

    # Relacionamento de um-para-muitos com Music
    musics: Mapped[list["Music"]] = relationship("Music", back_populates="playlist", default_factory=list)

@table_registry.mapped_as_dataclass
class Music:
    __tablename__ = "Musics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(255))

    # Chave estrangeira para Playlist
    playlist_id: Mapped[int] = mapped_column(ForeignKey("Playlists.id"))

    # Relacionamento de muitos-para-um com Playlist
    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="musics", init=False)
