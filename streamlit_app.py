# streamlit_app.py

import streamlit as st
import os
import sys
import time

# --- Setup and Initialization ---
# Add the project root to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from dotenv import load_dotenv
load_dotenv() # Load .env file

from router.router import QueryRouter
from models.response import QueryResponse

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic LLM Routing System",
    page_icon="⚡",
    layout="wide"
)

# --- Application State ---
# Initialize the router once and store it in the session state.
if 'router' not in st.session_state:
    st.session_state.router = QueryRouter()

# --- Main UI ---
st.title("⚡ Dynamic LLM Routing System")
st.markdown("Ask a question and the system will route it to the most appropriate model.")

# Use a form for the main query input.
with st.form(key="query_form"):
    user_query = st.text_area(
        "Your Question:",
        height=100,
        placeholder="e.g., What is the capital of France? or Explain quantum computing."
    )
    submit_button = st.form_submit_button(label="Process Query")

# --- Processing and Display ---
if submit_button and user_query:
    # Show a spinner during processing.
    with st.spinner("Routing query and generating response..."):
        start_time = time.time()
        
        # The core call to your router.
        result: QueryResponse = st.session_state.router.route_query_and_return_response(user_query)
        
        elapsed_time = time.time() - start_time

    # --- Display Results ---
    st.subheader("System Analysis")
    
    # Display metrics in columns.
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Complexity", result.complexity.capitalize())
    col2.metric("Final Model", result.model_name)
    col3.metric("From Cache", "Yes" if result.cached else "No")
    col4.metric("Execution Time", f"{elapsed_time:.2f}s")

    st.subheader("Response")
    st.success(result.response)

    # Optional: Display the raw response object for debugging.
    with st.expander("Show Raw Result Object"):
        st.json(result.to_dict())

