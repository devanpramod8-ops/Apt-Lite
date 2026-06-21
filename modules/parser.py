# modules/parser.py — Parse nmap results into structured JSON

def parse_scan(nm, target: str) -> dict:
    """
    Takes nmap PortScanner object.
    Returns structured dict of findings.
    """

    result = {
        "target":   target,
        "hostname": "",
        "state":    "",
        "ports":    []
    }

    # Check host exists in scan
    if target not in nm.all_hosts():
        result["state"] = "host not found"
        return result

    host = nm[target]

    # Hostname
    hostnames = host.hostnames()
    if hostnames:
        result["hostname"] = hostnames[0].get("name", "")

    # Host state
    result["state"] = host.state()

    # Loop protocols
    for proto in host.all_protocols():
        ports = host[proto].keys()
        for port in sorted(ports):
            port_data = host[proto][port]

            result["ports"].append({
                "port":     port,
                "protocol": proto,
                "state":    port_data.get("state", ""),
                "service":  port_data.get("name", ""),
                "product":  port_data.get("product", ""),
                "version":  port_data.get("version", ""),
                "extrainfo":port_data.get("extrainfo", "")
            })

    return result
