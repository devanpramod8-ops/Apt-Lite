# modules/ai_engine.py — OpenRouter AI finding text generator

import requests
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_API_URL


def query_openrouter(prompt: str) -> str:
    """
    Send prompt to OpenRouter API.
    Returns response text.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://apt-lite.local",
        "X-Title":       "APT-Lite"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role":    "system",
                "content": "You are a professional cybersecurity analyst writing formal VAPT reports. Always respond in structured format exactly as instructed."
            },
            {
                "role":    "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens":  500
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers = headers,
            json    = payload,
            timeout = 30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return "AI unavailable: Connection error."
    except requests.exceptions.Timeout:
        return "AI unavailable: Request timed out."
    except KeyError:
        return "AI unavailable: Unexpected response format."
    except Exception as e:
        return f"AI generation failed: {str(e)}"


def enrich_finding(finding: dict) -> dict:
    """
    Takes a finding dict.
    Uses OpenRouter to generate description, impact, remediation.
    Returns enriched finding.
    """

    port     = finding["port"]
    title    = finding["title"]
    service  = finding["service"]
    version  = finding["version"]
    product  = finding["product"]
    severity = finding["severity"]
    reason   = finding["reason"]

    prompt = f"""You are writing a professional VAPT report finding.

Finding Details:
- Title: {title}
- Port: {port}
- Service: {service}
- Product: {product}
- Version: {version}
- Severity: {severity}
- Initial Reason: {reason}

Respond ONLY in this exact format with no extra text:
Description: <2-3 sentence technical description of the security risk>
Impact: <2-3 sentence explanation of what an attacker could do if exploited>
Remediation: <2-3 sentence actionable fix recommendation>"""

    raw = query_openrouter(prompt)

    description = ""
    impact      = ""
    remediation = ""

    for line in raw.splitlines():
        line = line.strip()
        if line.lower().startswith("description:"):
            description = line[len("description:"):].strip()
        elif line.lower().startswith("impact:"):
            impact = line[len("impact:"):].strip()
        elif line.lower().startswith("remediation:"):
            remediation = line[len("remediation:"):].strip()

    finding["description"] = description or reason
    finding["impact"]      = impact      or "Impact assessment pending manual review."
    finding["remediation"] = remediation or "Consult security team for remediation guidance."

    return finding


def enrich_all_findings(findings: list) -> list:
    """
    Enrich all findings with AI-generated text.
    """
    enriched = []
    for i, finding in enumerate(findings):
        print(f"[AI] Enriching finding {i+1}/{len(findings)}: {finding['title']}")
        enriched.append(enrich_finding(finding))
    return enriched
