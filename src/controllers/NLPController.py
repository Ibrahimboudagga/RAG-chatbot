from .BaseController import BaseController
from models.db_schemes import Project, DataChunk 
from typing import List
from stores.LLM import DocumentTypeEnums
import json
import logging




class NLPController(BaseController):

    def __init__(self, vectordb_client,  generation_client, embedding_client, template_parser):
        super().__init__()


        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.vectordb_client = vectordb_client
        self.template_parser = template_parser
        self.logger = logging.getLogger('uvicorn.error')

    def create_collection_name( self, project_id: str):
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name = collection_name)
    
    async def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name = collection_name)
        return json.loads( json.dumps(collection_info, default = lambda x: x.__dict__))
    
    async def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                chunk_ids: List[int] ,do_reset: bool = False):
        
        # stap1 get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2 manage items
        # step2 manage items
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        
        vectors = []
        batch_size = 90

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_vectors = self.embedding_client.embed_batch(
                texts=batch_texts,
                document_type=DocumentTypeEnums.DOCUMENT.value
            )
            if batch_vectors:
                vectors.extend(batch_vectors)
            else:
                # Handle error or break loop if critical
                self.logger.error(f"Error embedding batch {i // batch_size + 1}")
                return False
        # step3 create collection if not exists

        _ = await self.vectordb_client.create_collection(
                    collection_name = collection_name,
                    embedding_size = self.embedding_client.embedding_size,
                    do_reset = do_reset
        )

        # step 4 insert into vector db
        _ = await self.vectordb_client.insert_many(
                collection_name = collection_name,
                texts = texts,
                metadata = metadata,
                vectors = vectors,
                record_ids = chunk_ids,
        )

        return True

    async def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        query_vector = None
        # step1 get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)
        self.logger.info(f"Searching in collection: {collection_name}")

        # step2 get text embedding vector
        vector = self.embedding_client.embed_text(text = text, document_type = DocumentTypeEnums.QUERY.value)

        if not vector or len(vector) == 0:
            self.logger.error("Embedding generation failed (vector is empty/None)")
            return False
        
        self.logger.info(f"Vector generation successful, length: {len(vector)}, type: {type(vector)}")
        if isinstance(vector, list) and len(vector) > 0:
            query_vector = vector[0]
            self.logger.info(f"Extracted query_vector, length: {len(query_vector) if isinstance(query_vector, list) else 'not a list'}, type: {type(query_vector)}")
        else:
            query_vector = vector
            self.logger.info(f"Using vector directly as query_vector")
        
        # step3 do semantic search
        self.logger.info(f"Calling search_by_vector for collection {collection_name}")
        results = await self.vectordb_client.search_by_vector(
            collection_name = collection_name,
            vector = query_vector,
            limit = limit
        )

        self.logger.info(f"Search results: {results}")
        if not results :
            self.logger.warning("Vector search returned no results")
            return False


        return results
    
    async def answer_rag_question(self, project: Project, query: str, limit: int = 10):

        retreive_doc = await self.search_vector_db_collection(
            project=project,
            text = query,
            limit = limit
        )
        answer, full_prompt, chat_history = None, None, None
    
        if retreive_doc is None or len(retreive_doc) == 0:
            return answer, full_prompt, chat_history

        system_prompt = self.template_parser.get("rag", "system_prompt")
        document_prompts = []

        for idx, doc in enumerate(retreive_doc):

            document_prompts.append(

                self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx +1,
                    "chunk_text": doc.text,
                })
            )

        footer_prompt = self.template_parser.get("rag", "footer_prompt")
        chat_history = [self.generation_client.construct_prompt(
            prompt = system_prompt,
            role = self.generation_client.enums.SYSTEM.value
        )]

        full_prompt = "\n\n".join(document_prompts + [footer_prompt])
        answer = self.generation_client.generate_text(
            prompt = full_prompt,
            max_output_tokens = 1000,
            chat_history = chat_history,
        )

        return answer, full_prompt, chat_history







        
    

    

    
    
