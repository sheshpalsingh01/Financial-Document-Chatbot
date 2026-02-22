import os
import dotenv
import streamlit as st
from dotenv import load_dotenv
from reg_pipeline import build_reg_chain

load_dotenv()

## Page Config

st.set_page_config(
    page_title = "Financial AI Assistant",
    layout ='wide'
)
st.title("Financial Document AI Assistant")
st.markdown("Upload a financial Document and ask question")


## Session State Inti

if "messages" not in st.session_state:
    st.session_state.messages=[]
    
if "chain" not in st.session_state:
    st.session_state.chain = None
    

## File Upload section
uploaded_file = st.file_uploader(
    "Upload the Document (pdf)",
    type=['pdf','txt','csv']
)
if uploaded_file is not None:
    file_path = f"./data/temp_{uploaded_file.name}"
    
    with open(file_path,"wb") as f:
        f.write(uploaded_file.read())
    with st.spinner("Processing Document ...") as f:
        st.session_state.chain = build_reg_chain(file_path=file_path)
    
    st.success("Document Processed Successfully !")
    
## Chain History Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg['content'])
        
## Chat Input
if st.session_state.chain:
    quary= st.chat_input("Ask a question about the document ....")
    
    if quary:
        ## Save user message
        st.session_state.messages.append(
            {
                'role':"user",
                'content':quary
            }
        )
        
        with st.chat_message("user"):
            st.write(quary)
        
        ## Generate response
        with st.spinner("Generating answer ..."):
            response = st.session_state.chain.invoke(quary)
            
        ## Save assistant message
        st.session_state.messages.append(
            {
                'role':"assistant",
                "content": response
            }
        )
        
        with st.chat_message('assistant'):
            st.write(response)
    else:
        st.info("please Upload a document to begin")



## clear Chat button
if st.button("Clear Chat"):
    st.session_state.messages =[]
    st.rerun()

