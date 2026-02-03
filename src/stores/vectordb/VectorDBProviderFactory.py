from .provider.QdrantDBProvider import QdrantDBProvider
from .provider.PGVectorProvider import PGVectorProvider
from .VectorDBenums import VectorDBenums
from controllers.BaseController import BaseController
from sqlalchemy.orm import session


class VectorDBProviderFactory:

    def __init__(self, config, db_client:session = None):
        self.config = config
        self.db_client = db_client
        self.base_controller = BaseController()

    def create(self, provider: str):

        qdrant_db_client = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
        if provider.lower() == VectorDBenums.QDRANT.value:
            return QdrantDBProvider(
                qdrant_db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE
            )
        if provider.lower() == VectorDBenums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD
            )
        return None
        
        

    
 