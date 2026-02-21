
# 🛡️ AI Network Watcher: Setup & Installation Guide

Welcome to the AI Network Watcher! This tool uses Deep Packet Inspection (DPI) and a local Large Language Model (LLM) to monitor your network traffic in real-time for privacy threats, data brokers, and security anomalies.

Requirements
requests
ollama
langchain
langchain-community
langchain-text-splitters
chromadb
sentence-transformers
EOF

## ✨ Features

- 🔍 **Deep Packet Inspection**: Captures live network traffic using TShark without dropping packets.
- 🧠 **Local AI Analysis**: Uses Ollama (Qwen3) to audit traffic for privacy threats 100% locally.
- 🛡️ **Threat Intelligence**: Automatically downloads and cross-references the StevenBlack Privacy Blocklist.
- 📊 **Real-Time GUI**: Clean, Tkinter-based dashboard for live monitoring and historical logging.

## 🚀 Quick Start

### 1. Install Prerequisites (Ubuntu/Debian)

The core engine relies on TShark (the terminal version of Wireshark) and Tkinter. Open your terminal and run:

```bash
sudo apt update
sudo apt install tshark python3-tk python3-venv
```

**⚠️ CRITICAL PERMISSION STEP:** By default, Linux does not let standard users sniff network packets. You must add your user to the Wireshark group so the app can run without needing root/sudo:

```bash
sudo dpkg-reconfigure wireshark-common
# (Select "Yes" when it asks if non-superusers should be able to capture packets)

sudo usermod -aG wireshark $USER
# Note: You MUST log out of your computer and log back in for this to take effect!
```

### 2. Install Ollama (Local AI Engine)

This app is strictly privacy-first. The AI analysis happens entirely on your machine.

```bash
# Install Ollama
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# Pull the Qwen3 4B Instruct model
ollama pull qwen3:4b-instruct
```

### 3. Set Up Python Environment

```bash
# Clone the repository (Replace YOUR-USERNAME with your actual GitHub username)
git clone [https://github.com/YOUR-USERNAME/AI-Network-Watcher.git](https://github.com/YOUR-USERNAME/AI-Network-Watcher.git)
cd AI-Network-Watcher

# Create virtual environment
python3 -m venv myenv

# Activate it
source myenv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Make sure your virtual environment is active
source myenv/bin/activate

# Start the application
python net_monitor.py
```

## 🎯 What to Expect

Upon launch, the app will automatically download the latest StevenBlack Privacy Blocklist (over 70,000 known ad-trackers). It will then open a GUI and begin sniffing packets. Every 60 seconds, it compiles the traffic, flags any known data brokers, and passes the batch to the local Qwen3 AI for a complete privacy and cybersecurity audit. All reports are permanently saved to a local security_logs.txt file.
EOF
