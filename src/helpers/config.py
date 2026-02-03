from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional, List

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    ALLOWED_FILE_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    # MONGODB_URL : str
    # MONGODB_DATABASE: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str

    GENERATION_BACKEND : str
    EMBEDDING_BACKEND : str

    OPENAI_API_KEY : str = None
    OPEN_API_URL  : str = None
    COHERE_API_KEY  : str = None
    
    GENERATION_MODEL_ID_LITERAL: List['str'] = None
    GENERATION_MODEL_ID  : str = None
    EMBEDDING_MODEL_ID  : str = None
    EMBEDDING_MODEL_SIZE  : Optional[int] = None

    INPUT_DEFAULT_MAX_CHARACTER  : int = None
    GENERATION_DEFAULT_MAX_TOKEN: int = None
    GENERATION_DEFAULT_MAX_TEMPERATURE: float = None

    VECTOR_DB_BACKEND_LITERAL: List['str'] = None
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = None

    DEFAULT_LANGUAGE: str = "en"
    PRIMARY_LANGUAGE: str = "en"

    VECTOR_DB_PGVEC_INDEX_THRESHOLD : int = None


    


    @field_validator("EMBEDDING_MODEL_SIZE", mode="before")
    @classmethod
    def empty_str_to_int(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

def get_settings():
    return Settings()