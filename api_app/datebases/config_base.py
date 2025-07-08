from pymongo import AsyncMongoClient

# Подключение к MongoDB
client = AsyncMongoClient('mongodb://localhost:27017/')
db = client['meeting_app']
users_collection = db['users']
speaker_listener_collection = db['speaker_listener']
lecture_collection = db['lecture']
stream_collection = db["stream"]
conference_collection = db["conference"]