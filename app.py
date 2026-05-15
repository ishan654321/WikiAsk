import streamlit as st
import wikipedia
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Wiki Storyteller", page_icon="📚", layout="centered")

st.title(" Wikipedia Rabbit Hole Storyteller ")
st.write("Turn boring Wikipedia facts into highly entertaining stories!")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("Configuration")
    # Taking the API key as a password input keeps it secure and out of your source code!
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.markdown("[Get a free API key here](https://aistudio.google.com/app/apikey)")

# --- MAIN USER INTERFACE ---
topic = st.text_input("Enter a Wikipedia topic:", placeholder="e.g., The Great Emu War, Black Holes")
perspective = st.text_input("Enter a style or perspective:", placeholder="e.g., a grizzled detective, a dramatic movie trailer")

# --- GENERATION LOGIC ---
# This button triggers the code block below it
if st.button("✨ Generate Story", type="primary"):
    
    # 1. Validation checks
    if not api_key:
        st.error(" Please enter your Gemini API Key in the sidebar to continue.")
    elif not topic or not perspective:
        st.warning(" Please fill out both the topic and the perspective!")
    else:
        # 2. Show a loading spinner while the AI thinks
        with st.spinner(f"Fetching facts about '{topic}' and writing your story..."):
            try:
                # Initialize the Gemini client with the user's key
                client = genai.Client(api_key=api_key)
                
                # Fetch Wikipedia data
                wiki_data = wikipedia.summary(topic, auto_suggest=False)
                
                # Construct the prompt
                prompt = f"""
                Here is factual information from Wikipedia about "{topic}":
                {wiki_data}

                Rewrite this information into an entertaining, creative story. 
                You MUST write it using this exact style/perspective: {perspective}.
                Make sure to include the real historical facts, but make it incredibly fun to read.
                """

                # Call the AI model
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=prompt
                )
                
                # Display the result in a nice box
                st.success("Story Generated!")
                st.markdown("### Your AI Story")
                st.write(response.text)

            except wikipedia.exceptions.DisambiguationError as e:
                st.error(f" '{topic}' is too broad. Did you mean one of these? {e.options[:5]}")
            except wikipedia.exceptions.PageError:
                st.error(f" Couldn't find a Wikipedia page for '{topic}'. Try another search.")
            except Exception as e:
                st.error(f" An error occurred with the AI: {e}")