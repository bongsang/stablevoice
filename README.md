# Stable Voice WebUI
Stable Voice WebUI is not an independent model but a framework designed to facilitate easy comparison and analysis of various upcoming voice clone models in one place. It aims to promote global collaboration and development toward establishing a global standard. Initially, This is based on RVC-Project.


## Environment
The environment has been reconfigured based on Python 3.11 to support the latest features of various libraries.


## Installation
### Create virtual environments
You can use any virtual environment but I recommend using venv because the venv module supports creating lightweight "virtual environments", each with their own independent set of Python packages installed in their site directories. And, also you can use anaconda environment together.

```bash
python -m venv .venv
.venv/Scripts/activate
```
e.g. In Windows, you may see your prompt like this: (.venv) (base) D:\projects\stablevoice-webui> _

### PIP Upgrade
```bash
python -m pip install --upgrade pip
```

### Install PyTorch
[PyTorch Official Guide](https://pytorch.org/get-started/locally/)

#### With CPU (Without GPU)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Or,
#### With Nvidia GPU CUDA 11.8
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Or,
#### With Nvidia GPU CUDA 12.1
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Install required libraries
You don't need to install Fairseq separately. There are many errors when trying to install it on Windows, and I also spent a lot of time dealing with this. To make things easier, I included the wheel locally. You can install all the libraries with just one line. If you're happy with it, please give it a star.

```bash
pip install -r requirements.txt
```

### Install FFMPEG
For Windows, you don't need to install but add "stablevoice/bin/" path
```bash
# To modify the system PATH variable using setx on Windows, you should open the Command Prompt as Administrator.
# For example, if you clone stablevoice project to "D:\projects\stablevoice" then
setx PATH "%PATH%;D:\projects\stablevoice\bin"
```

For Linux, install ffmpeg directly.
```bash
sudo apt update
sudo apt install ffmpeg
```

## Run
Simple! "Ctrl+F5 in main.py" ^^

Or,
```bash
(.venv) python main.py
```

## Base models
+ [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/)
  + The pretrained model is trained and tested by [yxlllc](https://github.com/yxlllc/RMVPE) and [RVC-Boss](https://github.com/RVC-Boss).
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [Vocal pitch extraction:RMVPE](https://github.com/Dream-High/RMVPE)
