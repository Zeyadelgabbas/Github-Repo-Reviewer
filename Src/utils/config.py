import os 
import yaml 

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict , List , Any

from .logger import get_logger

logging = get_logger(__name__)
load_dotenv()

class Config:

    """ Handles configurations for the project """


    def __init__(self,config_path: str = "config.yaml"):

        self.config_path = config_path
        self._config = self._load_config()
        self._validate_config()
 

    def _load_config(self) -> Dict[str,Any]:
        
        try:
            with open(self.config_path,"r") as f:
                return yaml.safe_load(f)
            
        except Exception as e:
            logging.error(f"Error loading config.yaml file : {e}")
            raise e
        
    def _validate_config(self):
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in enviroment variables")
        
    @property
    def openai_api_key(self):
        return os.getenv("OPENAI_API_KEY")
    
    @property
    def github_token(self):
        return os.getenv("GITHUB_TOKEN")
    
    @property
    def model_name(self):
        return os.getenv("MODEL_NAME")
    
    @property
    def temperature(self):
        return os.getenv("TEMPERATURE")
    

    @property
    def max_tokens(self):
        return int(os.getenv("MAX_TOKENS"))
    
    def get(self,key: str):

        keys = key.split(".")
        dic = self._config

        for k in keys:

            if isinstance(dic,dict):
                dic = dic.get(k)

        return dic 


config = Config()     