
# 🛡️ AI Network Watcher: Security & Privacy Edition

A lightweight Ubuntu desktop application that monitors real-time outbound network traffic and uses a local Large Language Model (LLM) to translate raw technical data into human-readable summaries.

## ✨ Features & Architecture

* **The "Zero Blind Spot" Pipeline**: Traditional network monitors (like top or nethogs) use a "polling" method—taking snapshots every few seconds. This creates blind spots where fast-executing malware or background telemetry can send a payload and close the socket undetected. Solution: This tool utilizes tshark (Wireshark CLI) running in a continuous background subprocess stream. It catches every single packet the millisecond it hits the network interface card (NIC).
* **Thread-Safe Data Bucket**: To prevent the UI and AI from crashing while reading data that TShark is actively writing, the system uses a Python threading.Lock() (Mutex). Packets are continuously dumped into a shared memory bucket. Every 60 seconds, the reporting thread locks the bucket, copies the data, instantly clears the original bucket, and unlocks it—ensuring no packets are dropped during the AI analysis phase.
* **Deep Packet SNI Extraction**: IP addresses alone are useless for privacy auditing (e.g., distinguishing between a Google Search and a hidden Google Analytics tracker). The app instructs TShark to extract the Server Name Indication (SNI) from TLS handshakes and DNS Queries. This reveals the exact domain names (like tracking.prf.hn or ads.mozilla.org) routing through cloud infrastructure.
* **Real-Time Threat Intelligence**: On startup, the application pulls the latest StevenBlack Hosts Blocklist (the same open-source intelligence used by Pi-Hole) directly into system memory. It cross-references over 79,000 known tracking, telemetry, and affiliate marketing domains against the live packet stream, immediately tagging privacy threats before they even reach the AI.
* **Stateless Local AI Analysis**: The tool features a fully local, privacy-respecting AI integration. Every 60 seconds, the top 15 traffic destinations are enriched with GeoIP physical location data and fed into a local Qwen3:4b-instruct model via Ollama. The AI is strictly prompt-engineered to act as a cybersecurity auditor, evaluating the enriched dataset for anomalous volumes, unusual ISPs, and flagged privacy trackers. The analysis is completely stateless, meaning it analyzes the isolated 60-second window without overrunning token limits or memory context.

## ⚙️ How It Works
The application operates in a 3-step cycle every 2 minutes:
1. **Capture:** Uses nethogs in trace mode to identify exactly which processes (apps) are sending data and to which remote IP addresses.
2. **Analyze:** Passes the raw, messy terminal output to Ollama (running locally).
3. **Summarize:** The Al filters out system background noise and displays a clean list in the GUI window: [App] sent [Amount] to [Server].

## 🛠️ Tech Stack & Requirements
* **OS:** Ubuntu 22.04+
* **Environment:** Python 3.x (specifically Python 3.12)
* **Packet Capture Engine:** TShark (Wireshark) and nethogs
* **AI/LLM Ops:** Ollama (Qwen3) / llama3
* **GUI Framework:** Tkinter (python3-tk)
* **Data Enrichment:** IP-API (GeoIP lookup), Requests
* **Deployment:** PyInstaller (compiled as a standalone Linux binary with a .desktop integration)

## 🚀 Setup & Installation (Ubuntu/Debian)

### 1. Install Prerequisites
The core engine relies on TShark, Nethogs, and Tkinter. Open your terminal and run:

```bash
sudo apt update
sudo apt install tshark nethogs python3-tk python3-venv
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

## 🎮 Running the Application
Once installed, execute the following command to start the monitor:

```bash
./myenv/bin/python3 net_monitor.py
```
*(Note: If the application needs raw socket access outside the Wireshark group, run it with root privileges: `sudo python3 net_monitor.py`)*

## 📊 Output & Logging
The application provides a live, scrolling GUI of the AI's 60-second audits. Simultaneously, it maintains a persistent `security_logs.txt` file, saving a permanent historical record of all traffic spikes and identified threats for later analysis. Upon launch, the app will automatically download the latest StevenBlack Privacy Blocklist (over 70,000 known ad-trackers) to enrich these logs.
EOF
