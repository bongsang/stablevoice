import json
from google.cloud import texttospeech
import os
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from pathlib import Path
import torch
import numpy as np
from openai import OpenAI

# Initialize OpenAI API client
openai_client = OpenAI()
google_client = texttospeech.TextToSpeechClient()

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

base_dir = Path(__file__).parent
source_dir = base_dir / "sources"
output_dir = base_dir / "outputs"
os.makedirs(source_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
model.config.forced_decoder_ids = None
# Move model to GPU
model.to(device)


def transcribe(audio_file_path, chunk_length_s):
    audio, sampling_rate = librosa.load(audio_file_path.as_posix(), sr=16000)

    # Define a function to split audio into chunks
    def chunk_audio(audio, chunk_length_s=chunk_length_s, sampling_rate=sampling_rate):
        chunk_length = chunk_length_s * sampling_rate
        audio_chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
        return audio_chunks

    # Split audio into 30-second chunks
    audio_chunks = chunk_audio(audio)

    # Process each chunk and concatenate the transcriptions
    transcriptions = []

    for chunk in audio_chunks:
        input_features = processor(chunk, sampling_rate=sampling_rate, return_tensors="pt").input_features
        input_features = input_features.to(device)
        predicted_ids = model.generate(input_features, language="en")
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        print(transcription)
        transcriptions.extend(transcription)
    
    return transcriptions

def summary(input_texts, lang):
    summaries = []
    
    for text in input_texts:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a helpful summary bot. Please provide the summary in {lang}.\n"
                            "Return the summary in the following JSON format:\n"
                            "{\n"
                            "    \"title\": <title of the summary>,\n"
                            "    \"subtitle\": <summary>\n"
                            "}"
                        ).strip()
                    },
                    {
                        "role": "user",
                        "content": text.strip()
                    }
                ]
            )
            content_str = response.choices[0].message.content
            content_json = json.loads(content_str)
            
            summaries.append(content_json)
        
        except Exception as e:
            print(f"An error occurred while processing the text: {text}\nError: {e}")
            summaries.append(None)

    return summaries



def google_tts(text, file_path):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        # name="en-US-Standard-C",
        # name="ko-KR-Standard-A", # female
        name="ko-KR-Standard-B", # female
        # name="ko-KR-Standard-C", # male
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1
    )

    response = google_client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    try:
        with open(file_path.as_posix(), "wb") as out:
            out.write(response.audio_content)
    except Exception as e:
        raise Exception(f"In Google TTS, error: {e}")


def openai_tts(text, file_path):
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
        input=text
    )

    try:
        content = response.read()  # Read the content of the response
        with open(file_path.as_posix(), "wb") as out:
            out.write(content)  # Write the content to the file
    except Exception as e:
        raise Exception(f"In OpenAI TTS, error: {e}")


if __name__ == "__main__":
    # load your own audio file
    audio_file_path = source_dir / "apple2.m4a"  # Update this to your audio file path
    chunk_length_s = 60
    transcriptions = transcribe(audio_file_path, chunk_length_s)
    print(transcriptions)

    summaries = summary(transcriptions, "Korean")
    print(summaries)

    # final_transcription = " ".join(transcriptions)
    # # Save the transcription to a file
    # with open(output_dir / "transcription2.txt", "w") as f:
    #     f.write(final_transcription)

    # final_summary = " ".join(summaries)
    # # Save the transcription to a file
    # with open(output_dir / "summary2.txt", "w") as f:
    #     f.write(final_transcription)
    
    for i, data in enumerate(summaries):
        file_name = f"_google_tts_korean_{i}.mp3"
        file_path = output_dir / file_name
        # google_tts(data['subtitle'], file_path)
        openai_tts(data['subtitle'], file_path)
