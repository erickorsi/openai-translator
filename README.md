Translator using OpenAI API.
Made using Python Python 3.10.6

Initial build supports running in command line and requires setting your own OPENAI_API_KEY in the ```.env```.

# Modules

## Translation

Uses LLM model to translate text from a *txt* file and generates another *txt* file with the translated text.
Breaks the text into multiple segments when surpassing the max token limit for the supported model.

### Usage and Testing

Currently only supports usage through command line. Example:

``` cmd
python translator.py --from english --to portuguese --txt_path ./samples/english_examples.txt --context "A set of varied example texts in english."
```
where --context is optional.

Creates a file called ```[output_language]_translated.txt``` in the same directory as the input txt_path.