import pymongo
import pprint

API_KEY_ASSEMBLYAI = "<your_api_key_here>"
API_KEY_OPENAI = "<your_api_key_here>"
API_KEY_ELEVENLABS = "<your_api_key_here>"
API_KEY_HUGGINGFACE = "<your_api_key_here>"

client = pymongo.MongoClient("your_database_url_here")

db = client['Findonic']
