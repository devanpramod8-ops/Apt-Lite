# config.example.py — Copy this to config.py and fill in your values

import os

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SCANS_DIR   = os.path.join(BASE_DIR, "scans")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DB_DIR      = os.path.join(BASE_DIR, "db")
DB_PATH     = os.path.join(DB_DIR, "apt_lite.db")

OPENROUTER_API_KEY = "your-openrouter-api-key-here"
OPENROUTER_MODEL   = "nex-agi/nex-n2-pro:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

NMAP_SCAN_PROFILES = {
    "basic":      "-sV --open",
    "full":       "-sV -sC --open",
    "stealth":    "-sS -sV --open",
    "udp":        "-sU -sV --open",
    "os_detect":  "-sV -O --open",
    "vuln_scan":  "-sV --script vuln --open",
    "aggressive": "-A --open",
    "complete":   "-A -O --script vuln --open",
}

APP_NAME    = "APT-Lite"
APP_VERSION = "1.0"
