import logging

from jsonschema import validate, ValidationError

def validate_data(valid_schema, check_schema) -> bool:
    try:
        validate(valid_schema, check_schema)
        return True
    except ValidationError as e:
        logging.warning(e)
        return False
