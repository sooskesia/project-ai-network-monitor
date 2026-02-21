# project-ai-network-monitor
Real-time, AI-powered network monitor that detects stealthy data brokers, telemetry trackers, and security threats using a local Large Language Model.



# 🛡️ AI Network Watcher: Setup & Installation Guide

Welcome to the AI Network Watcher! This tool uses Deep Packet Inspection (DPI) and a local Large Language Model (LLM) to monitor your network traffic in real-time for privacy threats, data brokers, and security anomalies. 

Because this tool interacts directly with your Network Interface Card (NIC) and runs a local AI, there are a few system-level dependencies you need to install before running the Python script.

## ⚙️ Prerequisites (Ubuntu/Debian Linux)

### 1. Install TShark (Packet Sniffer) & Tkinter (GUI)
The core engine relies on TShark (the terminal version of Wireshark) to capture packets, and Tkinter for the desktop interface. Open your terminal and run:

```bash
sudo apt update
sudo apt install tshark python3-tk python3-venv

⚠️ CRITICAL PERMISSION STEP: By default, Linux does not let standard users sniff network packets. You must add your user to the Wireshark group so the app can run without needing root/sudo:
Bash

sudo dpkg-reconfigure wireshark-common

(Select "Yes" when it asks if non-superusers should be able to capture packets)
Bash

sudo usermod -aG wireshark $USER

Note: You must log out of your computer and log back in for this permission to take effect!

2. Install Ollama (Local AI Engine)

This app is strictly privacy-first, meaning the AI analysis happens 100% locally on your machine. You need to install Ollama and pull the specific Qwen3 models the app uses.
Bash

curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
ollama pull qwen3:4b-instruct

🚀 Installation & Running the App

Once the system prerequisites are handled, setting up the Python environment takes less than a minute.

1. Clone the repository:
Bash

git clone [https://github.com/YOUR-USERNAME/AI-Network-Watcher.git](https://github.com/YOUR-USERNAME/AI-Network-Watcher.git)
cd AI-Network-Watcher

2. Create and activate a virtual environment:
Bash

python3 -m venv myenv
source myenv/bin/activate

3. Install the required Python libraries:
Bash

pip install -r requirements.txt

4. Run the application:
Bash

python net_monitor.py

🎯 What to Expect

Upon launch, the app will automatically download the latest StevenBlack Privacy Blocklist (over 70,000 known ad-trackers). It will then open a GUI and begin sniffing packets. Every 60 seconds, it compiles the traffic, flags any known data brokers, and passes the batch to the local Qwen3 AI for a complete privacy and cybersecurity audit. All reports are permanently saved to a local security_logs.txt file.


*(Don't forget to change `YOUR-USERNAME` in the `git clone` command once you paste it!)*

**Let me know when your GitHub repo is officially complete, and we will finally write that Python LangChain script to hook up your local RAG system to the logs!**
