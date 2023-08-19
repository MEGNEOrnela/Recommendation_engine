
import openai
import os
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain,SequentialChain

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) #read local .env file



# This is an LLMChain to write a summary given the lyric of a song
llm = OpenAI(temperature=.0)
summary_template = """You are a text summarizer. Given the lyrics of a song, it is your job to write a summary for that lyrics.
Your output should be in english if the lyrics is in english or in french if it's in french, otherwise in english.

lyrics: {song}"""
prompt_template = PromptTemplate(input_variables=["song"], template=summary_template)
summary_chain = LLMChain(llm=llm, prompt=prompt_template)

# This is an LLMChain to get emotions from summary of the song
template = """ Given the summary of a song lyrics, it is your job to produce a list of 5 emotions as comma separated that I will later use to retrieve the song.
Ensure that your output has the same language as the summary.

summary:
{summary}
"""
prompt_template = PromptTemplate(input_variables=["summary"], template=template)
emotion_chain = LLMChain(llm=llm, prompt=prompt_template)


# This is the overall chain where we run these two chains in sequence.
overall_chain = SimpleSequentialChain(
    chains=[summary_chain, emotion_chain],
    verbose=True)


with open(
"data/lyrics_with_spotify_url.json",
"r",
) as f:
    data = json.load(f)

lyrics_emotions = {}

for author, lyrics in data.items():
    for lyric in lyrics:
        print(f"Creating summary for {lyric['title']}")
        emotions = overall_chain.run(lyric["text"])
        print(emotions)
        lyrics_emotions[lyric["title"].lower()] = {
            "emotion": emotions,
            "embed_url": lyric["embed_url"],
        }
        

with open(
    "data/lyrics_with_spotify_url_and_emotion.json",
    "w",
) as f:
    json.dump(lyrics_emotions, f)