# modules/cve_lookup.py — CVE lookup via NVD API (free, no key needed)

import requests
import time

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def search_cves(service: str, version: str, max_results: int = 3) -> list:
    """
    Search NVD for CVEs matching service and version.
    Returns list of CVE dicts.
    """

    if not service:
        return []

    keyword = service
    if version:
        keyword = f"{service} {version}"

    params = {
        "keywordSearch":  keyword,
        "resultsPerPage": max_results
    }

    try:
        response = requests.get(NVD_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        cves = []
        for item in data.get("vulnerabilities", []):
            cve    = item.get("cve", {})
            cve_id = cve.get("id", "N/A")

            descriptions = cve.get("descriptions", [])
            desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "No description.")

            score    = "N/A"
            severity = "N/A"
            metrics  = cve.get("metrics", {})

            if "cvssMetricV31" in metrics:
                cvss     = metrics["cvssMetricV31"][0]["cvssData"]
                score    = cvss.get("baseScore", "N/A")
                severity = cvss.get("baseSeverity", "N/A")
            elif "cvssMetricV2" in metrics:
                cvss     = metrics["cvssMetricV2"][0]["cvssData"]
                score    = cvss.get("baseScore", "N/A")
                severity = metrics["cvssMetricV2"][0].get("baseSeverity", "N/A")

            cves.append({
                "id":          cve_id,
                "description": desc[:300] + "..." if len(desc) > 300 else desc,
                "score":       score,
                "severity":    severity,
                "url":         f"https://nvd.nist.gov/vuln/detail/{cve_id}"
            })

        time.sleep(6)
        return cves

    except requests.exceptions.Timeout:
        return [{"id": "Timeout", "description": "NVD lookup timed out.",
                 "score": "N/A", "severity": "N/A", "url": ""}]
    except Exception as e:
        return [{"id": "Error", "description": str(e),
                 "score": "N/A", "severity": "N/A", "url": ""}]


def enrich_findings_with_cves(findings: list) -> list:
    """
    Add CVE data to each finding.
    """
    for i, finding in enumerate(findings):
        service = finding.get("service", "")
        version = finding.get("version", "")
        product = finding.get("product", "")

        print(f"[CVE] Looking up CVEs for: {product} {service} {version}")

        search_term     = product if product else service
        finding["cves"] = search_cves(search_term, version)

    return findings
