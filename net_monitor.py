import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import time
import requests
import ollama

class NetMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Network Watcher (Security & Privacy Edition)")
        self.root.geometry("850x800")
        
        # New Bucket Format: { "Domain_or_IP": bytes_sent }
        self.traffic_bucket = {}
        self.bucket_lock = threading.Lock()
        
        # Threat Intelligence Set
        self.privacy_blocklist = set()

        self.bg_color = "#1e1e1e"
        self.root.configure(bg=self.bg_color)

        tk.Label(root, text="Continuous Security & Privacy Log", font=("Arial", 14, "bold"), 
                 bg=self.bg_color, fg="white").pack(pady=10)
        
        self.display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=95, height=35, 
                                                 font=("Courier", 10), bg="#2d2d2d", fg="#d4d4d4",
                                                 insertbackground="white")
        self.display.pack(pady=10, padx=10)

        self.status_var = tk.StringVar(value="Initializing Systems...")
        tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, 
                 anchor=tk.W, bg="#333333", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

        # Download the blocklist before starting the sniffers
        self.load_threat_intelligence()

        self.sniffer_thread = threading.Thread(target=self.continuous_sniffer, daemon=True)
        self.sniffer_thread.start()

        self.report_thread = threading.Thread(target=self.reporting_loop, daemon=True)
        self.report_thread.start()

    def load_threat_intelligence(self):
        """Downloads the StevenBlack Pi-Hole Blocklist into system memory."""
        self.status_var.set("Downloading Privacy Threat Intelligence List...")
        try:
            url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
            response = requests.get(url, timeout=10)
            for line in response.text.split('\n'):
                if line.startswith("0.0.0.0 ") and "0.0.0.0 0.0.0.0" not in line:
                    domain = line.split(" ")[1].strip()
                    self.privacy_blocklist.add(domain)
            self.update_display(f"System Ready. Loaded {len(self.privacy_blocklist):,} known trackers and ad brokers.")
        except Exception as e:
            self.update_display("Failed to load blocklist. Privacy features degraded.")

    def get_active_interface(self):
        try:
            route_cmd = r"ip route get 8.8.8.8 | grep -oP 'dev \K\S+'"
            interface = subprocess.check_output(route_cmd, shell=True).decode().strip()
            return interface if interface else "eth0"
        except Exception:
            return "eth0"

    def log_to_file(self, text):
        try:
            with open("security_logs.txt", "a", encoding="utf-8") as f:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"--- [REPORT @ {timestamp}] ---\n")
                f.write(text + "\n\n" + "="*80 + "\n\n")
        except Exception:
            pass

    def continuous_sniffer(self):
        interface = self.get_active_interface()
        self.root.after(0, self.status_var.set, f"Sniffing packets & SNI on {interface}...")
        
        # Upgraded TShark command: Now extracts Domain Names via DNS or TLS SNI
        cmd = ["tshark", "-i", interface, "-l", "-n", "-T", "fields", 
               "-e", "ip.dst", "-e", "frame.len", 
               "-e", "tls.handshake.extensions_server_name", "-e", "dns.qry.name"]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
            for line in process.stdout:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    ip = parts[0]
                    
                    try:
                        length = int(parts[1])
                    except ValueError:
                        continue

                    # Determine the best identifier: SNI > DNS > IP
                    identifier = ip
                    if len(parts) > 2 and parts[2]: # TLS SNI is present
                        identifier = parts[2].split(',')[0] 
                    elif len(parts) > 3 and parts[3]: # DNS Query is present
                        identifier = parts[3].split(',')[0]

                    with self.bucket_lock:
                        self.traffic_bucket[identifier] = self.traffic_bucket.get(identifier, 0) + length
        except Exception as e:
            self.root.after(0, self.update_display, f"Sniffer Error: {e}")

    def reporting_loop(self):
        while True:
            time.sleep(60) 
            
            with self.bucket_lock:
                current_batch = self.traffic_bucket.copy()
                self.traffic_bucket.clear() 

            if not current_batch:
                continue

            self.root.after(0, self.status_var.set, "Analyzing Privacy and Security Threats...")

            sorted_traffic = sorted(current_batch.items(), key=lambda x: x[1], reverse=True)[:15]
            
            enriched_logs = []
            for identifier, bytes_sent in sorted_traffic:
                kb_sent = round(bytes_sent / 1024, 2)
                
                # Check against the privacy blocklist!
                warning = ""
                if identifier in self.privacy_blocklist:
                    warning = " 🚨 [PRIVACY THREAT/TRACKER]"

                enriched_logs.append(f"Destination: {identifier}{warning} | Data Sent: {kb_sent} KB")

            raw_data_string = "\n".join(enriched_logs)

            # Updated Prompt for Privacy Auditing
            prompt = (
                "You are a strict data privacy and cybersecurity analyst. Review this packet capture data.\n"
                "Focus on identifying data brokers, telemetry, ad trackers, and any destinations marked as 🚨 [PRIVACY THREAT/TRACKER].\n"
                "Provide a bulleted summary calling out the worst privacy offenders and security risks.\n\n"
                f"Data:\n{raw_data_string}"
            )

            try:
                response = ollama.chat(
                    model='qwen3:4b-instruct',
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.1}
                )
                summary = f"RAW PACKET DATA (Top 15 Destinations):\n{raw_data_string}\n\nAI PRIVACY & SECURITY ANALYSIS:\n{response['message']['content'].strip()}"
                
                self.root.after(0, self.update_display, summary)
                self.log_to_file(summary)
                
            except Exception as e:
                self.root.after(0, self.update_display, f"AI offline. Raw Data:\n{raw_data_string}")
            
            self.root.after(0, self.status_var.set, "Sniffing...")

    def update_display(self, text):
        timestamp = time.strftime('%H:%M:%S')
        new_entry = f"--- [REPORT @ {timestamp}] ---\n{text}\n\n{'='*80}\n\n"
        
        self.display.config(state=tk.NORMAL)
        self.display.insert(tk.END, new_entry)
        self.display.see(tk.END)
        self.display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetMonitorApp(root)
    root.mainloop()
