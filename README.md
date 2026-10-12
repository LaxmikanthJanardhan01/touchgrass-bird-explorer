# 🌿 TouchGrass AI Bird Explorer

### Discover Nature. Identify Birdsong. Document the Wild.

TouchGrass AI Bird Explorer is an AI-powered nature exploration project designed to help people engage with the natural world through bird sound identification and AI-assisted nature journaling.

Built around the idea of **using technology to encourage people to spend more time outdoors**, the project combines bird audio analysis with a digital field journal, creating an accessible way to observe, explore, and learn from nature.

---

## 📌 Project Overview

Modern technology often keeps people focused on screens and disconnected from their surroundings. TouchGrass AI Bird Explorer explores a different approach: using AI as a tool to encourage outdoor curiosity, environmental awareness, and real-world exploration.

Users can upload bird recordings for possible species identification and document their personal observations in a nature journal supported by a locally hosted language model.

## ✨ Key Features

### 🐦 AI-Powered Bird Identification
- Upload bird audio recordings from your device.
- Analyze recordings using BirdNET to obtain possible bird species predictions.
- Review the identification results and model scores.
- Use clear recordings with minimal background noise for better results.

### 📓 AI Nature Journal
- Write observations about birds and the surrounding environment.
- Generate organized journal notes with a locally hosted Qwen2.5 language model.
- Keep the journal focused on the observations provided by the user.

### 🌱 Nature-First Experience
- Encourages outdoor exploration instead of passive screen time.
- Supports curiosity about birds, wildlife, and local ecosystems.
- Combines practical AI applications with environmental learning.

### ⚙️ Local AI Integration
- Uses Qwen2.5-0.5B-Instruct through llama.cpp for journal generation.
- Integrates the AI model with a Python and Flask web application.
- Designed to run with an Arduino UNO Q-based setup.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Hardware platform | Arduino UNO Q |
| Bird sound analysis | BirdNET |
| Language model | Qwen2.5-0.5B-Instruct |
| Local model server | llama.cpp |
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Configuration | YAML |

---

## 🏗️ Project Structure

```text
touchgrass-bird-explorer/
├── python/
│   ├── bird_worker.py
│   ├── main.py
│   └── requirements.txt
├── sketch/
│   ├── sketch.ino
│   └── sketch.yaml
├── web_app.py
├── app.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Arduino UNO Q or a compatible development environment.
- Python and pip.
- Required Python packages listed in the project requirements files.
- BirdNET components and their required model files.
- llama.cpp and the Qwen2.5-0.5B-Instruct GGUF model for AI journal generation.

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/LaxmikanthJanardhan01/touchgrass-bird-explorer.git
   cd touchgrass-bird-explorer
   ```

2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the BirdNET components and Qwen model according to your environment.

4. Start the local Qwen model server using llama.cpp, configured for the endpoint expected by the application.

5. Start the Flask web application using the appropriate Python environment and configuration.

6. Open the application in your browser and upload a supported bird audio recording or enter a nature observation.

**Note:** Model files and hardware-specific dependencies may need to be installed separately. Exact startup commands can vary depending on the environment.

---

## 🔄 How It Works

1. **Capture:** Record or select a bird sound, or write a personal nature observation.
2. **Analyze:** BirdNET analyzes the audio and returns possible species predictions.
3. **Document:** The local language model helps organize the observation into readable journal notes.
4. **Explore:** Use the results as a starting point for further observation and learning.

Bird identification results are predictions, not guaranteed identifications. AI-generated journal notes should also be reviewed for accuracy.

---

## 🎯 Project Goals

- Make AI-assisted nature exploration more accessible.
- Encourage people to observe birds and their environment.
- Explore practical local AI applications on accessible hardware.
- Combine open-source technologies for an educational, nature-focused experience.

## 🔮 Future Improvements

- Improve voice input and speech-to-text reliability.
- Add a searchable journal and observation history.
- Improve the mobile experience and accessibility.
- Expand testing across different bird recordings and environments.
- Explore location-aware observations and additional wildlife information.
- Improve setup documentation and deployment options.

## 🤝 Contributing

Contributions, bug reports, feature suggestions, and documentation improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing the improvement.

Please ensure that changes are tested and that model limitations are clearly documented.

## 🌍 Open Innovation

TouchGrass AI Bird Explorer explores how open-source tools, accessible hardware, and AI can work together to support learning beyond the screen.

By combining bird sound analysis with local AI-assisted journaling, the project aims to make technology a companion to outdoor curiosity rather than a replacement for real-world experiences.

## 📄 License

A license has not yet been specified. Before reusing or distributing this project, check the licenses of the included code, models, and dependencies. A repository license can be added once the project's licensing terms are decided.

---

**Built with curiosity, open-source technology, and a love for nature.*



