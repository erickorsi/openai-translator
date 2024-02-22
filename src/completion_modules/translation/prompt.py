def translator_prompt(
        input_lang: str,
        output_lang: str,
        context: str = None
    ) -> str:
    '''
    Generate a prompt for the translator task.

    Parameters:
    - input_lang (str): The input language.
    - output_lang (str): The output language.

    Returns:
    - prompt (str): The generated prompt.
    '''

    prompt = f"""You are a translator and text reviewer.
You have been given a task to translate a text from {input_lang} to {output_lang}.

Make sure to not miss any details and translate the text as accurately as possible,
as a native speaker would do, and keep the context in mind.
Maintain the same tone and style of the text in the translation, as well as any formatting.

Proof read the translated text and make sure it is accurate and makes sense before submitting it.
Revise the translated text and make any necessary changes to improve it, as if it were initially written in that language.
"""

    if context:
        prompt += f"\n\nText context: {context}"
    return prompt
