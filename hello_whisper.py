import time
import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI API client
client = OpenAI()

# Define directories
base_dir = Path(__file__).parent
source_dir = base_dir / "sources"
os.makedirs(source_dir, exist_ok=True)

output_dir = base_dir / "outputs"
os.makedirs(output_dir, exist_ok=True)

# 1. Extract lyrics in Korean with timestamps from the audio file
source_file_path = source_dir / "haeya-short.mp3"
audio_file = open(source_file_path.as_posix(), "rb")

transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["word"]
)

lyrics_timestamp = transcript.words

# 2. Translate the extracted lyrics into English along with the timestamps
translated_lyrics_with_timestamps = []
for segment in lyrics_timestamp:
    start_time = segment['start']
    end_time = segment['end']
    text = segment['word']
    
    translation_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """Translate the following Korean lyrics into English. If there is not provided Korean lyrics, do not translate and return the emtpy message like ''.
Preserve the meaning and try to match the rhythm and syllable count as much as possible.
"""},
            {"role": "user", "content": text}
        ]
    )
    
    translated_text = translation_response.choices[0].message.content
    translated_lyrics_with_timestamps.append({
        "start": start_time,
        "end": end_time,
        "text": translated_text
    })

print(translated_lyrics_with_timestamps)


# Write the translated lyrics with timestamps to a text file
translated_lyrics_file_path = output_dir / "haeya_translated.txt"
with open(translated_lyrics_file_path.as_posix(), "w") as file:
    for lyric in translated_lyrics_with_timestamps:
        file.write(f"[{lyric['start']:.2f} - {lyric['end']:.2f}] {lyric['text']}\n")

print(f"Translated lyrics saved to {translated_lyrics_file_path}")

# 3. Create new vocals based on the translated lyrics with timestamps
# Important: Fit the new vocals into the same timestamp

# Create a single text input for TTS by joining translated lyrics
tts_input = "\n".join([lyric["text"] for lyric in translated_lyrics_with_timestamps])

# Generate speech
tts_response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=tts_input
)

# Save the TTS output
output_file_path = output_dir / "haeya_translated.mp3"
with open(output_file_path.as_posix(), "wb") as f:
    f.write(tts_response.read())

print(f"Translated and synthesized audio saved to {output_file_path}")
