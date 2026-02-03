from  ..VectorDBinterface import VectorDBinterface
from  ..VectorDBenums import distanceMethodEnum
from qdrant_client import QdrantClient, models
import logging
from typing import List
from models.db_schemes import retreivedocument

class QdrantDBProvider(VectorDBinterface):

    def __init__(self, db_client, default_vector_size: int, distance_method: str, index_threshold: int = 100):

        self.client = None
        self.db_client = db_client
        self.distance_method = None
        self.default_vector_size = default_vector_size

        if distance_method == distanceMethodEnum.COS.value:
            self.distance_method = models.Distance.COSINE

        if distance_method == distanceMethodEnum.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger("uvicorn")
    
    async def connect(self):
        self.client= QdrantClient(path=self.db_client)
    
    async def disconnect(self):
        self.client= None

    async def is_collection_existed(self, collection_name:str) -> bool:
        return self.client.collection_exists(collection_name = collection_name)

    async def list_all_collection(self) -> List:
        return self.client.get_collections()
    
    async def get_collection_info(self, collection_name:str) -> dict:
        try:
            return self.client.get_collection(collection_name = collection_name)
        except Exception as e:
            self.logger.error(f"Error getting collection info for {collection_name}: {e}")
            return None

    async def delete_collection(self, collection_name:str):
        if await self.is_collection_existed(collection_name=collection_name):
            self.client.delete_collection(collection_name = collection_name)
        
    async def create_collection(self, collection_name:str, embedding_size:int,
                           do_reset:bool):
        if do_reset:
            _ = await self.delete_collection(collection_name=collection_name)
        if not await self.is_collection_existed(collection_name=collection_name):
            _ = self.client.create_collection(collection_name=collection_name,
                                       vectors_config = models.VectorParams(
                                           size = embedding_size,
                                           distance = self.distance_method

                                       ))
            return True
        
        return False
    

    async def insert_one(self, collection_name:str, text:str, vector:list,
                   metadata:dict=None, record_id:str = None) -> dict:
        
        if not await self.is_collection_existed(collection_name=collection_name):
            self.logger(f"cannot insert new record to non existed collection {collection_name}")
            return False
        try:
            _ = self.client.upload_points(

                collection_name = collection_name,
                points = [models.PointStruct( 
                            id = record_id,
                            vector=vector,
                            payload = {
                                "text": text,
                                "metadata": metadata
                })]
            )
        except Exception as e:
            self.logger.error(f'error while uploading record {e}')

        return True
    

    async def insert_many(self, collection_name:str, texts:list, vectors:list,
                   metadata:list=None, record_ids:list = None, batch_size:int = 50) -> dict:
        
        if metadata is None : 
            metadata = [None]*len(texts)

        if record_ids is None : 
            record_ids = list(range(0,len(texts)))
        
        for i in range(0, len(texts), batch_size):

            batch_end = i + batch_size
            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [
                models.PointStruct(
                    id = batch_record_ids[x],
                              vector=batch_vectors[x],
                        payload = {
                            "text": batch_texts[x],
                            "metadata": batch_metadata[x]
            })

                for x in range(len(batch_texts))
            ]
            try:
                with open("debug_log.txt", "a") as f:
                    f.write(f"DEBUG: Inserting batch {i} to {batch_end} into {collection_name}\n")
                    f.write(f"DEBUG: First record vector length: {len(batch_records[0].vector)}\n")
                    f.write(f"DEBUG: First record ID: {batch_records[0].id}\n")

                operation_info = self.client.upload_points(
                    collection_name = collection_name,
                    points = batch_records,
                    wait=True 
                )
                with open("debug_log.txt", "a") as f:
                    f.write(f"DEBUG: Upload result: {operation_info}\n")
                    
                print(f"DEBUG: Upload result: {operation_info}")
            except Exception as e:

                self.logger.error(f'error while uploading the record {e}')
                print(f"DEBUG: Error uploading: {e}")
                with open("debug_log.txt", "a") as f:
                    f.write(f"DEBUG: Error uploading: {e}\n")

                return False
            
        return True
    

    async def search_by_vector(self, collection_name:str, vector:list,
                  limit:int = 5) -> dict:
        
        try:
            results =  self.client.query_points(
                collection_name = collection_name,
                query = vector,
                limit = limit
            ).points

            if not results or len(results) == 0:
                return  None
            
            return [

                retreivedocument(**{
                    "score": result.score,
                    "text" : result.payload["text"],

                })

                for result in results
            ]
        except Exception as e:
            self.logger.error(f"Error during vector search in collection {collection_name}: {e}")
            print(f"CRITICAL ERROR in search_by_vector: {e}")
            return None
        



