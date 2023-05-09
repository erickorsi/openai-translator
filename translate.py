# -*- coding: utf-8 -*-
"""
Created on Tue May 09 11:52 2023

@author: erickorsi

Translate a document from one language to another.

v. 0.0.1

"""
import os
from pathlib import Path
from enum import Enum

import openai
from docx import Document

openai.api_key = os.getenv("OPENAI_API_KEY")
#----------------------------------------
def translate(doc_path: Path,
              txt_path: Path,
              translated_path: Path,
              origin_lang: str = "en",
              target_lang: str = "pt"
              ) -> str:
    '''
    Translate a document from one language to another.

    Available languages:
        "en" - English
        "pt" - Portuguese
    '''
    # Get the text from the document
    full_text = __get_doc_text(doc_path, txt_path)

    origin_lang = Languages[origin_lang.upper()].value
    target_lang = Languages[target_lang.upper()].value

    # Translate the text
    prompt_system = f"""
The following text is a document in {origin_lang}.

Your task is to translate it to {target_lang}.

While translating, consider the associations between the words and the context of the text.
Maintain the same meaning and style of the text.
Maintain the same structure of the text in order to allow the translation to be saved exactly the same as the original.

Return only the translated text.
    """

    completion_text = []
    for text in full_text:
        prompt_user = f"""
Text to be translated:

'''
{text}
'''
        """

        completion = __get_completion(prompt_system, prompt_user)
        print(completion)
        completion_text.append(completion)

    # Save the translated text to a txt file
    with open(translated_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("\n\n".join(completion_text))


def __get_doc_text(doc_path: Path,
                   txt_path: Path) -> str:
    '''
    Get the text from a document.
    Saves the text to a txt file.
    '''
    with open(doc_path, "rb") as doc_file:
        doc = Document(doc_file)
        # For reading over connection or streaming
        #source_stream = StringIO(f.read())
    #doc = Document(source_stream)

    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    # Save the text to a txt file
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("\n\n".join(full_text))

    return full_text


def __get_completion(prompt_system, prompt_user, model="gpt-4"):
    '''
    Get the completion of a prompt from the OpenAI API.
    '''
    messages = [{"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


class Languages(Enum):
    '''
    Languages available for translation.
    '''
    PT = "portuguese"
    EN = "english"
