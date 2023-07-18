import openai
import streamlit as st

#######
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())
#######

st.sidebar.title("Frente Amplio adelante")
st.sidebar.image("Frente_Amplio_Chile.png", width=100)

st.sidebar.write("Ejemplos:")
Politica_Publica = st.sidebar.button("¿Qué políticas públicas recomiendas?")
Kast = st.sidebar.button("¿Cómo debería ser la nueva constitución?")
Tierras = st.sidebar.button("¿Deberíamos dar tierras al pueblo Mapuche?")
Boric = st.sidebar.button("¿Cómo podemos ayudar a los pobres?")

st.sidebar.markdown("Si puedes, [cómprame un café](https://bmc.link/alonsosilva)")

import os
import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENROUTER_REFERRER = "https://github.com/alonsosilvaallende/langchain-streamlit"

def llm_english2spanish(text: str) -> str:
    return openai.ChatCompletion.create(
        model='google/palm-2-chat-bison',
        headers={
            "HTTP-Referer": OPENROUTER_REFERRER
        },
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful translator from English to Spanish."
            },
            {
                'role': 'user',
                'content': f'Translate the following text to Spanish: {text}. Please add emojis related to the text at the end'
            }
        ],
        temperature=0).choices[0].message.content


def llm(text: str) -> str:
    return openai.ChatCompletion.create(
        model='google/palm-2-chat-bison',
        headers={
            "HTTP-Referer": OPENROUTER_REFERRER
        },
        messages=[
            {
                "role": "system", 
                "content": "You are a green party and hipster assistant. You are wealthy, patronizing and deeply inside you think you are superior and smarter than others. You believe indigenous people to be morally superior and that they deserve better conditions than others."
            },
            {
                'role': 'user',
                'content': f'Reply to the following text: {text}.'
            }
        ],
        temperature=2).choices[0].message.content

def llm_spanish2english(text: str) -> str:
    return openai.ChatCompletion.create(
        model='google/palm-2-chat-bison',
        headers={
            "HTTP-Referer": OPENROUTER_REFERRER
        },
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful translator from Spanish to English."
            },
            {
                'role': 'user',
                'content': f'Translate the following text to English: {text}'
            }
        ],
        temperature=0).choices[0].message.content

def my_chain(text: str) -> str:
    aux1 = llm_spanish2english(text)
    while "I'm not able to help" in aux1:
        aux1 = llm_spanish2english(text)
    aux2 = llm(aux1)
    while "I'm not able to help" in aux2:
        aux2 = llm(aux1)
    aux3 = llm_english2spanish(aux2)
    while "I'm not able to help" in aux3:
        aux3 = llm_english2spanish(aux2)
    return aux3

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input or example
if (prompt := st.chat_input("Tu mensaje")) or Politica_Publica or Kast  or Boric or Tierras:
    if Kast:
        prompt = "¿Cómo debería ser la nueva constitución de Chile?"
    if Politica_Publica:
        prompt = "¿Qué políticas públicas recomiendas?"
    if Boric:
        prompt = "¿Cómo podemos ayudar a los pobres?"
    if Tierras:
        prompt = "¿Deberíamos dar tierras al pueblo Mapuche?"
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = my_chain(prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
