import streamlit as st
from src.helper import voice_input, llm_model, text_to_speech

def main():
    st.title("Multilingual AI Assistant")

    if st.button("Ask me anything"):

        with st.spinner("Listening..."):
            try:
                text = voice_input()  # Assuming voice_input returns the spoken text
                if not text:
                    st.error("No input received. Please try again.")
                    return

                response = llm_model(text)  # Assuming llm_model processes the text and generates a response
                if not response:
                    st.error("No response generated. Please try again.")
                    return

                # Convert the response to speech
                text_to_speech(response)  # Assuming this generates a speech file "speech.mp3"

                # Open the audio file
                with open("speech.mp3", "rb") as audio_file:
                    audio_bytes = audio_file.read()

                # Display the response and audio
                st.text_area(label="Response:", value=response, height=350)
                st.audio(audio_bytes)

                # Provide download link for the speech
                st.download_button(
                    label="Download Speech",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
