import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech
from logger import logging 
from exception import CustomException  



def main():
    st.title("Multilingual AI Assistant")

    if st.button("Ask me anything"):

        with st.spinner("Listening..."):
            try:
                text = voice_input()  
                if not text:
                    st.error("No input received. Please try again.")
                    logging.info("No input received from voice input.")
                    return

                response = llm_model_object(text)  # Assuming llm_model processes the text and generates a response
                if not response:
                    st.error("No response generated. Please try again.")
                    logging.info("No response generated from model.")
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
                logging.info("Successfully generated and displayed the response with audio.")

            except Exception as e:
                # Log the exception with traceback
                logging.info(f"An error occurred: {e}")
                st.error(f"An error occurred: {e}")
                raise CustomException(f"Error in main function: {e}")

if __name__ == '__main__':
    try:
        main()
    except CustomException as ce:
        logging.info(f"Critical Error: {ce}")
        st.error(f"A critical error occurred: {ce}")
