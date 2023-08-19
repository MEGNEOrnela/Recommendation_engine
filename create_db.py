from cgitb import reset
from dotenv import load_dotenv

load_dotenv()
import json
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import DeepLake


def load_db(dataset_path: str, *args, **kwargs) -> DeepLake:
    db = DeepLake(dataset_path, *args, **kwargs)
    return db

def create_db(dataset_path: str, json_filepath: str) -> DeepLake:
    with open(json_filepath, "r") as f:
        data = json.load(f)

    texts = []
    metadatas = []
    
    for title, lyrics in data.items():
        
        texts.append(lyrics["emotion"])
        metadatas.append(
            {
                "title": title,
                "embed_url": lyrics["embed_url"],
            }
        )
        
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    db = DeepLake.from_texts(texts, embeddings, metadatas=metadatas, dataset_path=dataset_path
    )

    return db


if __name__ == "__main__":
    my_activeloop_dataset_name = "African_songs"
    dataset_path = f"hub://{os.environ['ACTIVELOOP_ORG_ID']}/{my_activeloop_dataset_name}"
    create_db(dataset_path, "data/lyrics_with_spotify_url_and_emotion_old.json")

