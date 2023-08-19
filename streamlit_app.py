import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()
import os
from typing import List, Tuple
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document

from create_db import load_db
from utils import weighted_random_sample

st.set_page_config(
    page_title="Recommendation App",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)


st.title('MeloMood 💿🎵💬')
st.markdown(" ")



@st.experimental_memo
def init_resources():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    my_activeloop_dataset_name = 'African_songs'
    dataset_path = f"hub://{os.environ['ACTIVELOOP_ORG_ID']}/{my_activeloop_dataset_name}"
    
    db = load_db(
        dataset_path,
        embedding_function=embeddings,
    )

    Prompt = PromptTemplate(
        input_variables=["user_input"],
        template=Path("prompts/bot_prompt").read_text(),
    )

    motivation_prompt = PromptTemplate(
        input_variables=["emotions"],
        template=Path("prompts/motivation_prompt").read_text(),
    )
    
    llm = ChatOpenAI(temperature=0.0)

    chain = LLMChain(llm=llm, prompt=Prompt)
    motivation_chain = LLMChain(llm=llm, prompt=motivation_prompt)

    return db, chain, motivation_chain



db, chain,motivation_chain = init_resources()

with st.sidebar:
    st.markdown("# Description 🙌")
    st.markdown("---")
    st.markdown("MeloMood uses the text provided by the user to generate emotions.\n \
                Based on these emotions, it suggests either an appropriate song or a comforting message, \
                according to the user's preferences.")


# List of emojis for users to choose from
emojis_list = ["😊","🥰","😎","😥", "😭","😡","🤒","😟",]

# select the input type
input_type = st.selectbox("Select an input type",['Text', 'Emoji'])
if input_type=='Text':
    text_input = st.text_input(
    label="Hi there, How are you doing today?",
    placeholder="Write your text here!")
else:
    text_input = st.selectbox("Hi there, How are you doing today?", emojis_list)


# Create two columns for layout
col1, col2 = st.columns([1, 1])

# Button 1 in the left column
with col1:
    button_1 = st.button("Find a melody! 🎶🎙️")

# Button 2 in the right column
with col2:
    button_2 = st.button("Find a message! 📜")


placeholder_emotions = st.empty()
placeholder = st.empty()


Matches = List[Tuple[Document, float]]


# MAIN FUNCTIONS

def filter_scores(matches: Matches, th: float = 0.8) -> Matches:
    return [(doc, score) for (doc, score) in matches if score > th]

def normalize_scores_by_sum(matches: Matches) -> Matches:
    scores = [score for _, score in matches]
    tot = sum(scores)
    return [(doc, (score / tot)) for doc, score in matches]

def get_song(user_input: str, k: int = 2):
    emotions = chain.run(user_input=user_input)
    matches = db.similarity_search_with_score(emotions, distance_metric="cos", k=k)
    docs, scores = zip(
        *normalize_scores_by_sum(filter_scores(matches, 0.5))
    )
    choosen_docs = weighted_random_sample(
        np.array(docs), np.array(scores), n=2
    ).tolist()
    return choosen_docs, emotions


def set_song(user_input):
    if user_input == "":
        return
    
    user_input = user_input[:120]
    docs, emotions = get_song(user_input, k=2)
    print(emotions)
    songs = []
    with placeholder_emotions:
        st.markdown("Emotions: `" + emotions + "`")
    with placeholder:
        iframes_html = ""
        for doc in docs:
            name = doc.metadata["title"]
            print(f"song = {name}")
            songs.append(name)
            embed_url = doc.metadata["embed_url"]
            iframes_html += (
                f'<iframe src="{embed_url}" style="border:0;height:100px"> </iframe>'
            )

        st.markdown(
            f"<div style='display:flex;flex-direction:column'>{iframes_html}</div>",
            unsafe_allow_html=True,
        )

def set_story(user_input):
    if user_input == "":
        return
    user_input = user_input[:120]
    _, emotions = get_song(user_input, k=2)
    text = motivation_chain.run(emotions=emotions)
    
    with placeholder_emotions:
        st.markdown("Emotions: `" + emotions + "`")
    with placeholder:
        st.markdown(
            f"<div style='display:flex;flex-direction:column'>{text}</div>",
            unsafe_allow_html=True,
        )

if button_1:
    set_song(text_input)

if button_2:
    set_story(text_input)



