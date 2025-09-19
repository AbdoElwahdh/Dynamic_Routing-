# app.py
import streamlit as st
from router.router import route_query  # We keep our clean structure

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic LLM Router",
    page_icon="",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.title("Dynamic LLM Router")
    st.markdown("---")
    st.markdown("A smart system that routes queries to the most efficient LLM based on complexity.")
    st.markdown("Developed for the **Namasoft** LLM Task.")

# --- Main UI ---
st.title("Ask the Smart System")

# --- THE SIMPLIFIED AND CORRECT LOGIC ---

# We use a form to group the input and the button.
# This ensures that the app only reruns when the button is clicked.
with st.form(key="query_form"):
    user_query = st.text_area(
        "Your Question:",
        height=100,
        placeholder="e.g., What is the capital of Egypt?"
    )
    submit_button = st.form_submit_button(label="🚀 Process Query")

# This block of code will ONLY run if the submit button inside the form was clicked.
if submit_button and user_query:
    # 1. Show a spinner while the long process is running.
    with st.spinner(" System is thinking... This may take a few minutes..."):
        # 2. Call the actual routing function from our backend.
        # The result is stored in a simple local variable. No complex session state needed here.
        result = route_query(user_query)

    # 3. Once the process is done, display the results.
    st.subheader("System Analysis")

    # Use .get() with a default value to prevent errors if a key is missing.
    route_taken = result.get('route', 'N/A')
    final_model = result.get('final_model', 'N/A')
    exec_time = result.get('execution_time', 0.0)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Route Taken", value=route_taken)
    col2.metric(label="Final Model", value=final_model)
    col3.metric(label="Execution Time", value=f"{exec_time:.2f} s")

    st.subheader(" Response")
    response_text = result.get('response', 'No response received.')
    
    if "Error" in final_model:
        st.error(response_text)
    else:
        st.success(response_text)