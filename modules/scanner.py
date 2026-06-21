# modules/scanner.py — Nmap scan runner

import nmap
import os
from datetime import datetime
from config import SCANS_DIR

def run_scan(target: str, scan_type: str = "basic") -> dict:
    """
    Run Nmap scan against target.
    Returns structured dict with raw results.
    """

    nm = nmap.PortScanner()

    # Choose flags based on scan type
    flags = {
        "basic":   "-sV --open",
        "full":    "-sV -sC --open",
        "stealth": "-sS -sV --open",
        "udp":     "-sU -sV --open"
    }.get(scan_type, "-sV --open")

    print(f"[*] Starting scan on {target} with flags: {flags}")

    try:
        nm.scan(hosts=target, arguments=flags)
    except Exception as e:
        return {"error": str(e), "target": target}

    # Save raw XML output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_file  = os.path.join(SCANS_DIR, f"scan_{timestamp}.xml")

    with open(xml_file, "w") as f:
        f.write(nm.get_nmap_last_output().decode("utf-8", errors="ignore"))

    print(f"[*] Raw scan saved to {xml_file}")

    return {
        "target":    target,
        "scan_type": scan_type,
        "timestamp": timestamp,
        "xml_file":  xml_file,
        "nm_object": nm
    }
