import os
from dotenv import load_dotenv

import streamlit as st
import streamlit.components.v1 as components

from databricks.sdk import WorkspaceClient

st.set_page_config(
    page_title="Databricks Billing",
    page_icon="📊",
    layout="wide",
    menu_items={}
)

st.markdown(
    """
        <style>
            [data-testid="stDecoration"] {
                display: none;
            }
            .stAppHeader {
                background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
                visibility: visible;  /* Ensure the header is visible */
            }

            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }

            [data-testid="stSidebar"][aria-expanded="true"]{
                min-width: 500px;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

def clear_chat_history():
    st.session_state.messages = []

# Set up the chat configuration
load_dotenv()
w = WorkspaceClient()
client = w.serving_endpoints.get_open_ai_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_avatar  = {
    "user": ":material/person:",
    "assistant": "✨",
    "genie": ":material/table_view:"
}


# Chat in Streamlit Sidebar
with st.sidebar:
    col_l, col_r = st.columns([0.9, 0.1], vertical_alignment="bottom")
    col_l.title("Billing AI Assistant")
    col_r.button(":material/refresh:", on_click=clear_chat_history, help="Clear chat history")

    chat_window = st.container(height=800)

    for message in st.session_state.messages:
        role = message["role"]
        with chat_window.chat_message(name=role, avatar=chat_avatar[role]):
            st.write(f"**{role.capitalize()}**")
            st.write(message["content"])

    if prompt := st.chat_input("Ask something.."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_window.chat_message(name="user", avatar=chat_avatar["user"]):
            st.write("**User**")
            st.write(prompt)

        with chat_window:
            with st.spinner("Thinking..", show_time=True):
                response = client.chat.completions.create(
                    model="agents_main-billing-billing_agent",
                    messages=[
                        {
                            "role": m["role"] if m["role"] == "user" else "assistant",
                            "content": m["content"]
                        }
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

        for chunk in response:
            if chunk.delta.get("name") == "Genie":
                role = "genie"
            elif not chunk.delta.get("name"):
                role = "assistant"
            else:
                continue
            
            with chat_window.chat_message(name=role, avatar=chat_avatar[role]):
                st.write(f"**{role.capitalize()}**")
                st.write(chunk.delta["content"])
            st.session_state.messages.append({"role": role, "content": chunk.delta["content"]})

st.title("Databricks Billing Dashboard")
st.markdown("Effortlessly monitor your Databricks usage and costs with the **Billing Dashboard**, complemented by an **Billing AI Assistant** ready to address all your billing-related questions.")

# Databricks Dashboard Ebbedding
dashboard_url = "https://adb-922119294322318.18.azuredatabricks.net/embed/dashboardsv3/01f020ddcaef173d83c74386d1319b26"
components.iframe(dashboard_url, height=800)
