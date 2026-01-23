from dotenv import load_dotenv
import os
import streamlit as st
from datetime import date
import json

from services.db_service import insert_transaction, fetch_recent_transactions

load_dotenv()

st.set_page_config(page_title="Finance AI", layout="centered")

st.title("💸 Finance AI – V1")

if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

if "show_ai_dialog" not in st.session_state:
    st.session_state.show_ai_dialog = False

if "override_ai" not in st.session_state:
    st.session_state.override_ai = False


@st.dialog("AI Suggs")
def ai_confirmation_dialog():
    from crew.crew import run_categorization

    with st.spinner("Analyzing with AI..."):
        agent_result = run_categorization({"description": txn_description, "amount": txn_amount})
        try:
            st.session_state.ai_result = json.loads(agent_result)
            st.session_state.show_ai_dialog = True
            
        except json.JSONDecodeError:
            st.error("AI response could not be parsed")
            st.text(agent_result)
        
        st.write("AI has suggested the following details:")
        ai = st.session_state.ai_result

        st.markdown(f"**Type:** {ai['type']}")
        st.markdown(f"**Category:** {ai['category']}")
        st.markdown(f"**Sub Category:** {ai.get('sub_category', 'N/A')}")
        
        st.divider()

        st.write("Do you want to confirm and save this transaction?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancel, Manual Override"):
                st.session_state.override_ai = True
                    
        with col2:
            if st.button("Save Transaction"):
                insert_transaction({
                    "date": txn_date.isoformat(),
                    "amount": txn_amount,
                    "type": st.session_state.ai_result["type"],
                    "category": st.session_state.ai_result["category"],
                    "sub_category": st.session_state.ai_result.get("sub_category"),
                    "description": txn_description,
                    "confidence": st.session_state.ai_result.get("confidence")
                })
                st.success("Transaction Added Successfully")
                st.session_state.show_ai_dialog = False
                st.session_state.ai_result = None


entry_mode = st.radio(
    "Select Entry Mode",
    ("Manual Entry", "AI Assisted Entry"),
    horizontal=True
)
if entry_mode == "Manual Entry":
    st.write("Add Manual Transaction")

    st.divider()

    with st.form("add_transaction_form" , clear_on_submit=True, ):

        txn_date = st.date_input(
            "Date",
            value = date.today()
        )

        txn_amount = st.number_input(
            "Amount",
            min_value=0.0,
            value = 0.0,
            step = 1.0
        )

        txn_type = st.selectbox(
            "Type",
            ["expense","income","saving"]
        )

        txn_category = st.text_input(
            "Category",
            placeholder="Food, Rent, Investment..."
        )

        txn_sub_category = st.text_input(
            "Sub Category",
            placeholder="Groceries, Dining, Fixed Deposits..."
        )

        txn_description = st.text_area(
            "Description",
            placeholder="swgy instamrt blr"
        )

        submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if txn_amount <= 0:
            st.error("Transaction Amount must be greater than 0")
    
        elif not txn_category or not txn_description:
            st.error("Category and Description is required")
    
        else:
            insert_transaction({
                "date" : txn_date.isoformat(),
                "amount":txn_amount,
                "type": txn_type,
                "category": txn_category,
                "sub_category": txn_sub_category,
                "description": txn_description,
                "confidence": None
            })

            st.success("Transaction Added Succesfully")

elif entry_mode == "AI Assisted Entry":
    with st.form("ai_assisted_entry_form", clear_on_submit=False):

        txn_date = st.date_input("Date", value=date.today())

        txn_amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=0.0,
            step=1.0
        )

        txn_description = st.text_area(
            "Describe your transaction",
            placeholder="swgy instamrt blr, salary credited, SIP mutual fund"
        )

        analyze = st.form_submit_button("Analyze with AI")

    if analyze:
        if txn_amount <= 0:
            st.error("Transaction Amount must be greater than 0")
    
        elif not txn_description:
            st.error("Description is required")
    
        else:
            st.info("AI analysis feature is under development.")
            ai_confirmation_dialog()            


st.divider()

st.subheader("Recent Transactions")

recent_transactions = fetch_recent_transactions(limit = 10)

if not recent_transactions:
    st.info("No Transactions Found. Please add some transactions.")
else:
    table_data = [
        {
            "Date": row[0],
            "Amount": row[1],
            "Type": row[2],
            "Category": row[3],
            "Sub Category": row[4],
            "Description": row[5],
            "Created At": row[6]
        }
        for row in recent_transactions
    ]

    st.table(table_data)