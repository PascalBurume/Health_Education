import streamlit as st
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AZURE_ENDPOINT_KEY = os.environ['AZURE_ENDPOINT_KEY'] = '2NY3PsD0ZIvY8WuwFxARDL5ohTvGAzaj'

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
# Streamlit UI components
    st.image("education.png", width=600)
    st.title('📖 Welcome to your Essential of Anantomy and Physiology Assistant!🌐')
    st.sidebar.title("📖 Copilot for Anantomy and Physiology  !🌐")
    st.sidebar.caption("Made by an Pascal Burume")
    st.sidebar.info("""
    Generative AI technology has the potential to greatly enhance education in the health sector, particularly in fields like anatomy and physiology. This is because AI platforms can create highly detailed and interactive models of the human body, making complex systems like the cardiovascular or nervous systems easier to understand than with traditional methods.
    """)
def main():
    allowSelfSignedHttps(True)
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for interaction in st.session_state.chat_history:
        if interaction["inputs"]["chat_input"]:
            with st.chat_message("user"):
                st.write(interaction["inputs"]["chat_input"])
        if interaction["outputs"]["chat_output"]:
            with st.chat_message("assistant"):
                st.write(interaction["outputs"]["chat_output"])

    # React to user input
    if user_input := st.chat_input("Ask me anything..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(user_input)

        # Query API
        data = {"chat_history": st.session_state.chat_history, 'chat_input': user_input}
        body = json.dumps(data).encode('utf-8')
        url = 'https://essentialap.swedencentral.inference.ml.azure.com/score'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {AZURE_ENDPOINT_KEY}',
            'azureml-model-deployment': 'essentialap-1'
        }
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            response_data = json.loads(response.read().decode('utf-8'))

            # Print out the response data
            st.write(response_data)

            # Check if 'chat_output' key exists in the response_data
            if 'chat_output' in response_data:
                with st.chat_message("assistant"):
                    st.markdown(response_data['chat_output'])

                st.session_state.chat_history.append(
                    {"inputs": {"chat_input": user_input},
                     "outputs": {"chat_output": response_data['chat_output']}}
                )

            else:
                st.error("The response data does not contain a 'chat_output' key.")

        except urllib.error.HTTPError as error:
            st.error(f"The request failed with status code: {error.code}")

if __name__ == "__main__":
    main()