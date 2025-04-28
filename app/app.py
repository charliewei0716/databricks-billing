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
            .stAppHeader {
                background-color: rgba(255, 255, 255, 0.0);
                visibility: visible;
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

            .stSidebar h1 {
                font-size: 30px;
            }
        </style>
    """,
    unsafe_allow_html=True
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
    col_l, col_r = st.columns([0.87, 0.13], vertical_alignment="bottom")
    col_l.markdown("# Billing AI Assistant")
    col_r.button(":material/refresh:", on_click=clear_chat_history, help="Clear chat history", use_container_width=True)

    chat_window = st.container(height=600)

    for message in st.session_state.messages:
        role = message["role"]
        with chat_window.chat_message(name=role, avatar=chat_avatar[role]):
            st.write(f"**{role.capitalize()}**")
            st.write(message["content"])
            if message.get("ans_from_docs"):
                st.badge("**Answer from Databricks Document**", icon=":material/check:", color="green")

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

        from_docs = False
        for chunk in response:
            if chunk.delta.get("name") == "Genie":
                role = "genie"
            elif not chunk.delta.get("name"):
                role = "assistant"
            else:
                from_docs = True
                continue
            
            with chat_window.chat_message(name=role, avatar=chat_avatar[role]):
                st.write(f"**{role.capitalize()}**")
                st.write(chunk.delta["content"])
                if role == "assistant" and from_docs:
                    st.badge("**Answer from Databricks Document**", icon=":material/check:", color="green")
            
            ans_from_docs = role == "assistant" and from_docs
            st.session_state.messages.append({"role": role, "content": chunk.delta["content"], "ans_from_docs": ans_from_docs})


# Streamlit Title
text_title = (
    "# Databricks "
    "<span style='background: linear-gradient(to right, #dc2424, #4a569d);color:transparent;background-clip:text;'>Billing</span>"
    " Dashboard"
)
test_subtitle = (
    "Effortlessly monitor your Databricks usage and costs with the "
    "<span style='background: linear-gradient(to right, #dc2424, #4a569d);color:transparent;background-clip:text;font-weight:bold;'>Billing Dashboard</span>"
    ", complemented by an "
    "<span style='background: linear-gradient(to right, #dc2424, #4a569d);color:transparent;background-clip:text;font-weight:bold;'>Billing AI Assistant</span>"
    " ready to address all your billing-related questions."
)

st.markdown(text_title, unsafe_allow_html=True)
st.markdown(test_subtitle, unsafe_allow_html=True)


# Databricks Dashboard Ebbedding
dashboard_url = "https://adb-922119294322318.18.azuredatabricks.net/embed/dashboardsv3/01f020ddcaef173d83c74386d1319b26"
components.iframe(dashboard_url, height=800)
