import logging
import processor
import llm_client_ollama
import llm_client_openai
import validator
from pathlib import Path
import pandas as pd
import argparse
import yaml

INPUT_LOCATION = Path('./input')
OUTPUT_LOCATION = Path('./output')

CONFIG_PATH = Path('./config.yaml')


def load_config():
    with open(CONFIG_PATH, "r") as c:
        _config = yaml.safe_load(c)
    return _config


# Switch for model selection
def process_llm(file, model: str = "ollama"):
    _config = load_config()
    match model:
        case "ollama":
            return llm_client_ollama.process_ollama(_config["llm_prompt"], file, _config["json_schema"], _config["ollama_model"])
        case "openai":
            return llm_client_openai.process_openai(_config["llm_prompt"], file, _config["json_schema"], _config["openai_model"])
        case _:
            logging.warning("LLM model not found: "+ model + ". Using ollama as fallback.")
            return process_llm(file)




if __name__ == '__main__':
    config = load_config()

    parser = argparse.ArgumentParser(description='Import, process via LLM, and validate .txt files in the input folder.')
    parser.add_argument("--platform", type=str, default="ollama", help="'ollama' (local) or 'openai' (online) supported")
    args = parser.parse_args()

    files = processor.import_files(INPUT_LOCATION)

    processed_files = []
    errors = []
    for filename, text in files:
        attempts = 0
        while attempts < config["retry_limit"]:
            try:
                llm_return = process_llm(text, args.platform)
                if validator.validate_data(config["json_schema"], llm_return):
                    processed_files.append(llm_return)
                    logging.info(f"Processed file: {filename}")
                    break
                else:
                    attempts += 1
                    logging.warning("File returned from LLM has failed validation. | Attempt "+ str(attempts) + "/" + str(config["retry_limit"]))

            except Exception as e:
                attempts += 1
                logging.warning(str(e) + "| Attempt " + str(attempts) + "/" + str(config["retry_limit"]))
        else:
            logging.error("Maximum number of attempts reached: " + str(filename))
            errors.append(filename)
    try:
        pd.DataFrame(processed_files).to_csv(OUTPUT_LOCATION / "results.csv", index=False)
        logging.info(f"Results saved to: {OUTPUT_LOCATION}/results.csv")
        print(f"Results saved to: {OUTPUT_LOCATION}/results.csv")
    except Exception as e:
        logging.error(e)
    if len( errors) > 0:
        logging.error(str(len(errors)) + " files were skipped due to errors.")

