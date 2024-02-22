import sys
import argparse
from os.path import dirname, abspath

import openai
import tiktoken

sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))

from src.settings import Settings
from src.completion_modules.base import BaseCompletion
from src.completion_modules.translation.prompt import translator_prompt

class Translator(BaseCompletion):
    '''
    Class for the translator completion.
    Inherits from BaseCompletion.

    Attributes:
    - input_lang (str): The input language.
    - output_lang (str): The output language.
    - output (str): The output of the completion.

    Methods:
    - run(text_to_translate: str) -> str: Run the completion and return the result.
    '''
    def __init__(self, input_lang: str, output_lang: str) -> None:
        self.input_lang = input_lang
        self.output_lang = output_lang
        self.output = ""
        self.segments_length = None

    def run(self, text_to_translate: str, context:str=None) -> str:
        '''
        Run the completion and return the result.

        Parameters:
        - text_to_translate (str): The text to translate.
        - context (str, default=None): The context for the translation.

        Returns:
        - output (str): The output of the completion.
        '''
        # Check Max Tokens and split the text if it exceeds the limit
        tokenizer = tiktoken.encoding_for_model(Settings.OPENAI_MODEL)
        prompt_tokens = len(tokenizer.encode(
            translator_prompt(self.input_lang, self.output_lang, context)
        ))
        # half for prompt and half for completion
        max_tokens = (Settings.OPENAI_MAX_TOKENS - prompt_tokens) // 2
        if len(text_to_translate) > max_tokens:
            segments = [text_to_translate[i:i+max_tokens] \
                                 for i in range(0, len(text_to_translate), max_tokens)]
        else:
            segments = [text_to_translate]
        self.segments_length = len(segments)

        # Run the completion for each part of the text
        for text in segments:
            prompt = translator_prompt(self.input_lang, self.output_lang, context)
            response = openai.chat.completions.create(
                model=Settings.OPENAI_MODEL,
                messages=[{"role": "system", "content": prompt},
                          {"role": "user", "content": text}],
                max_tokens=max_tokens,
                temperature=Settings.OPENAI_TEMPERATURE
            )
            self.output += response.choices[0].message.content
        return self.output

def main():
    '''
    Main function for testing or running the translator completion at command line.
    '''
    from os.path import dirname
    parser = argparse.ArgumentParser(description='Translate text using OpenAI')
    parser.add_argument(
        '--from',
        dest='input_lang',
        type=str,
        help='Input language i.e. "english"',
        metavar='input_lang',
        required=True,
        nargs='?'
    )
    parser.add_argument(
        '--to',
        dest='output_lang',
        type=str,
        help='Output language code i.e. "portuguese"',
        metavar='output_lang',
        required=True,
        nargs='?'
    )
    parser.add_argument(
        '--txt_path',
        type=str,
        help='Path to the text file (.txt) to translate',
        required=True,
        nargs='?'
    )
    parser.add_argument(
        '--context',
        type=str,
        help='Context for the translation',
        required=False,
        nargs='?'
    )
    args = parser.parse_args()

    translator = Translator(args.input_lang, args.output_lang)

    # Read the input text
    with open(args.txt_path, 'r', encoding='utf-8') as file:
        text_to_translate = file.read()

    translated_text = translator.run(text_to_translate, args.context)

    # Write the translated text to a file
    with open(
        f'{dirname(args.txt_path)}/{args.output_lang}_translated.txt', 'w',
        encoding='utf-8'
    ) as file:
        file.write(translated_text)

if __name__ == "__main__":
    main()
