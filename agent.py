# ========================================
# 1. Install required libraries
# ========================================
# Run in terminal: 
# pip install streamlit transformers langchain wikipedia

# ========================================
# 2. AI Agent Code (save as agent_app.py)
# ========================================
import streamlit as st
from transformers import pipeline
import wikipedia

# Load small model (for demo)
llm = pipeline("text-generation", model="gpt2")

# Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tools
def calculator_tool(expression):
    try:
        result = eval(expression)
        return f"🧮 The result is: {result}"
    except:
        return "❌ Sorry, I couldn't calculate that."

def wikipedia_tool(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"📖 Wikipedia: {summary}"
    except:
        return "❌ Sorry, I couldn't find info on that."

# AI Agent Logic
def ai_agent(user_input):
    # Check for tool commands
    if user_input.lower().startswith("calc:"):
        return calculator_tool(user_input[5:].strip())
    elif user_input.lower().startswith("wiki:"):
        return wikipedia_tool(user_input[5:].strip())
    
    # Otherwise use LLM
    prompt = "User: " + user_input + "\nAgent:"
    response = llm(prompt, max_new_tokens=80, do_sample=True)[0]['generated_text']
    reply = response.split("Agent:")[-1].strip()
    return reply

# Streamlit UI
st.title("🤖Agent")
st.write("Type your question below. Use **calc: 2+2** or **wiki: India** for tools.")

user_input = st.text_input("You:", "")

if user_input:
    reply = ai_agent(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Agent", reply))

# Display chat
for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {text}")
    else:
        st.markdown(f"**🤖 {role}:** {text}")
