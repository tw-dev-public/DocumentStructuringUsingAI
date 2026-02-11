Document Structuring Using AI
___
This tool categorizes input files with varied and unpredictable data, typically associated with human responses.
Leveraging AI, automates what would typically a tedious and time-consuming step for humans or complex algorithms
with excessive development.
___

Design Tradeoffs
Using LLMs currently has inherent drawbacks. In this circumstance, unreliability would be a significant concern.
This is largely mitigated by using JSON schema validation to check if the response from the LLM is reasonable, or if it ran into any
major errors that prevented its completion. If it fails this check, it its attempted until the response can be validated
or it reaches the maximum number of attempts (specified in config.yaml). Error and warning logging allows the user to see exactly 
which files and how many, if any, resulted in errors for troubleshooting. With these checks and logging in place, the user can
feel much more confident using this powerful technology.

___

Input Files
     ↓
Processor
     ↓
LLM Client
     ↓
Validator
     ↓
Output CSV + Logs


Example:
Input:
"John Doe: My computer has become sentient" (as .txt file)

Output:
fields: (as .csv file)
"user_name"
"message_type"
"priority"

___


Possible future upgrades:

GUI - depending on target users

Increase filetype compatibility (JSON) and varying folder structure

Query multiple models on failure in sequence depending on (specified?) model priority - This could increase tool 
reliability by switching to another LLM after failing to receive appropriate data from the first.

Asynchronous processing - can significantly increase processing speeds in the event of a large number of files

Upgrade OpenAI dialogue to "Responses" - depending on target model and performance potential

More specific response validation including empty fields or nonsensical values.

LLM processing time limits - prevent waiting an excessive amount of time for a single file, when skipping or retrying
may be more efficient

Check for files already existing in output folder to prevent overwriting or mixing data.

Allow user editing/modification of parameters including the JSON schema, the elevated LLM_PROMT, attempts, etc.

More precise priority determination with standardization 