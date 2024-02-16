import streamlit as st
import os
from utils import *
import uuid



def main():
    st.title("Custom Chatbot")

    if 'OPENAI_API_KEY' not in st.session_state:
        st.session_state["OPENAI_API_KEY"]=''
    if "unique_id" not in st.session_state:
        st.session_state["unique_id"]=''
    if "bot_ready_flag" not in st.session_state:
        st.session_state["bot_ready_flag"]=''


    # st.sidebar.title("😎🗝️")

    # st.session_state["OPENAI_API_KEY"]=st.sidebar.text_input("Enter your API key?", type="password")
    # os.environ["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"]
    

    st.session_state["unique_id"] = uuid.uuid4().hex
    unique_id = st.session_state["unique_id"]
    os.environ["NAMESPACE"] = unique_id

    files = st.sidebar.file_uploader("Upload your file", type="pdf",accept_multiple_files=True)


    push_doc = st.sidebar.button("Push for bot to learn")
    if push_doc:
        st.session_state["bot_ready_flag"] = False
        # create doc out of provided pdf
        docs = create_docs(files,unique_id)
        global tiny_docs
        tiny_docs = split_docs(docs, chunk_size=500, chunk_overlap=40)

        # creating embeddings
        embedding = get_embeddings()

        with st.spinner("Wait! ChatBot is Learning ✋🏻"):
            push_to_pinecone(tiny_docs, embedding, os.environ.get("NAMESPACE"))
            st.session_state["bot_ready_flag"] = True



    st.subheader("Search Document..🤖")

    global query
    query = st.text_area("Enter query here.. 👇🏻", key='question')

    submit = st.button("Get Answer")

    if submit and st.session_state["bot_ready_flag"]==True:
        if query:
            # text embedding
            embedding = get_embeddings()

            # get similar docs
            with st.spinner("Generating Response"):
                response = get_answer(query, embedding, k=2)

                st.write(response)
            st.success("How was that?")
            
        
        else:
            st.error("You gotta be kidding me.. I really wish I could read your mind")
    elif submit:
        st.error("Provide the document first")
    


if __name__ == "__main__":
    main()
