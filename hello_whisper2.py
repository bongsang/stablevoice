import os
from pathlib import Path
from openai import OpenAI
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioClip
import numpy as np

# Initialize OpenAI API client
client = OpenAI()

# Define directories
base_dir = Path(__file__).parent
source_dir = base_dir / "sources"
os.makedirs(source_dir, exist_ok=True)

output_dir = base_dir / "outputs"
os.makedirs(output_dir, exist_ok=True)

# Function to check if the duration of two audio files are the same
def check_audio_duration(original_duration, generated_audio_path):
    generated_audio = AudioFileClip(generated_audio_path)
    generated_duration_in_seconds = generated_audio.duration
    return abs(original_duration - generated_duration_in_seconds) < 0.1  # Allowing a small tolerance

# 1. Extract lyrics in Korean with timestamps from the audio file
source_file_path = source_dir / "haeya-short.mp3"
audio = AudioFileClip(source_file_path.as_posix())
duration_in_seconds = audio.duration

audio_file = open(source_file_path.as_posix(), "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    language='ko',
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word"]
)

# Extract the words and their timestamps
words_with_timestamps = transcription.words

# Handle possible discrepancies in the structure
korean_lyrics = " ".join([word.get("text", "") for word in words_with_timestamps if "text" in word])
print(korean_lyrics)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """Translate the following Korean lyrics into English. This is not a document but a song. So you need to match the tone and style of the text.
If you think some words are not Korean, guess based on the whole context. You may generate new words if they suit the context well.
Preserve the meaning and try to match the rhythm and syllable count as much as possible.
If no Korean lyrics are provided, return an empty string. Do not return a guide message like "Without the specific Korean lyrics, I'm unable to provide a translation. Please provide the Korean lyrics you would like translated."""},
        {"role": "user", "content": korean_lyrics if korean_lyrics.strip() else ""}
    ]
)

translated_lyrics = response.choices[0].message.content.strip()
print(translated_lyrics)

# Function to generate speech for a given text segment
def generate_speech_segment(text_segment, start_time, end_time, output_dir, index):
    tts_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text_segment
    )
    segment_path = output_dir / f"segment_{index}.mp3"
    with open(segment_path.as_posix(), "wb") as f:
        f.write(tts_response.read())
    return segment_path, start_time, end_time

# Function to create a silent audio segment
def generate_silent_audio(duration):
    fps = 44100
    samples = np.zeros((int(duration * fps), 2))  # stereo audio with two channels
    return AudioClip(lambda t: samples[:len(t)], duration=duration, fps=fps)

# 2. Generate speech segments based on timestamps
speech_segments = []
if translated_lyrics:
    for index, word_info in enumerate(words_with_timestamps):
        if "start" in word_info and "end" in word_info and "text" in word_info:
            start_time = word_info["start"]
            end_time = word_info["end"]
            text_segment = word_info["text"]
            segment_path, start_time, end_time = generate_speech_segment(
                text_segment, start_time, end_time, output_dir, index
            )
            speech_segments.append((segment_path, start_time, end_time))

# 3. Sync the translated audio segments with the original instrumental periods
original_audio_clip = AudioFileClip(source_file_path.as_posix())

# Create a list to store audio clips
clips = []
if speech_segments:
    last_end_time = 0
    for segment_path, start_time, end_time in speech_segments:
        if start_time > last_end_time:
            # Create a silent segment for the non-vocal period
            silent_segment = generate_silent_audio(start_time - last_end_time)
            clips.append(silent_segment)
        translated_clip = AudioFileClip(segment_path.as_posix())
        clips.append(translated_clip)
        last_end_time = end_time
    # Add remaining silence if any
    if last_end_time < duration_in_seconds:
        silent_segment = generate_silent_audio(duration_in_seconds - last_end_time)
        clips.append(silent_segment)
else:
    # If no speech segments, create a single silent segment
    silent_segment = generate_silent_audio(duration_in_seconds)
    clips.append(silent_segment)

# Concatenate all segments
final_audio = concatenate_audioclips(clips)

# Save the final synced audio output
final_output_path = output_dir / "haeya_translated_synced.mp3"
final_audio.write_audiofile(final_output_path)

print(f"Translated and synced audio saved to {final_output_path}")
