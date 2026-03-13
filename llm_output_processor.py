import json
import re

# Despite instructions otherwise, LLMs sometimes still format the data within other formats/structures.
def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise