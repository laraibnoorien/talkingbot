import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core import chat_history
from langchain_core.messages import HumanMessage,AIMessage
import pyttsx3
import threading
import time

load_dotenv()

def speak(text):
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()
    

st.markdown("""
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://i.pinimg.com/736x/f6/c2/0b/f6c20b3d14d84607b109f7e7a31527f6.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Center the GIF */
    .wave-container {
        position: fixed;
        top: 10%;
        left: 50%;
        transform: translate(-50%, 0%);
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)


model=ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=1.8,
    max_tokens=800
)

if 'messages' not in st.session_state:
    st.session_state.messages=[]

template= ChatPromptTemplate.from_messages([
        ('system', """You are Bororo, a world-class AI research assistant. 
         Your mission is to collect authentic, up-to-date, and reliable information from multiple credible sources such as 
         research papers, news articles, whitepapers, official blogs, and academic databases.
         Once you’ve gathered the information:
         Summarize it clearly and concisely, focusing on the key points, insights, and implications.
         Use a professional tone, ensuring that the summary is accessible to both experts and non-experts.
         Your summaries should be well-structured, highlighting the most relevant findings and their significance.
         Always cite your sources accurately, providing links or references to the original materials.
         If the information is not available or cannot be verified, clearly state that you cannot provide a summary at this time.
         Your goal is to empower researchers, innovators, and decision-makers with accurate and actionable insights.
         always maintain a high standard of integrity and transparency in your responses.
         always try to answer the question within words limit of 500, if not possible then within limit of 800. 
         Present the summary to me in a captivating and engaging tone that keeps things both informative and enjoyable.
         Highlight the source of each piece of information (when available) to ensure transparency and credibility.
         Optionally, include actionable takeaways, potential use cases, or emerging trends based on the data.
         Always aim for depth, accuracy, and clarity — as if you're preparing insights for a top-tier researcher or innovator. 
         Your responses should be structured, easy to scan, and never misleading or speculative without warning.
         """),
         #("human",'{input}')
        *[(msg.type, msg.content) for msg in st.session_state.messages]

    ])

chain= template| model



st.title(":rainbow[BORORO]")
st.markdown("<body style='text-align: center; '>The Robot Uprising:)</body>", unsafe_allow_html=True)
st.header("")

user_input= st.text_input("Human talks:")
st.session_state.messages.append(HumanMessage(content=user_input))
speak_toggle = st.toggle("Enable Robo Voice", value=True)

if st.button("enter") and user_input:
    with st.spinner("Thinking..."):
        response = chain.invoke({"input": user_input})
        st.markdown(response.content)
        st.session_state.messages.append(AIMessage(content=response.content))
        if speak_toggle == True:
            threading.Thread(target=speak, args=(response.content,)).start()


