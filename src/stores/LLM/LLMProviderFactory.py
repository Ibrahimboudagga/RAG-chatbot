from .LLMenums import LLMEnums
from .providers.OpenAIPrivider import OpenAIPrivider
from .providers.CoHereProvider import CoHereProvider



class LLMProviderFactory:
    def __init__(self, config):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIPrivider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPEN_API_URL,
                default_input_self_character=self.config.INPUT_DEFAULT_MAX_CHARACTER,
                default_generation_max_output_token=self.config.GENERATION_DEFAULT_MAX_TOKEN,
                default_generation_temperature=self.config.GENERATION_DEFAULT_MAX_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_self_character=self.config.INPUT_DEFAULT_MAX_CHARACTER,
                default_generation_max_output_token=self.config.GENERATION_DEFAULT_MAX_TOKEN,
                default_generation_temperature=self.config.GENERATION_DEFAULT_MAX_TEMPERATURE
            )

        return None


    
 