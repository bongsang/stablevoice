import os
import numpy as np
from pathlib import Path
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioClip
from openai import OpenAI
from google.cloud import texttospeech

# Initialize OpenAI API client
client = OpenAI()
gtts = texttospeech.TextToSpeechClient()

# Define directories
base_dir = Path(__file__).parent
source_dir = base_dir / "sources"
os.makedirs(source_dir, exist_ok=True)

output_dir = base_dir / "outputs"
os.makedirs(output_dir, exist_ok=True)



def generate_silent_audio(duration, fps=44100):
    """
    Generates a silent audio clip of the given duration.

    Args:
    duration (float): Duration of the silence in seconds.
    fps (int): Frames per second, defaults to 44100 (CD quality).

    Returns:
    AudioClip: A MoviePy AudioClip of the silent duration.
    """
    # Calculate the number of samples needed for the given duration
    num_samples = int(duration * fps)
    # Create an array of zeros (silence) with two columns for stereo
    silent_array = np.zeros((num_samples, 2))
    # Create and return the AudioClip
    return AudioClip(lambda t: silent_array, duration=duration, fps=fps)

def translate(context, text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """Translate the following Korean lyrics into English.
Note that this is not a standard document but a song, so it's crucial to match the tone and style of the original text.
The new given text may be challenging to translate as it is fragmented along with the music. To solve the problem, I will provide you with the concatenated context of the words so far to aid in this task.
Therefore, you should reference the provided context to translate the given text accurately. If some words are ambiguous, make educated guesses based on the overall context.
You may also introduce new words if they fit well within the given context.
Return only new translated text not including context or history.
"""
            },
            {"role": "user", "content": f"[Context]\n{context}\n\n[New Text]\n{text}"}
        ]
    )
    translated_text = response.choices[0].message.content.strip()

    return translated_text

def gtts_audio(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-F",
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1
    )

    response = gtts.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    file_name = output_dir / "_gtts_audio.mp3"
    with open(file_name.as_posix(), "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{file_name}"')

    return file_name

# Function to check if the duration of two audio files are the same
def check_audio_duration(original_duration, generated_audio_path):
    with AudioFileClip(generated_audio_path) as generated_audio:
        return abs(original_duration - generated_audio.duration) < 0.1  # Allowing a small tolerance

# 1. Extract lyrics in Korean with timestamps from the audio file
source_file_path = source_dir / "haeya-short.mp3"
audio = AudioFileClip(source_file_path.as_posix())
duration_in_seconds = audio.duration

with open(source_file_path.as_posix(), "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        language='ko',
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

# Extract the words and their timestamps
korean_lyrics_with_timestamps = transcription.words

first_vocal_start_time = float(korean_lyrics_with_timestamps[0]['start'])
first_silent_clip = generate_silent_audio(first_vocal_start_time)

audio_clips = []
audio_clips.append((0.0, first_silent_clip)) # [(start time in float, audio clip), ...
context = []
for lyrics_dict in korean_lyrics_with_timestamps:
    text = lyrics_dict['word']
    start_time = lyrics_dict['start']
    context.append(text)

    context_str = " ".join(context)
    translated_text = translate(context_str, text)
    translated_audio_file = gtts_audio(translated_text)
    translated_audio_clip = AudioClip(translated_audio_file)
    audio_clips.append((start_time, translated_audio_clip))

# Generate new full audio file by concatenating audio_clips

