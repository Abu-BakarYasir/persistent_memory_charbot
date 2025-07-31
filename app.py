import streamlit as st
from openai import OpenAI
import os
from mem0 import MemoryClient
import hashlib
from dotenv import load_dotenv
import json
import tiktoken
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logging for feedback
logging.basicConfig(level=logging.INFO)

# Initialize Groq client
GROK_API_KEY = os.getenv("GROK_API_KEY")

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Initialize mem0.ai client with API key
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
memory = MemoryClient(api_key=MEM0_API_KEY)

# Function to generate a unique user ID based on session
def get_user_id():
    if "user_id" not in st.session_state:
        st.session_state.user_id = hashlib.md5("user@example.com".encode()).hexdigest()
    return st.session_state.user_id

# Function to add user input to memory if it contains important details
def add_to_memory(user_input, user_id):
    important_keywords = ["name", "prefer", "like", "dislike", "birthday", "address", "goal", "plan", "remember", "favorite", "hobby", "interest"]
    if any(keyword in user_input.lower() for keyword in important_keywords) or len(user_input.split()) >= 3:  # Relaxed threshold
        try:
            memory_data = [{"role": "user", "content": user_input}]
            logging.info(f"Attempting to add to memory: {memory_data}")
            response = memory.add(memory_data, user_id=user_id)
            logging.info(f"Memory add response: {response}")
            return response  # Return response for debugging
        except Exception as e:
            logging.error(f"Failed to add memory: {str(e)}")
            st.error(f"Failed to add memory: {str(e)}")
            return None

# Function to check all stored memories (for debugging)
def check_memories(user_id):
    try:
        memories = memory.get_all(user_id=user_id)
        logging.info(f"Retrieved memories: {memories}")
        return [m["memory"] for m in memories] if memories else []
    except Exception as e:
        logging.error(f"Failed to retrieve all memories: {str(e)}")
        st.error(f"Failed to retrieve memories: {str(e)}")
        return []
    

# Function to retrieve relevant memories
def get_relevant_memories(user_input, user_id):
    try:
        memories = memory.search(query=user_input, user_id=user_id, limit=5)
        return [m["memory"] for m in memories] if memories else []
    except Exception as e:
        st.error(f"Failed to retrieve memories: {str(e)}")
        return []

# Function to count tokens using tiktoken
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Compatible with llama3
    return len(encoding.encode(text))

# Function to generate response using Groq LLM
def generate_response(user_input, memories):
    context = "\n".join(memories) if memories else "No relevant memories."
    prompt = f"""
    You are a helpful chatbot. Use the following memories to inform your response, but only if relevant:
    {context}
    
    User input: {user_input}
    
    Respond concisely and naturally, referencing memories only when appropriate.
    """
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Streamlit UI
st.title("💬 Grok Chatbot")
st.markdown("**Chat with the bot and it will remember important details across sessions!**")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

#Sidebar for settings and export
with st.sidebar:
    st.header("Chat Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.feedback = []
        st.success("Chat history cleared!")
    if st.download_button(
        label="Export Chat History",
        data=json.dumps(st.session_state.messages, indent=2),
        file_name="chat_history.json",
        mime="application/json"
    ):
        st.success("Chat history exported!")
    if st.button("Check Stored Memories"):
        memories = check_memories(get_user_id())
        if memories:
            st.write("**Stored Memories:**")
            for mem in memories:
                st.write(f"- {mem}")
        else:
            st.write("No memories found.")

# Calculate total tokens
total_tokens = sum(count_tokens(msg["content"]) for msg in st.session_state.messages)
st.sidebar.markdown(f"**Total Tokens Used:** {total_tokens}")

# Scrollable chat container
with st.container(height=400):
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(
            message["role"],
            avatar="🧑‍💻" if message["role"] == "user" else "🤖"
        ):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍", key=f"thumb_up_{i}"):
                        st.session_state.feedback.append({"message_index": i, "is_positive": True})
                        logging.info(f"Positive feedback for message {i}: {message['content']}")
                        st.success("Thanks for your feedback!")
                with col2:
                    if st.button("👎", key=f"thumb_down_{i}"):
                        st.session_state.feedback.append({"message_index": i, "is_positive": False})
                        logging.info(f"Negative feedback for message {i}: {message['content']}")
                        st.success("Thanks for your feedback!")

# Fixed chat input at the bottom
with st.container():
    user_id = get_user_id()
    if prompt := st.chat_input("What do you want to talk about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        add_to_memory(prompt, user_id)
        memories = get_relevant_memories(prompt, user_id)
        response = generate_response(prompt, memories)

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})