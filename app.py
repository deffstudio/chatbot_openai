import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']=os.getenv('LANGCHAIN_PROJECT')

## Pormpt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    llm=ChatOpenAI(model=llm,openai_api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

## Title of the app
st.title("Enhanced Q&A Chabto with OpenAI")

## Sidebar for settings
st.sidebar.title("Settings")
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

api_key = st.sidebar.text_input("Enter your Open AI API Key:", type="password", value=st.session_state['api_key'])
st.session_state['api_key'] = api_key

## Drop down to select various Open AI models
llm=st.sidebar.selectbox("Select an Open AI Model", ["gpt-4o","gpt-4-turbo","gpt-4"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperatur", min_value=0.0, max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens", min_value=50, max_value=300,value=150)

## Main interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response = generate_response(user_input, st.session_state['api_key'], llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")