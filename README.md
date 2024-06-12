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

#### With CUDA 11.8
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Or,
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

#### With CUDA 12.1
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
Or,
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

### Install Python Libraries
```bash
pip install -r requirements.txt
```

### Install Fairseq
For Windows users, open new prompt outside of VSCode as <span style="color:red">**Administrator**</span>. If not, you will get errors.

```bash
pip install git+https://github.com/One-sixth/fairseq.git
```

## Run
### MacOS
可以通过 `run.sh` 来安装依赖
```bash
sh ./run.sh
```

## 其他预模型准备
RVC需要其他一些预模型来推理和训练。

你可以从我们的[Hugging Face space](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/)下载到这些模型。

### 1. 下载 assets
以下是一份清单，包括了所有RVC所需的预模型和其他文件的名称。你可以在`tools`文件夹找到下载它们的脚本。

- ./assets/hubert/hubert_base.pt

- ./assets/pretrained 

- ./assets/uvr5_weights

想使用v2版本模型的话，需要额外下载

- ./assets/pretrained_v2

### 2. 安装 ffmpeg
若ffmpeg和ffprobe已安装则跳过。

#### Ubuntu/Debian 用户
```bash
sudo apt install ffmpeg
```
#### MacOS 用户
```bash
brew install ffmpeg
```
#### Windows 用户
下载后放置在根目录。
- 下载[ffmpeg.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffmpeg.exe)

- 下载[ffprobe.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffprobe.exe)

### 3. 下载 rmvpe 人声音高提取算法所需文件

如果你想使用最新的RMVPE人声音高提取算法，则你需要下载音高提取模型参数并放置于RVC根目录。

- 下载[rmvpe.pt](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/rmvpe.pt)

#### 下载 rmvpe 的 dml 环境(可选, A卡/I卡用户)

- 下载[rmvpe.onnx](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/rmvpe.onnx)

### 4. AMD显卡Rocm(可选, 仅Linux)

如果你想基于AMD的Rocm技术在Linux系统上运行RVC，请先在[这里](https://rocm.docs.amd.com/en/latest/deploy/linux/os-native/install.html)安装所需的驱动。

若你使用的是Arch Linux，可以使用pacman来安装所需驱动：
````
pacman -S rocm-hip-sdk rocm-opencl-sdk
````
对于某些型号的显卡，你可能需要额外配置如下的环境变量（如：RX6700XT）：
````
export ROCM_PATH=/opt/rocm
export HSA_OVERRIDE_GFX_VERSION=10.3.0
````
同时确保你的当前用户处于`render`与`video`用户组内：
````
sudo usermod -aG render $USERNAME
sudo usermod -aG video $USERNAME
````

## 开始使用
### 直接启动
使用以下指令来启动 WebUI
```bash
python infer-web.py
```

若先前使用 Poetry 安装依赖，则可以通过以下方式启动WebUI
```bash
poetry run python infer-web.py
```

### 使用整合包
下载并解压`RVC-beta.7z`
#### Windows 用户
双击`go-web.bat`
#### MacOS 用户
```bash
sh ./run.sh
```
### 对于需要使用IPEX技术的I卡用户(仅Linux)
```bash
source /opt/intel/oneapi/setvars.sh
```

## 参考项目
+ [ContentVec](https://github.com/auspicious3000/contentvec/)
+ [VITS](https://github.com/jaywalnut310/vits)
+ [HIFIGAN](https://github.com/jik876/hifi-gan)
+ [Gradio](https://github.com/gradio-app/gradio)
+ [FFmpeg](https://github.com/FFmpeg/FFmpeg)
+ [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui)
+ [audio-slicer](https://github.com/openvpi/audio-slicer)
+ [Vocal pitch extraction:RMVPE](https://github.com/Dream-High/RMVPE)
  + The pretrained model is trained and tested by [yxlllc](https://github.com/yxlllc/RMVPE) and [RVC-Boss](https://github.com/RVC-Boss).

## 感谢所有贡献者作出的努力
<a href="https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=RVC-Project/Retrieval-based-Voice-Conversion-WebUI" />
</a>
