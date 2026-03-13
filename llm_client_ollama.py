import logging
import ollama
from ollama import ChatResponse
import llm_output_processor


# Processing using Ollama LLM locally.
# prompt (parameter) is used at an elevated state to contextualize the text (parameter) given
def process_ollama(prompt: str, text: str, json_schema_param, model):
    try:
        core_schema = json_schema_param.get("schema", json_schema_param)

        response: ChatResponse = ollama.chat(
            model=model,
            messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            },],
            format=core_schema,
            options={
                "temperature": 0,
                "num_predict": 300
            }
        )
        if not response.done:
            logging.warning("Ollama did not finish: " + response.done_reason + " Text: " + text)

        logging.info("Ollama response: " + str(response.message.content))
        processed_json = llm_output_processor.extract_json(response.message.content)
        return processed_json

    except Exception as e:
        logging.error(e)
        raise e