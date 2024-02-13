import streamlit as st
import os
#from dotenv import load_dotenv
from utils import *
import uuid

#load_dotenv()

st.title("Custom Chatbot")

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state["OPENAI_API_KEY"]=''

os.environ['HUGGINGFACEHUB_API_TOKEN']=os.environ.get("HUGGINGFACE_TOKEN")

st.sidebar.title("😎🗝️")
st.session_state["OPENAI_API_KEY"]=st.sidebar.text_input("Enter your API key?", type="password")
# st.session_state["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]
file = st.sidebar.file_uploader("Upload your file", type="pdf")


if "unique_id" not in st.session_state:
    st.session_state["unique_id"]=''

st.session_state["unique_id"] = uuid.uuid4().hex
id = st.session_state["unique_id"]


st.subheader("Search Document..")

query = st.text_area("Enter query here..", key='question')

submit = st.button("Get Answer")

if submit:
    if file and query:
        st.write("lookign for:",query)
        directory = f"pdf_files/{id}"
        content = save_pdf_to_directory(file,directory)
        st.write(content)
        
    elif file:
        st.error("Enter the query first")
    elif query:
        st.error("Enter the document first")
    else:
        st.error("You gotta be kidding me.. I really wish I could read your mind")
        
