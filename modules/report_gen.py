# modules/report_gen.py — HTML VAPT report generator

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config import REPORTS_DIR, APP_NAME, APP_VERSION


def generate_report(project: str, target: str, hostname: str,
                    scan_type: str, findings: list, notes: str = "") -> str:
    """
    Generate HTML VAPT report from findings.
    Returns path to saved report.
    """

    # Count severities
    severity_counts = {
        "Critical":      0,
        "High":          0,
        "Medium":        0,
        "Low":           0,
        "Informational": 0
    }

    for f in findings:
        sev = f.get("severity", "Informational")
        if sev in severity_counts:
            severity_counts[sev] += 1

    # Build context for template
    context = {
        "app_name":        APP_NAME,
        "app_version":     APP_VERSION,
        "project":         project,
        "target":          target,
        "hostname":        hostname or "N/A",
        "scan_type":       scan_type,
        "notes":           notes,
        "findings":        findings,
        "severity_counts": severity_counts,
        "total_findings":  len(findings),
        "report_date":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer":      (
            "This report was generated using APT-Lite for authorized "
            "lab and educational purposes only. Unauthorized use of this "
            "tool against systems without explicit permission is illegal."
        )
    }

    # Load Jinja2 template
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    # Render HTML
    html_output = template.render(context)

    # Save report
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(REPORTS_DIR, f"report_{project}_{timestamp}.html")

    with open(report_file, "w") as f:
        f.write(html_output)

    print(f"[REPORT] Report saved to {report_file}")
    return report_file
