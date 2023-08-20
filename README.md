
# Welcome to MeloMood 💿🎵💬

This work was inspired and built upon the great work made [here](https://github.com/FrancescoSaverioZuppichini/FairytaleDJ/tree/main).

This application accepts user input in the form of text or emojis and then offers song recommendations or messages that resonate with their emotions. 
The input text can be in either English or French.

## Description

The following points outline the steps used to achieve the task:
- **Lyric data scraping**: apply web scraping techniques (beautiful soup) to extract lyrical content from songs ( African songs [1](https://afrikalyrics.com/top-lyrics), [2](https://afrikalyrics.com/language/French)).
- **Large Language Model (LLM)**: use LLM with the [Langchain library](https://python.langchain.com/docs/get_started/introduction.html), to generate summarized representations of the lyrics and get a list of emotions for each lyric.
- **Data Storage**: use the ActiveLoop [Deep Lake](https://www.deeplake.ai/) vector store to store all the emotions, metadata, and embeddings.
- **User Input analysis**: the user input is sent to an LLM to get the emotion that matches his feeling.
- **Music Recommendation**: in cases where the user seeks song recommendations,  a cosine similarity search is performed between the encoded user emotions and those stored in the -database. The top 2 songs with the highest similarity scores corresponding to the user's emotion are selected as recommendations.
- **Motivational Message**: for a user interested in motivational messages or advice, his associated emotions pass through an LLM which  provides advice or a motivated message depending on the emotion.


## Setup

1. Clone the repo 
2. create an activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
   ```
3. Install the requirements
```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
   ```
4. Setup the .env file by adding
  ```bash
OPENAI_API_KEY=<OPENAI_API_KEY>
ACTIVELOOP_TOKEN=<ACTIVELOOP_TOKEN>
   ```
5. Test the app
```bash
streamlit run app.py
```

## Demo 😎
https://github.com/MEGNEOrnela/Recommendation_engine/assets/82549028/9530782f-e33e-4bfa-81ea-42511d2def0a

## Note 
In this work, a database containing only 28 lyrics songs was used. Consequently, the LLM's ability is limited to recommend adequate songs for certain emotions.
