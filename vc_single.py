import os
import shutil
import sys
import warnings
from pathlib import Path

import soundfile as sf
import torch
from dotenv import load_dotenv

from configs.config import Config
from infer.modules.vc.modules import VC

# Set up environment
now_dir = os.getcwd()
sys.path.append(now_dir)
load_dotenv()

# Temporary directories setup
tmp = os.path.join(now_dir, "TEMP")
shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/infer_pack" % now_dir, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/uvr5_pack" % now_dir, ignore_errors=True)
os.makedirs(tmp, exist_ok=True)
os.makedirs(os.path.join(now_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(now_dir, "assets/weights"), exist_ok=True)
os.environ["TEMP"] = tmp
weight_root = os.getenv("weight_root")
weight_uvr5_root = os.getenv("weight_uvr5_root")
index_root = os.getenv("index_root")
outside_index_root = os.getenv("outside_index_root")
torch.manual_seed(114514)
warnings.filterwarnings("ignore")

# Load configuration and VC module
base_dir = Path(__file__).resolve().parent
config = Config()
vc = VC(config)


def initialize_vc(vc, voice_name):
    model_path = f"{voice_name}.pth"
    vc.get_vc(model_path)


def get_cloned_voice(voice_name, original_audio, output_file_path):
    index_file_path = base_dir / "logs" / voice_name / f"added_IVF256_Flat_nprobe_1_{voice_name}_v2.index"

    spk_item = 0
    vc_transform0 = -7 # 0
    f0_file = None
    f0method0 = "rmvpe"
    file_index1 = ""
    file_index2 = index_file_path.as_posix()
    index_rate1 = 0.75 # 0.75
    filter_radius0 = 3 # 3
    resample_sr0 = 0 # 0
    rms_mix_rate0 = 0.25 # 0.25
    protect0 = 0.33 # 0.33

    # Perform voice conversion
    info, response = vc.vc_single(
        spk_item,
        original_audio,
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
    )

    if "Success" in info:
        tgt_sr, audio_opt = response
        # Save the output audio
        sf.write(output_file_path, audio_opt, tgt_sr)
        return output_file_path
    else:
        raise Exception(info)


if __name__ == "__main__":
    voice_name = "bible-voice"
    voice_name = "youinna"
    voice_name = "son-announcer"
    
    original_voice = base_dir / "outputs" / "_google_tts_korean_1.mp3"
    # original_voice = "male_base_voice.wav"
    output_folder = output_file_path = base_dir / "outputs" / voice_name
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = output_folder / f"cloned_google_tts_korean_1.wav"

    try:
        initialize_vc(vc, voice_name)
        response = get_cloned_voice(voice_name, original_voice.as_posix(), output_file_path.as_posix())
        print(f"Cloned voice saved to: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
