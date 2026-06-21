# 🔐 APT-Lite — AI-Assisted Pentest Automation Toolkit

<div align="center">

![APT-Lite Banner](https://img.shields.io/badge/APT--Lite-v1.0-00ff41?style=for-the-badge&logo=linux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Nmap](https://img.shields.io/badge/Scanner-Nmap-red?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-OpenRouter-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A Python-based AI-powered cybersecurity tool that automates the full VAPT workflow —
from reconnaissance to professional report generation.**

</div>

---

## 📌 What is APT-Lite?

APT-Lite is an **AI-Assisted Penetration Testing Automation Toolkit** built in Python.
It simulates a real-world Vulnerability Assessment and Penetration Testing (VAPT) workflow
by combining automated scanning, intelligent risk analysis, CVE correlation, and
AI-generated professional reporting — all in one tool.

This project was built as a cybersecurity portfolio project to demonstrate practical
knowledge of the full pentest lifecycle including:

- Active reconnaissance and service enumeration
- Risk-based vulnerability classification
- CVE correlation with real vulnerability databases
- AI-assisted professional finding generation
- VAPT-standard report creation

> ⚠️ **Legal Notice:** This tool is strictly for authorized lab and educational use only.
> Unauthorized scanning of systems without explicit permission is illegal.

---

## ⚡ Key Features

| Feature | Description |
|---|---|
| 🔍 Nmap Scanner | 7 scan profiles — basic, full, stealth, OS detect, vuln scripts, aggressive, complete |
| 📡 Service Enumeration | Detects open ports, service names, product names, and versions |
| ⚠️ Risk Engine | Rule-based mapping of 16+ services to severity levels (Critical to Informational) |
| 🔴 CVE Lookup | Queries NVD API for real CVEs per finding |
| 🤖 AI Enrichment | OpenRouter LLM generates Description, Impact, and Remediation per finding |
| 📄 VAPT Report | Full professional HTML report with executive summary, findings, CVEs |
| 🗄️ Scan History | Stores all past scans and reports in local SQLite database |
| 💻 Hacker UI | Dark terminal-themed Streamlit UI with Matrix rain animations |

---

## 🖥️ How It Works
[ User Input ]

│

▼

[ Nmap Scan ] ──► Detect open ports, services, versions

│

▼

[ Parser ] ──► Extract structured data from scan results

│

▼

[ Risk Engine ] ──► Map services to risk rules and assign severity

│

▼

[ CVE Lookup ] ──► Query NVD API for known CVEs per service

│

▼

[ AI Engine ] ──► Generate professional finding text via OpenRouter

│

▼

[ Report Generator ] ──► Build full VAPT HTML report via Jinja2

│

▼

[ SQLite Storage ] ──► Save scan history and report path

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|---|---|---|
| Language | Python 3 | Core language |
| UI | Streamlit | Fast professional UI without HTML/JS |
| Scanner | Nmap + python-nmap | Industry standard recon tool |
| AI | OpenRouter API | Access to powerful free LLMs |
| CVE Data | NVD REST API | Official US government CVE database |
| Reporting | Jinja2 + HTML | Professional dynamic report templating |
| Storage | SQLite | Zero-config local scan history |

---

## 📁 Project Structure
apt-lite/

├── app.py                  # Streamlit UI entry point

├── config.py               # API keys, paths, scan profiles

├── config.example.py       # Safe config template

├── requirements.txt        # Python dependencies

├── README.md

├── modules/

│   ├── init.py

│   ├── scanner.py          # Nmap scan runner

│   ├── parser.py           # Parser to structured JSON

│   ├── risk_engine.py      # Service to risk/severity mapping

│   ├── ai_engine.py        # OpenRouter AI finding generation

│   ├── report_gen.py       # Jinja2 HTML VAPT report

│   ├── storage.py          # SQLite scan history

│   └── cve_lookup.py       # NVD API CVE lookup

├── templates/

│   └── report.html         # VAPT report template

├── reports/                # Generated reports (gitignored)

├── scans/                  # Raw Nmap output (gitignored)

└── db/                     # SQLite database (gitignored)

---

## 🚀 Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/devanpramod8-ops/Apt-Lite.git
cd Apt-Lite
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Nmap
```bash
sudo apt install nmap
```

### 4. Set up config
```bash
cp config.example.py config.py
nano config.py
```

Add your OpenRouter API key:
```python
OPENROUTER_API_KEY = "your-openrouter-api-key-here"
OPENROUTER_MODEL   = "nex-agi/nex-n2-pro:free"
```

Get free API key at: https://openrouter.ai

### 5. Run the tool
```bash
streamlit run app.py
```

Open browser: http://localhost:8501

---

## 🎯 How To Use

### Step 1 — Enter target details
- Target IP or Domain
- Project or client name
- Scan profile
- Optional notes

### Step 2 — Choose options
- Enable AI Enrichment (OpenRouter)
- Enable CVE Lookup (NVD)

### Step 3 — Launch scan
Click LAUNCH SCAN. Tool runs Nmap, parses results, maps risks, looks up CVEs, generates AI findings.

### Step 4 — Download report
Click DOWNLOAD VAPT REPORT to get the full HTML report.

---

## 🔍 Scan Profiles

| Profile | Nmap Flags | Use Case |
|---|---|---|
| basic | -sV --open | Quick service detection |
| full | -sV -sC --open | Full scan with default scripts |
| stealth | -sS -sV --open | Low-noise SYN scan |
| os_detect | -sV -O --open | OS fingerprinting |
| vuln_scan | -sV --script vuln --open | NSE vulnerability scripts |
| aggressive | -A --open | Aggressive scan |
| complete | -A -O --script vuln --open | Full comprehensive scan |

---

## 📊 Severity Levels

| Severity | Examples |
|---|---|
| Critical | Telnet, SMB, open databases |
| High | FTP, RDP, VNC |
| Medium | HTTP, SMTP, DNS |
| Low | SSH, HTTPS alternate ports |
| Informational | Unknown services |

---

## 📄 Report Sections

1. Title Page
2. Executive Summary with severity cards
3. Scope
4. Methodology
5. Target Information
6. Findings Summary Table
7. Detailed Findings with CVEs
8. Conclusion

---

## 🧪 Safe Lab Targets

- 127.0.0.1 — Your own localhost
- Metasploitable2 VM
- DVWA — Damn Vulnerable Web App
- TryHackMe VPN targets
- HackTheBox VPN targets
- Your own home lab VMs

---

## 📦 Requirements
streamlit

python-nmap

jinja2

requests

---

## 👤 Author

Devan Pramod
- GitHub: https://github.com/devanpramod8-ops
- Email: devanpramod8@gmail.com

---

## 📜 License

MIT License — Free to use for educational and authorized testing purposes.

---

## ⚠️ Disclaimer

This tool is developed for educational purposes and authorized penetration testing only.
The author is not responsible for any misuse or illegal activity conducted with this tool.
Always obtain written permission before scanning any system.
