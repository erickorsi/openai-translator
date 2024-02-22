'''
File to load environment variables from .env file and set them in a settings class.
'''
import os
import string
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

class Settings:
    '''
    Class with set environment variables.
    '''
    class MaxTokensMap(Enum):
        '''
        Enum class to set the max tokens for each model.
        '''
        GPT4 = 8192

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.8'))

    punctuation_trans = str.maketrans('', '', string.punctuation)
    OPENAI_MAX_TOKENS = MaxTokensMap[OPENAI_MODEL.upper().translate(punctuation_trans)].value
