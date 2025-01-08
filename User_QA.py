import streamlit as st
import anthropic
import time

####d 01052025
'''
This is a smart assistant demo for https://www.moj.go.jp/isa/
Have a great day! 😊
\nこれは Pony が作成したスマートアシスタントのデモです。素敵な一日をお過ごしください！😊
\nPony AI
'''

# Function to switch language
def switch_language(lang):
    if lang == "日本語":
        return True  # Set language to Japanese
    else:
        return False

# Add the language switch button in the sidebar
with st.sidebar:
    st.title("User View")
    language = st.radio("Language", ("English", "日本語"), index=0)
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")
    
    "[[About](suppport@pony.com)](© 2024 Pony. All rights reserved.)"

# Check if language is set to Japanese
is_japanese = switch_language(language)

# Update title and text based on the selected language
if is_japanese:
    st.title("🖋 ポニー・スマートアシスタント")  # Japanese title
else:
    st.title("🖋 Pony Smart Assistant")

# Load the data file from the directory
data_file_path = "data.txt"
try:
    with open(data_file_path, "r", encoding="utf-8") as file:
        article = file.read()
except FileNotFoundError:
    st.error("Data file 'data.txt' not found in the directory. Please ensure it exists.")
    st.stop()

# Question input box
question_placeholder = "参考のための質問例" if is_japanese else "Example Questions for Reference"
question = st.text_input(
    "質問入力ボックス" if is_japanese else "Question Input Box",
    placeholder=question_placeholder,
)

if question and not anthropic_api_key:
    st.info("Anthropic APIキーを追加してください。" if is_japanese else "Please add your API key to continue.")

if question and anthropic_api_key:
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2",  # "claude-2" for Claude 2 model, claude-3-5-sonnet-latest
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)

# Retry logic
def get_response_with_retry(client, retries=5, delay=2):
    for i in range(retries):
        try:
            response = client.completions.create(
                model="claude-2",  # Use the correct model
                prompt="Your prompt here",
                max_tokens=1000
            )
            return response
        except anthropic.InternalServerError as e:
            print(f"Attempt {i+1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("All retries failed.")
