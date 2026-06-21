# modules/risk_engine.py — Map ports/services to risks and severity

# Rule-based risk mapping
RISK_RULES = {
    21:   {"title": "FTP Service Exposed",
           "severity": "High",
           "reason": "FTP transmits data in plaintext. Anonymous access may be enabled."},
    22:   {"title": "SSH Service Exposed",
           "severity": "Low",
           "reason": "SSH is generally secure but older versions may have vulnerabilities."},
    23:   {"title": "Telnet Service Exposed",
           "severity": "Critical",
           "reason": "Telnet sends all data including credentials in plaintext."},
    25:   {"title": "SMTP Service Exposed",
           "severity": "Medium",
           "reason": "Open SMTP may allow mail relaying or user enumeration."},
    53:   {"title": "DNS Service Exposed",
           "severity": "Medium",
           "reason": "DNS may allow zone transfers leaking internal hostnames."},
    80:   {"title": "HTTP Web Service Exposed",
           "severity": "Medium",
           "reason": "Unencrypted web service. May expose sensitive data or admin panels."},
    110:  {"title": "POP3 Service Exposed",
           "severity": "Medium",
           "reason": "POP3 may transmit credentials in plaintext."},
    139:  {"title": "NetBIOS Service Exposed",
           "severity": "High",
           "reason": "NetBIOS can leak system info and enable SMB attacks."},
    443:  {"title": "HTTPS Web Service Exposed",
           "severity": "Informational",
           "reason": "Encrypted web service. Check for weak TLS/SSL configurations."},
    445:  {"title": "SMB Service Exposed",
           "severity": "Critical",
           "reason": "SMB is commonly exploited. EternalBlue and ransomware use this port."},
    1433: {"title": "MSSQL Database Exposed",
           "severity": "Critical",
           "reason": "Database port exposed. Risk of data breach or SQL injection."},
    3306: {"title": "MySQL Database Exposed",
           "severity": "Critical",
           "reason": "Database port exposed to network. Should not be publicly accessible."},
    3389: {"title": "RDP Service Exposed",
           "severity": "High",
           "reason": "Remote Desktop exposed. Risk of brute force and BlueKeep exploits."},
    5900: {"title": "VNC Service Exposed",
           "severity": "High",
           "reason": "VNC may allow remote desktop access with weak or no authentication."},
    8080: {"title": "HTTP Alternate Port Exposed",
           "severity": "Medium",
           "reason": "Alternate HTTP port. May host admin panels or dev services."},
    8443: {"title": "HTTPS Alternate Port Exposed",
           "severity": "Low",
           "reason": "Alternate HTTPS port. Verify certificate and service configuration."},
}

def map_risks(parsed_result: dict) -> list:
    """
    Takes parsed scan result.
    Returns list of findings with severity.
    """

    findings = []

    for port_info in parsed_result.get("ports", []):
        port    = port_info["port"]
        service = port_info["service"]
        version = port_info["version"]
        product = port_info["product"]

        if port in RISK_RULES:
            rule = RISK_RULES[port]
            findings.append({
                "port":        port,
                "service":     service,
                "product":     product,
                "version":     version,
                "title":       rule["title"],
                "severity":    rule["severity"],
                "reason":      rule["reason"],
                "description": "",   # filled by AI engine
                "impact":      "",   # filled by AI engine
                "remediation": ""    # filled by AI engine
            })
        else:
            # Unknown port — informational
            findings.append({
                "port":        port,
                "service":     service,
                "product":     product,
                "version":     version,
                "title":       f"Unknown Service on Port {port}",
                "severity":    "Informational",
                "reason":      "Service not in known risk ruleset. Manual review recommended.",
                "description": "",
                "impact":      "",
                "remediation": ""
            })

    return findings
