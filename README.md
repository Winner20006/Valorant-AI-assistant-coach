# Sky Final: VALORANT Decision Support AI

An AI-powered decision support system for professional VALORANT players and coaches. It provides real-time tactical advice (Mid-Round) and post-round analysis (Post-Game) using LLMs, speech-to-text, and text-to-speech.

## 🚀 Overview

Sky Final is a multi-agent system designed to assist VALORANT teams in high-pressure environments:
- **Brain (Router)**: The central coordinator that interprets user intent and routes queries to the appropriate specialized agent.
- **Mid-Game Agent**: A live-round tactical advisor. It takes real-time round data and provides exactly two actionable options for the IGL (In-Game Leader) under strict time constraints.
- **Post-Game Agent**: A tactical analyst for post-round or general strategic queries. It evaluates claims and explains trade-offs between different tactical approaches.
- **VLM (Vision-Language Model)**: A visual processing agent using ResNet-18 to detect in-game events (kills, deaths, round ends) from screenshots.
- **STT (Speech-to-Text)**: Hands-free interaction using OpenAI Whisper, allowing players to speak naturally.
- **TTS (Text-to-Speech)**: High-quality voice feedback using Kokoro ONNX, enabling the AI to "talk back" to the team.
- **Data Agent**: Orchestrates data retrieval, combining VLM visual data with other sources to provide context to the tactical agents.

## 🛠 Stack

- **Language**: Python 3.12+
- **LLM Framework**: [LangChain](https://www.langchain.com/) (LCEL)
- **Local LLM**: [Ollama](https://ollama.com/) (default: `llama3.2:1b`)
- **Speech-to-Text**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Text-to-Speech**: [Kokoro ONNX](https://github.com/theodoregit/kokoro-onnx)
- **Computer Vision**: [PyTorch](https://pytorch.org/) & [Torchvision](https://pytorch.org/vision/) (ResNet-18)
- **Package Management**: Pip
- **Audio I/O**: PyAudio, SoundDevice, and SpeechRecognition

## 📋 Requirements

### System Dependencies
- **Python 3.12+**
- **PortAudio**: Required for `PyAudio` and `sounddevice`.
  - MacOS: `brew install portaudio`
  - Linux: `sudo apt-get install libportaudio2`
- **Ollama**: Must be installed and running locally.

### Model Files
- **Ollama Model**: `llama3.2:1b` (can be changed in `agents/brain.py`)
- **Whisper Model**: `tiny.en` (downloaded automatically on first run)
- **Computer Vision**: ResNet-18 weights (downloaded automatically on first run via `torchvision`)
- **Kokoro TTS**:
  - `kokoro.onnx`
  - `voices.bin`
  - Both files must be placed in the `tts_models/` directory.

## ⚙️ Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "sky finall"
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv ai
   source ai/bin/activate  # MacOS/Linux
   # or
   ai\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Model Initialization**:
   - Pull the Ollama model:
     ```bash
     ollama pull llama3.2:1b
     ```
   - Ensure `tts_models/kokoro.onnx` and `tts_models/voices.bin` are present.

## 🏃 Scripts & Entry Points

### Main Application
The primary way to interact with Sky Final is through the integrated loop:
```bash
python main.py
```
This script initializes STT, the Brain router, and TTS, then enters a listening loop.

### Individual Module Tests
You can run individual components to verify their functionality:

- **Mid-Game Agent (Manual Data Test)**: 
  ```bash
  python agents/mid_game.py
  ```
- **STT (Microphone Test)**:
  ```bash
  python stt/stt_model.py
  ```
- **TTS (Voice Output Test)**:
  ```bash
  python tts/tts_model.py
  ```
- **VLM (Vision Test)**:
  ```bash
  python agents/VLM.py
  ```
- **Brain (Router Test)**:
  *(Note: Currently relies on internal `if __name__ == "__main__":` blocks if added, or can be tested via `main.py`.)*

## 📁 Project Structure

```text
.
├── agents/             # LLM Agent Logic
│   ├── brain.py        # Router and coordinator
│   ├── mid_game.py     # Live round tactical advisor
│   ├── post_game.py    # Post-round analyst
│   ├── data_agent.py   # Game data retrieval logic
│   └── VLM.py          # Vision-Language Model for event detection
├── stt/                # Speech-to-Text (Whisper)
│   └── stt_model.py    
├── tts/                # Text-to-Speech (Kokoro)
│   └── tts_model.py    
├── tts_models/         # Storage for ONNX/Bin model files
├── ai/                 # Python virtual environment (standard name)
├── main.py             # Main system entry point
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 🔐 Environment Variables

Currently, the project runs entirely locally using Ollama and local models. 
(TODO: Add environment variables if integrating with cloud providers like OpenAI or Anthropic.)

## 🧪 Tests

- **Modular Tests**: Each major component contains a `main()` function or an `if __name__ == "__main__":` block for quick verification. Run the files directly as described in the [Scripts](#-scripts--entry-points) section.
- **Unit Tests**: (TODO: Implement a formal test suite using `pytest`.)

## 📝 TODO

- [ ] Connect `data_agent.py` to a real-time VALORANT data source (e.g., OCR or Game API).
- [ ] Refine `VLM.py` classification logic with trained models instead of placeholders.
- [ ] Expand `PostGameAgent` to consume specific match history data.
- [ ] Add `pytest` coverage for agent logic and routing.
- [ ] Support more voices and languages in TTS/STT.

## 📄 License

(TODO: Add License information, e.g., MIT)
