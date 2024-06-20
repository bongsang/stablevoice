import torch
from TTS.api import TTS
from pathlib import Path

base_dir = Path(__file__).parent

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
# Text to speech to a file
source_file = base_dir / "sources" / "train" / "youinna.wav"
output_file = base_dir / "outputs" / "_TTS_youinna.wav"
tts.tts_to_file(
    text="""
유쾌 상쾌한 쾌변처럼 일상의 스트레스를 날려줄 웃음펀치!
송해 할아버지가가 목욕을 하면? “뽀송뽀송해.”
전화기로 세운 건물은 “콜로세움.”
몇 년 전부터 등장하여 “뭐야~.” 하고 핀잔 받던 아재개그가 요즘 더욱 확산되며 어느새 개그 코드 중 하나로 자리 잡았다. TV 토크 프로그램의 연예인이 돌연 생뚱맞은 아재개그를 날린다. 처음엔 썰렁하다고 눈총 주기 바빴는데 이젠 재치와 그 시의적절함을 은근히 부러워하는 눈치다.
과거 참새 시리즈와 최불암 시리즈, 한 줄짜리 썰렁 개그의 연장선에 있는 아재개그는 의성어와 의태어를 활용하고, 우리말과 영어를 섞어서 구사하되 그 적절한 타이밍이 요구된다. 그리고 박장대소는 힘들고 너무 웃으면 격이 떨어져 약간 시크하게 웃고 나면 그만인 개그다. 한때 세대 차의 상징처럼 여겼던 이 썰렁 개그에 지금은 오히려 젊은 층이 열광하는데, 그 이유를 물어보면 ‘안 웃긴데 웃기고’, ‘들을수록 중독된다’는 것이다.
""",
    speaker_wav=source_file.as_posix(),
    language="ko",
    file_path=output_file.as_posix()
)

# [!] Warning: The text length exceeds the character limit of 95 for language 'ko', this might cause truncated audio.

