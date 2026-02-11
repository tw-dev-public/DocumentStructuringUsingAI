import logging
import os
from openai import OpenAI
from openai.types import ResponseFormatJSONSchema
from openai.types.chat import ChatCompletionDeveloperMessageParam, ChatCompletionUserMessageParam
import llm_output_processor

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# Processing using OpenAI online.
# prompt (parameter) is used at an elevated state to contextualize the text (parameter) given
def process_openai(prompt: str, text: str, json_schema_param, model):
    client = OpenAI(api_key=OPENAI_API_KEY)

    _messages = [
        ChatCompletionDeveloperMessageParam(
            role="developer",
            content=prompt
        ),
        ChatCompletionUserMessageParam(
            role="user",
            content=text
        )
    ]
    _json_response_format = {
                "type":"json_schema",
                "json_schema":json_schema_param
    }
    try:
        response = client.chat.completions.create(
            model=model,
            messages=_messages,
            max_tokens=200,
            response_format = _json_response_format
        )

        # Check if the conversation was too long for the context window, resulting in incomplete JSON
        if response.choices[0].message.refusal == "length":
            logging.warning("OpenAI refused: Conversation was too long for the context window, resulting in incomplete JSON. Text: " + text)
        # Check if the model's output included restricted content, so the generation of JSON was halted and may be partial
        elif response.choices[0].message.refusal == "content_filter":
            logging.warning("OpenAI refused: model's output included restricted content, so the generation of JSON was halted and may be partial. Text: " + text)
        elif response.choices[0].message.refusal == "stop":
            # In this case the model has either successfully finished generating the JSON object according to your schema, or the model generated one of the tokens you provided as a "stop token"
            logging.warning("OpenAI refused: model has either successfully finished generating the JSON object according to your schema, or the model generated one of the tokens you provided as a stop token. Text: " + text)
        elif response.choices[0].message.refusal is not None:
            logging.warning("OpenAI refused the request. Text: " + text + " Response: " + response.choices[0].message.content)

        print("OpenAI response: " + str(response.choices[0].message.content))
        logging.info("OpenAI response: " + str(response.choices[0].message.content))
        processed_json = llm_output_processor.extract_json(response.choices[0].message.content)

        return processed_json


    except Exception as e:
        # logging.error("Processing via OpenAI failed: " + str(e) + "Text: " + text)
        logging.error(e)
        raise e