from dotenv import load_dotenv
import os
import streamlit as st
from datetime import date
import json

from services.db_service import insert_transaction, fetch_recent_transactions

load_dotenv()

st.set_page_config(page_title="Finance AI", layout="centered")

st.title("💸 Finance AI – V1")

@st.dialog("AI Suggs")
def ai_confirmation_dialog():
    st.header("🤖 AI Suggested Categorization")

ai_confirmation_dialog()