import torch
from TTS.api import TTS
from pathlib import Path

base_dir = Path(__file__).parent
output_dir = base_dir / "outputs"

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)

# Run TTS
output_file = output_dir / "TTS_output.mp3"
tts.tts_to_file(text="Apps like NBA, where you can watch multiple live games with stats. What If, where you become a superhero in the Marvel Universe. And Unextinct, where you can explore endangered species. Games that take advantage of your space, immerse you completely, challenge you in new ways, or let you gather around a table to play with friends, even when you're not together. You can master Meditation with Poe,", file_path=output_file.as_posix())

