from fastapi import FastAPI
from routes import base
from routes import data 
from routes import nlp
from helpers.config import get_settings
from stores.LLM import LLMProviderFactory
from stores.vectordb import VectorDBProviderFactory
from stores.LLM.template.template_parser import TemplateParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from utils.metrics import setup_metrics




app = FastAPI()
setup_metrics(app)

@app.on_event('startup')
async def startup_span():
    settings = get_settings()
    print(f"DEBUG: VECTOR_DB_BACKEND is set to: '{settings.VECTOR_DB_BACKEND}'")
    postgres_con = f'postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}'
    app.db_engine = create_async_engine(postgres_con)
    app.db_client = sessionmaker(app.db_engine, class_ = AsyncSession, expire_on_commit = False)

    # app.mongo_conn =  AsyncIOMotorClient(settings.MONGODB_URL)
    # app.db_client =  app.mongo_conn[settings.MONGODB_DATABASE]

    llm_factory_provider = LLMProviderFactory(settings)
    vector_factory_provider = VectorDBProviderFactory(config=settings, db_client=app.db_client)

    app.generation_client = llm_factory_provider.create(provider = settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_factory_provider.create(provider = settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID,
                                               embedding_size = settings.EMBEDDING_MODEL_SIZE)
    app.vectordb_client = vector_factory_provider.create(
        provider = settings.VECTOR_DB_BACKEND
    )
    await app.vectordb_client.connect()
    app.template_parser = TemplateParser(
        language = settings.PRIMARY_LANGUAGE,
        default_language=settings.DEFAULT_LANGUAGE
    )
    
@app.on_event('shutdown')
async def shutdown_span():
    await app.db_engine.dispose()
    await app.vectordb_client.disconnect()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)


# Force reload
