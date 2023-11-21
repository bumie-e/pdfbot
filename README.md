# pdfbot
This bot was built with Streamlit and Azure OpenAI - gpt3.5 turbo and instruct models

To run,

1. `pip install -r requirements.txt`

2. `streamlit run bot.py`

To customize,

1. Create a Supabase account and create your Postgres database. You can use query samples to generate your own langchain supported vector embeddings database

2. Create the following Azure resources
   a. Azure OpenAI - gpt-turbo for chat, gpt-instruct for embeddings
   b. Azure Language Translator - If you want support for other languages

3. Your configuration file can look like this


``` AZURE_LANGUAGE_KEY = "your API key"
AZURE_LANGUAGE_ENDPOINT = "Deployment url"
AZURE_LANGUAGE_LOCATION = "Deployment location"


SUPABASE_URL = "Your supabase url", you can also see this from the sample curl examples.
SUPABASE_SERVICE_KEY = "Use one of the service keys"

OPENAI_API_KEY = "Azure deployment Key"
OPENAI_API_VERSION = "The version"
OPENAI_API_BASE = "Azure deployment url"

SUPABASE_TABLE_NAME = "Your table name"
SUPABASE_QUERY_NAME = "Your query name"

```


