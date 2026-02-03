from ..LLMinterface import LLMInterface
from ..LLMenums import OpenAIEnums
from openai import OpenAI
import logging
from typing import List, Union


class OpenAIPrivider(LLMInterface):

    def __init__(self, api_key:str, api_url:str = None, 
                        default_input_self_character:int = 1000,
                        default_generation_max_output_token:int = 1000,
                        default_generation_temperature:float = 0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_self_character = default_input_self_character
        self.default_generation_max_output_token = default_generation_max_output_token,
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
                    api_key = self.api_key,
                    base_url = self.api_url if self.api_url and len(self.api_url) > 0 else None
        )

        self.enums = OpenAIEnums
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
            self.logger.error("Openai client was not set")
            return None
        if not self.model_id:
            self.logger.error("text generation model for openai was not set")
            return None
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_token
        temperature = temperature if temperature else self.default_generation_temperature
        chat_history.append(self.construct_prompt(prompt = prompt, role = OpenAIEnums.USER.value))

        response = self.client.chat.completion.create(
            model = self.generatin_model_id,
            message = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature

        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("error while generating text with OpenAI")
            return None
        
        return response.choices[0].message.content

        
    
    def embed_text(self, text: Union[str, List[str]], document_type:str = None):
        
        if not self.client:
            self.logger.error("Openai client was not set")
            return None

        if isinstance(text, str):
            text = [text]
        if not self.embedding_model_id:
            self.logger.error("embedding model for openai was not set")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text,
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("error while ebedding text with OpenAI")
            return None
        
        return [rec.embedding for rec in response.data]
    
    def embed_batch(self, texts:list[str], document_type:str = None):
        
        if not self.client:
            self.logger.error("Openai client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("embedding model for openai was not set")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = [self.process_text(text) for text in texts],
        )

        if not response or not response.data or len(response.data) == 0:
            self.logger.error("error while ebedding text with OpenAI")
            return None
        
        return [data.embedding for data in response.data]
    
    def construct_prompt(self, prompt:str, role:str):

        return {
            "role" : role,
            "content" : self.process_text(prompt)
        }





    

    


