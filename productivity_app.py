import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 1. SETUP ---
st.set_page_config(page_title="Work Manager", layout="wide")
DATA_FILE = "my_tasks.csv"

# Ensure the CSV file exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Task", "Category", "Priority", "Deadline"])
    df.to_csv(DATA_FILE, index=False)

# --- 2. HEADER & LAYOUT ---
st.title("🎯 My personalize task network")

# THIS LINE DEFINES COL1 and COL2 (The order is very important!)
col1, col2 = st.columns([1, 2])

# --- 3. LEFT COLUMN: INPUT FORM ---
with col1:
    st.subheader("➕ Create New Task")
    with st.form("new_task", clear_on_submit=True):
        task_name = st.text_input("Task Description")
        category = st.selectbox("Category", ["Research", "PhD Students", "Family", "English Coaching"])
        priority_level = st.select_slider("Set Priority Level", options=["Low", "Medium", "High"])
        task_date = st.date_input("Deadline", date.today())
        submit_button = st.form_submit_button("Add to List")

    if submit_button and task_name:
        new_data = pd.DataFrame([[task_name, category, priority_level, task_date]],
                                columns=["Task", "Category", "Priority", "Deadline"])
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Task Added!")
        st.rerun()

# --- 4. RIGHT COLUMN: INTERACTIVE LIST ---
with col2:
    st.subheader("📋 Your Current Focus")
    tasks_df = pd.read_csv(DATA_FILE)

    if not tasks_df.empty:
        # Sort so High Priority is at the top
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks_df['sort_idx'] = tasks_df['Priority'].map(priority_order)
        tasks_df = tasks_df.sort_values('sort_idx').drop('sort_idx', axis=1)

        for index, row in tasks_df.iterrows():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**{row['Task']}**")
                st.caption(f"{row['Category']} | Due: {row['Deadline']}")
            with c2:
                color = "🔴" if row['Priority'] == "High" else "🟡" if row['Priority'] == "Medium" else "🟢"
                st.write(f"{color} {row['Priority']}")
            with c3:
                if st.button("Done", key=f"del_{index}"):
                    tasks_df = tasks_df.drop(index)
                    tasks_df.to_csv(DATA_FILE, index=False)
                    st.rerun()
            st.divider()
    else:
        st.info("No tasks! Time for some English practice or family time? 😊")