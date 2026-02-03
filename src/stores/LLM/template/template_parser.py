import os
import logging


class TemplateParser:

    def __init__(self, language: str = None, default_language:str = 'en'):

        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None
        self.logger = logging.getLogger(__name__)

        if language:
            self.set_language(language)
        else:
            self.language = default_language

    
    def set_language(self, language: str):
        if not language:
            self.language = self.default_language
            return 
    
        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.logger.warning(f"Language {language} not found. Falling back to {self.default_language}")
            self.language = self.default_language

    
    def get(self, group: str, key: str, vars: dict={}):

        if not group or not key :
            return None
        
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py" )
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            self.logger.error(f"Template group {group} not found in {targeted_language}")
            return None
        
        # Construct module path: stores.LLM.template.locales.{updated_language}.{group}
        # Note: We don't include .py in the module name
        module_name = f'stores.LLM.template.locales.{targeted_language}.{group}'
        
        try:
            module = __import__(module_name, fromlist=[group])
        except ImportError as e:
            self.logger.error(f"Failed to import template module {module_name}: {e}")
            return None
        
        if not module :
            return None
        
        key_attribute = getattr(module, key, None)
        if not key_attribute:
             self.logger.error(f"Key {key} not found in {module_name}")
             return None

        if hasattr(key_attribute, 'substitute'):
            return key_attribute.substitute(vars)
        else:
            return str(key_attribute)
