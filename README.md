# Welcome to MeloMood 💿🎵💬

This work was inspired and built upon the great work made [here](https://github.com/FrancescoSaverioZuppichini/FairytaleDJ/tree/main).

This application accepts user input in the form of text or emojis and then offers song recommendations or messages that resonate with their emotions. 
The input text can be in either English or French.

## Description

The following points outline the steps used to achieve the task:
**Lyric data scraping**: apply web scraping techniques (beautiful soup) to extract lyrical content from songs ( African songs [1](https://afrikalyrics.com/top-lyrics), [2](https://afrikalyrics.com/language/French)).
**Large Language Model (LLM)**: use LLM with the Langchain library, to generate summarized representations of the lyrics and get a list of emotion for each lyric.
**Data Storage**: use the ActiveLoop Deep Lake vector store to store all the emotions, metadata, and embeddings.
**User Input analysis**: the user input is sent to an LLM to get the emotion that matches his feeling.
**Music Recommendation**: in cases where the user seeks song recommendations,  a cosine similarity search is performed between the encoded user emotions and those stored in the database. The top 2 songs with the highest similarity scores corresponding to the user's emotion are selected as recommendations.
**Motivational Message**: for a user interested in motivational messages or advice, his associated emotions pass through an LLM which  provides an advice or motivated message depending on the emotion.


## Setup
1. Clone the repo 
2. create an activate virtual environment
```bash
   ```
3. Install the requirements
```bash
   ```
4. Setup the .env file by adding
  ```bash
   ```
5. Test the app


## Note 
In this work, a database containing only 28 lyrics song was used. Consequently, 
