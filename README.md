# Stable Voice UI
Stable Voice WebUI is a framework designed to facilitate easy comparison and analysis of various upcoming voice clone models in one place. It aims to promote global collaboration and development toward establishing a global standard. Initially, This is based on RVC-Project.


## Environment
The environment has been reconfigured based on Python 3.11 to support the latest features of various libraries.


## Installation
### Create virtual environments
You can use any virtual environment but I recommend using venv because the venv module supports creating lightweight "virtual environments", each with their own independent set of Python packages installed in their site directories. And, also you can use anaconda environment together.

```bash
stablevoice> python -m venv .venv
stablevoice> .venv/Scripts/activate
```
e.g. In Windows, you may see your prompt like this: (.venv) (base) D:\projects\stablevoice-webui> _

### PIP Upgrade
```bash
(.venv) stablevoice> python -m pip install --upgrade pip
```

### Install PyTorch
[PyTorch Official Guide](https://pytorch.org/get-started/locally/)

#### With CPU (Without GPU)
```bash
(.venv) stablevoice> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Or,
#### With Nvidia GPU CUDA 11.8
```bash
(.venv) stablevoice> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Or,
#### With Nvidia GPU CUDA 12.1
```bash
(.venv) stablevoice> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Install required libraries
You don't need to install Fairseq separately. There are many errors when trying to install it on Windows, and I also spent a lot of time dealing with this. To make things easier, I included the wheel locally. You can install all the libraries with just one line. If you're happy with it, please give it a star.

```bash
(.venv) stablevoice> pip install -r requirements.txt
```

### Install FFMPEG
For Windows, download ffmpeg from the official site.
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

For Linux, install ffmpeg by apt.
```bash
sudo apt update
sudo apt install ffmpeg
```
- Be sure! Include the FFMPEG path to your system $PATH variable.

## Run

```bash
(.venv) stablevoice> python main.py
```

## Base models
+ [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/)
  + The pretrained model is trained and tested by [yxlllc](https://github.com/yxlllc/RMVPE) and [RVC-Boss](https://github.com/RVC-Boss).
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [Vocal pitch extraction:RMVPE](https://github.com/Dream-High/RMVPE)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)