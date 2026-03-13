import logging

from jsonschema import validate, ValidationError

def validate_data(check_schema, valid_schema) -> bool:
    try:
        validate(check_schema, valid_schema)
        return True
    except ValidationError as e:
        logging.warning(e)
        return False
