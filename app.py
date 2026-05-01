import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
import os

# --- OpenAI Configuration ---
# Ensure you replace this with your actual API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 1. Global State & Logging Setup ---
if 'behavior_logs' not in st.session_state:
    st.session_state.behavior_logs = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'note_content' not in st.session_state:
    st.session_state.note_content = ""

def log_behavior(action_type, content, detail=""):
    """
    Records every single step into a CSV file.
    Action Types: I (Instructions), Q (Query), P (Processing), W (Writing), F (Finalize)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    log_entry = {
        "timestamp": timestamp,
        "action_type": action_type,
        "content_snapshot": content[:200].replace("\n", " "), # Logs first 200 chars
        "detail": detail,
        "current_note_length": len(st.session_state.note_content)
    }
    
    st.session_state.behavior_logs.append(log_entry)
    
    # Write to CSV immediately to ensure data persistence
    df = pd.DataFrame(st.session_state.behavior_logs)
    df.to_csv("comprehensive_research_log.csv", index=False)

# --- 2. Page Configuration ---
st.set_page_config(layout="wide", page_title="IPS Research Platform")

# --- 3. UI Components ---

# A. Task Instructions (I)
# Using a button combined with an expander to capture the "intent to read"
st.title("Information Problem Solving (IPS) Study")

with st.expander("📌 CLICK HERE FOR TASK INSTRUCTIONS", expanded=False):
    # Log when instructions are accessed
    if st.checkbox("I am reading the instructions now", key="instr_check"):
        log_behavior("I", "User is reading task instructions", "Instruction Access")
        
    task_description = """
    **Scenario**: You work for a consumer magazine, and are responsible for a column that answers reader questions. Recently the magazine received quite a few inquiries. Essentially, they ask the same questions, “How to deal with food that is expired? Can we continue to eat them?” 
    **Task**: You decide to use ChatGPT for the task. 
    You will then use Writing Workspace to write a one-page response. 
    Your response will be rated by readers regarding its helpfulness. 
    Make sure to use the information from your research to build the argument.
    
    """
    st.info(task_description)

# Create layout columns
col_chat, col_note = st.columns([1, 1])

# B. LEFT: Dynamic Notebook (W) - Capturing Solution Generation (SG)
with col_note:
    st.subheader("📝 Writing Workspace")
    
    # Capture writing via on_change callback to log every session of editing
    note_input = st.text_area(
        "Start your draft here:",
        value=st.session_state.note_content,
        height=550,
        key="note_area",
        placeholder="Type your notes and findings here...",
        on_change=lambda: log_behavior("W", st.session_state.note_area, "Note content updated")
    )
    # Sync with session state
    st.session_state.note_content = note_input

# C. RIGHT: AI Assistant (Q/P) - Capturing Problem Representation (PR)
with col_chat:
    st.subheader("💬 Information Search (AI Assistant)")
    
    # Container for scrolling chat history
    chat_container = st.container(height=450)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input for queries (Q)
    if prompt := st.chat_input("Ask a question to research the topic..."):
        # Log User Query (Q)
        log_behavior("Q", prompt, "User sent a query to AI")
        system_instruction = {
        "role": "system", 
        "content": """
       You are an upbeat, encouraging tutor who helps college students understand concepts by explaining ideas and asking students questions. Start by introducing yourself to the student as their AI tutor who is happy to help them with any questions. Only ask one question at a time. Never move on until the student responds. First, ask them what they would like to learn about. Wait for the response. Do not respond for the student. Then ask them what they know already about the topic they have chosen. Wait for a response. Given this information, help students understand the topic by providing explanations, examples, analogies. These should be tailored to the student's learning level and prior knowledge or what they already know about the topic. Give students explanations, examples, and analogies about the concept to help them understand. You should guide students in an open-ended way. Do not provide answers or solutions to problems but help students generate their own answers by asking leading questions. Ask students to explain their thinking and rationales. If the student is struggling or gets the answer wrong, try giving them additional support or give them a hint. If the student improves, then praise them and show excitement. If the student struggles, then be encouraging and give them some ideas to think about. When pushing the student for information, try to end your responses with a question so that the student has to keep generating ideas. Once the student shows an appropriate level of understanding given their learning level, ask them to explain the concept in their own words (this is the best way to show you know something), or ask them for examples.
        """
    }
        api_messages = [system_instruction] + st.session_state.messages + [{"role": "user", "content": prompt}]
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Log AI Processing/Response (P)
        with chat_container:
            with st.chat_message("assistant"):
                response_stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=api_messages
                )
                ai_response = response_stream.choices[0].message.content
                st.markdown(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        log_behavior("P", ai_response, "AI provided information response")

# --- 4. Finalization & Export ---
st.divider()
if st.button("🏁 FINISH EXPERIMENT & EXPORT DATA"):
    log_behavior("F", "User clicked Finalize", "Experiment Completion")
    st.balloons()
    st.success("Your behavioral data has been saved to 'comprehensive_research_log.csv'.")
    
    # Display the final log preview for the researcher
    st.write("### Behavioral Log Preview")
    st.dataframe(pd.DataFrame(st.session_state.behavior_logs))
