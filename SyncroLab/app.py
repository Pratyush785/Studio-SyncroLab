import streamlit as st
import google.generativeai as genai

# --- 1. DUAL API CONFIGURATION ---
# Replace these with your actual keys from Google AI Studio
API_KEYS = [
    "AIzaSyCcZaNSiFG_8kW2BiMh5pXv1uPGE0wRmEU", 
    "AIzaSyCHw_KtaldRPkuoeGhavuC3z2As-MPDQ_I"
]

def get_working_model():
    """Tries each API key until one works."""
    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            # Using the most stable 2026 model name
            model = genai.GenerativeModel('gemini-2.5-flash')
            # Test the key with a tiny request
            model.generate_content("ping")
            return model
        except:
            continue # If this key fails, try the next one
    return None

# Initialize the 'Brain'
model = get_working_model()

# --- 2. UI SETUP ---
st.set_page_config(page_title="Studio SyncroLab", page_icon="♾️")
st.title("♾️ Studio SyncroLab: Dual-Core AI || Powered by Gemini")
st.caption("Solves any Maths and applied Mathematics problems.")

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. UNIVERSAL SOLVER LOGIC ---
if prompt := st.chat_input("Ask any math or engineering question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            with st.spinner("Solving via active API..."):
                try:
                    response = model.generate_content(f"Solve this math problem step-by-step: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Both keys are currently busy. Error: {e}")
        else:
            st.error("Engine Error: No valid API keys found. Please check your config.")
