from ..LLMinterface import LLMInterface
from ..LLMenums import CoHereEnums, DocumentTypeEnums
import cohere 
import logging
from typing import List, Union






class CoHereProvider(LLMInterface):

    def __init__(self, api_key:str,
                        default_input_self_character:int = 1000,
                        default_generation_max_output_token:int = 1000,
                        default_generation_temperature:float = 0.1):
        
        
        self.api_key = api_key

        self.default_input_self_character = default_input_self_character
        self.default_generation_max_output_token = default_generation_max_output_token,
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(
                    api_key = self.api_key
        )

        self.enums = CoHereEnums
        self.logger = logging.Logger(__name__)


    def set_generation_model(self, model_id:str):
        self.model_id = model_id

    def set_embedding_model(self, model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text: str):
        return text[:self.default_input_self_character].strip()


    def generate_text(self, prompt:str, max_output_tokens:int,
                      temperature: float = None, chat_history:list=[]):
        
        if not self.client:
            self.logger.error("cohere client was not set")
            return None
        
        if not self.model_id:
            self.logger.error("text generation model for cohere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens

        )

        if not response or not response.text :
            self.logger.error('error while generating text with cohere')
            return None
        
        return response.text
        

    def embed_text(self, text:Union[str, List[str]], document_type:str = None):
        
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
        
        if isinstance(text, str):
            text = [text]
        if not self.embedding_model_id:
            self.logger.error("embedding model for Cohere was not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnums.QUERY :
            input_type = CoHereEnums.QUERY
        
        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [self.process_text(t) for t in text],
            input_type = input_type,
            embedding_types = ['float']
        )

        if not response or not response.embeddings or not response.embeddings.float or not response.embeddings.float[0]:
            self.logger.error("error while ebedding text with Cohere")
            return None

        return [f for f in response.embeddings.float]

    def embed_batch(self, texts:list[str], document_type:str = None):
        
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("embedding model for Cohere was not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnums.QUERY :
            input_type = CoHereEnums.QUERY
        
        try:
            response = self.client.embed(
                model = self.embedding_model_id,
                texts = [self.process_text(text) for text in texts],
                input_type = input_type,
                embedding_types = ['float']
            )

            if not response or not response.embeddings or not response.embeddings.float:
                self.logger.error("error while ebedding text with Cohere")
                return None

            return response.embeddings.float
        except Exception as e:
            self.logger.error(f"Error embedding batch with Cohere: {e}")
            return None

        
    def construct_prompt(self, prompt:str, role:str):

        return {
            "role" : role,
            "text" : prompt #self.process_text(prompt)
        }
        
    

        




