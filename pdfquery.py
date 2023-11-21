from langchain.document_loaders import PyPDFium2Loader
from decouple import config
import os
import time
import openai
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI


openai.api_base = config('OPENAI_API_BASE')
openai.api_type = "azure"
openai.api_version = config('OPENAI_API_VERSION')
openai.api_key = config('OPENAI_API_KEY')

supabase_url = config('SUPABASE_URL')
supabase_key = config('SUPABASE_SERVICE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(deployment="chaining",
                              openai_api_version=config('OPENAI_API_VERSION'),
                              openai_api_key = config('OPENAI_API_KEY'),
                            openai_api_base=config('OPENAI_API_BASE'),
                            openai_api_type="azure",)

# Initialize text splitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

llm = AzureOpenAI(temperature=0.0,
                  model_name="gpt-35-turbo-instruct",
                  openai_api_version=config('OPENAI_API_VERSION'),
                  openai_api_key = config('OPENAI_API_KEY'),
                deployment_name="lang-chain",)

path = f'./files/'

files = []

def write_to_supabase(vector_store, docs):
    retries = 3
    for _ in range(retries):
        try:
            vector_store.from_documents(docs, embeddings, client=supabase, table_name=f"gdpr".lower(), query_name=f"gdpr_match_documents".lower())
            
            #vector_store.from_documents(docs, embeddings, client=supabase, table_name=f"ethicspdfs".lower(), query_name=f"ethicspdfs_match_documents".lower())
            break
        except TimeoutError:
            time.sleep(5)  # Wait for 5 seconds before retrying


def uploadFile (filepath = path):
    for dirpath, dirnames, filenames in os.walk(filepath):
        vector_store = SupabaseVectorStore(client=supabase, embedding=embeddings, table_name=f"gdpr", query_name=f"egdpr_match_documents",)
        
        #vector_store = SupabaseVectorStore(client=supabase, embedding=embeddings, table_name=f"ethicspdfs", query_name=f"ethicspdfs_match_documents",)
        for filename in filenames:
            if filename.endswith('.pdf'):
                try:
                    files.append(os.path.join(dirpath, filename))
                    loader = PyPDFium2Loader(os.path.join(dirpath, filename))
                    data = loader.load()
                    docs = text_splitter.split_documents(data)
                    write_to_supabase(vector_store, docs)
                except:
                    continue

# generate a response
def generate_response(prompt):
    #vector_store = SupabaseVectorStore(client=supabase, embedding=embeddings, table_name=f"gdpr", query_name=f"gdpr_match_documents",)
    
    vector_store = SupabaseVectorStore(client=supabase, embedding=embeddings, table_name=f"ethicspdfs", query_name=f"ethicspdfs_match_documents",)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())
    response = qa.run(f'{prompt}')
    return response