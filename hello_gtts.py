import os

import gradio as gr
from google.cloud import texttospeech
from gradio_client import Client

# Assuming the Gradio app is running locally on the default port 7865
# GRADIO_URL = "http://127.0.0.1:7865"
# client = Client(GRADIO_URL)
text_to_speech_client = texttospeech.TextToSpeechClient()


def get_base_voice(text, sex):
    input_text = texttospeech.SynthesisInput(text=text)
    if sex == "female":
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Neural2-A",
        )
    else:
        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Wavenet-C",
        )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1
    )

    response = text_to_speech_client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    file_name = sex + "_base_voice.wav"
    with open(file_name, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{file_name}"')

    return file_name


def get_cloned_voice(base_voice_path):
    model_name = "son-announcer.pth"
    index_file_path = (
        "logs/son-announcer/added_IVF256_Flat_nprobe_1_son-announcer_v2.index"
    )
    spk_item = 0
    vc_transform0 = 0
    f0_file = None
    f0method0 = "rmvpe"
    file_index1 = ""
    file_index2 = index_file_path
    index_rate1 = 0.75
    filter_radius0 = 3
    resample_sr0 = 0
    rms_mix_rate0 = 0.25
    protect0 = 0.33

    # Log the inputs being sent to Gradio API for debugging
    print("Sending the following parameters to Gradio API:")
    print(f"spk_item: {spk_item}")
    print(f"base_voice_path: {base_voice_path}")
    print(f"vc_transform0: {vc_transform0}")
    print(f"f0_file: {f0_file}")
    print(f"f0method0: {f0method0}")
    print(f"file_index1: {file_index1}")
    print(f"file_index2: {file_index2}")
    print(f"index_rate1: {index_rate1}")
    print(f"filter_radius0: {filter_radius0}")
    print(f"resample_sr0: {resample_sr0}")
    print(f"rms_mix_rate0: {rms_mix_rate0}")
    print(f"protect0: {protect0}")

    response = client.predict(
        spk_item,
        base_voice_path,
        vc_transform0,
        f0_file,
        f0method0,
        file_index1,
        file_index2,
        index_rate1,
        filter_radius0,
        resample_sr0,
        rms_mix_rate0,
        protect0,
        api_name="/infer_convert",
    )
    return response


if __name__ == "__main__":
    text = """
태초에 하나님이 천지를 창조하시니라.
땅이 혼돈하고 공허하며 흑암이 깊음 위에 있고 하나님의 영은 수면 위에 운행하시니라.
"""
    base_voice = get_base_voice(text, "male")

    # cloned_voice = get_cloned_voice(base_voice)
    # print("Cloned voice:")
    # print(cloned_voice[-1])
    
