# app.py — APT-Lite Streamlit UI (Hacker Theme + Animations)

import streamlit as st
from modules.scanner import run_scan
from modules.parser import parse_scan
from modules.risk_engine import map_risks
from modules.ai_engine import enrich_all_findings
from modules.report_gen import generate_report
from modules.storage import init_db, save_scan, get_all_scans, get_scan_by_id
from modules.cve_lookup import enrich_findings_with_cves

init_db()

st.set_page_config(
    page_title="APT-Lite",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { font-family: 'Share Tech Mono', monospace; }

.stApp {
    background-color: #0a0a0a;
    color: #00ff41;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 10px; }

[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #00ff41;
}
[data-testid="stSidebar"] * {
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stTextInput input, .stTextArea textarea {
    background: #0d0d0d !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    caret-color: #00ff41;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    box-shadow: 0 0 10px #00ff41 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #0d0d0d !important;
    border: 1px solid #00ff41 !important;
    color: #00ff41 !important;
}
.stSelectbox svg { fill: #00ff41 !important; }
[data-baseweb="popover"] * {
    background: #0d0d0d !important;
    color: #00ff41 !important;
}

.stTextInput label, .stTextArea label,
.stSelectbox label, .stCheckbox label {
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stButton > button {
    background: transparent !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 14px !important;
    padding: 10px 30px !important;
    border-radius: 0px !important;
    text-transform: uppercase !important;
    letter-spacing: 3px !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: #00ff41 !important;
    color: #0a0a0a !important;
    box-shadow: 0 0 25px #00ff41, 0 0 50px #00ff41 !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #00ff41 !important;
    border: 1px solid #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 0px !important;
}
.stDownloadButton > button:hover {
    background: #00ff41 !important;
    color: #0a0a0a !important;
    box-shadow: 0 0 15px #00ff41 !important;
}

p, div, span, li { color: #00ff41; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #00ff41; }

/* ── ANIMATIONS ── */

/* Matrix rain canvas */
#matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    opacity: 0.07;
    pointer-events: none;
}

/* Glitch effect */
@keyframes glitch {
    0%   { text-shadow: 2px 0 #ff0000, -2px 0 #00ffff; }
    20%  { text-shadow: -2px 0 #ff0000, 2px 0 #00ffff; }
    40%  { text-shadow: 2px 2px #ff0000, -2px -2px #00ffff; }
    60%  { text-shadow: -2px 2px #ff0000, 2px -2px #00ffff; }
    80%  { text-shadow: 0 0 #ff0000, 0 0 #00ffff; }
    100% { text-shadow: 2px 0 #ff0000, -2px 0 #00ffff; }
}

/* Pulse glow */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 5px #00ff41, 0 0 10px #00ff41; }
    50%       { box-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41; }
}

/* Blink cursor */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}

/* Scan line */
@keyframes scanline {
    0%   { top: -10%; }
    100% { top: 110%; }
}

/* Typing */
@keyframes typing {
    from { width: 0; }
    to   { width: 100%; }
}

/* Fade in up */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.apt-header {
    border: 1px solid #00ff41;
    padding: 25px 30px;
    margin-bottom: 25px;
    background: #0d0d0d;
    position: relative;
    overflow: hidden;
    animation: pulse-glow 3s infinite;
}

.apt-header::before {
    content: '';
    position: absolute;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ff41, transparent);
    animation: scanline 3s linear infinite;
}

.apt-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 32px;
    font-weight: 900;
    color: #00ff41;
    letter-spacing: 6px;
    animation: glitch 4s infinite;
}

.apt-subtitle {
    font-size: 11px;
    color: #008f26;
    letter-spacing: 4px;
    margin-top: 8px;
}

.apt-status {
    font-size: 11px;
    color: #004d14;
    margin-top: 5px;
}

.blink {
    animation: blink 1s infinite;
    color: #00ff41;
}

.terminal-box {
    background: #0d0d0d;
    border: 1px solid #00ff41;
    border-radius: 0;
    padding: 15px 20px;
    margin: 15px 0;
    font-size: 12px;
    color: #008f26;
    animation: fadeInUp 0.5s ease;
}

.findings-header {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    color: #00ff41;
    letter-spacing: 3px;
    margin: 20px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #00ff41;
}

.warning-box {
    background: #1a0000;
    border: 1px solid #ff0000;
    padding: 10px 15px;
    margin: 15px 0;
    font-size: 12px;
    color: #ff4444;
    animation: fadeInUp 0.5s ease;
}

.scan-progress {
    width: 100%;
    height: 2px;
    background: #001a00;
    margin: 5px 0;
    position: relative;
    overflow: hidden;
}

.scan-progress::after {
    content: '';
    position: absolute;
    height: 100%;
    width: 30%;
    background: #00ff41;
    animation: scanning 1.5s linear infinite;
    box-shadow: 0 0 10px #00ff41;
}

@keyframes scanning {
    0%   { left: -30%; }
    100% { left: 130%; }
}
</style>

<!-- Matrix Rain Canvas -->
<canvas id="matrix-canvas"></canvas>

<script>
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()アイウエオカキクケコ';
const fontSize = 12;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawMatrix() {
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#00ff41';
    ctx.font = fontSize + 'px monospace';
    drops.forEach((y, i) => {
        const char = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(char, i * fontSize, y * fontSize);
        if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    });
}
setInterval(drawMatrix, 50);
</script>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class="apt-header">
    <div class="apt-title">⚡ APT-LITE</div>
    <div class="apt-subtitle">AI-ASSISTED PENTEST AUTOMATION TOOLKIT v1.0</div>
    <div class="apt-status">
        [ STATUS: ONLINE ] [ ENGINE: AI ] [ MODE: RECON ]
        <span class="blink">█</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
st.sidebar.markdown("""
<div style="font-family:'Orbitron',monospace; font-size:13px;
            color:#00ff41; letter-spacing:2px; margin-bottom:20px;
            padding-bottom:10px; border-bottom:1px solid #00ff41;">
    [ NAVIGATION ]
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["🖥  New Scan", "📁  Scan History"])

st.sidebar.markdown("""
<div style="margin-top:30px; font-size:11px; color:#004d14; line-height:2;">
    ▸ ENGINE: ONLINE<br>
    ▸ AI: OPENROUTER<br>
    ▸ CVE: NVD API<br>
    ▸ SCANNER: NMAP<br>
    ▸ REPORT: HTML<br>
</div>
""", unsafe_allow_html=True)

# ══ NEW SCAN ══
if "New Scan" in page:

    st.markdown("""
    <div class="terminal-box">
        > SYSTEM READY. INITIALIZE SCAN SESSION.<br>
        > ENTER TARGET PARAMETERS BELOW.<br>
        > AUTHORIZED USE ONLY. <span class="blink">_</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p style="color:#00ff41;font-size:11px;letter-spacing:2px;margin-bottom:4px;">TARGET IP / DOMAIN</p>', unsafe_allow_html=True)
        target = st.text_input("", placeholder="192.168.1.10", key="target", label_visibility="collapsed")

        st.markdown('<p style="color:#00ff41;font-size:11px;letter-spacing:2px;margin-bottom:4px;margin-top:10px;">PROJECT / CLIENT NAME</p>', unsafe_allow_html=True)
        project = st.text_input("", placeholder="Lab-Test-01", key="project", label_visibility="collapsed")

    with col2:
        st.markdown('<p style="color:#00ff41;font-size:11px;letter-spacing:2px;margin-bottom:4px;">SCAN PROFILE</p>', unsafe_allow_html=True)
        scan_type = st.selectbox("", [
            "basic", "full", "stealth",
            "os_detect", "vuln_scan",
            "aggressive", "complete"
        ], key="scan_type", label_visibility="collapsed")

        st.markdown('<p style="color:#00ff41;font-size:11px;letter-spacing:2px;margin-bottom:4px;margin-top:10px;">OPERATOR NOTES</p>', unsafe_allow_html=True)
        notes = st.text_area("", placeholder="Engagement notes...", key="notes", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        use_ai = st.checkbox("⚡ AI Enrichment (OpenRouter)", value=True)
    with col4:
        use_cve = st.checkbox("🔍 CVE Lookup (NVD)", value=True)

    st.markdown("""
    <div class="warning-box">
        ⚠ WARNING: Unauthorized scanning is illegal. Only scan systems
        you own or have explicit written permission to test.
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  LAUNCH SCAN", type="primary"):

        if not target or not project:
            st.error("[ ERROR ] Target and Project name required.")
        else:
            st.markdown(f"""
            <div class="terminal-box">
                > TARGET LOCKED: {target}<br>
                > PROFILE: {scan_type.upper()}<br>
                > INITIATING NMAP SCAN...<br>
                <div class="scan-progress"></div>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("[ SCANNING ] Nmap running..."):
                scan_result = run_scan(target, scan_type)

            if "error" in scan_result:
                st.error(f"[ FAILED ] {scan_result['error']}")
            else:
                st.success("[ OK ] Scan complete.")

                with st.spinner("[ PARSING ] Extracting port data..."):
                    parsed = parse_scan(scan_result["nm_object"], target)

                st.info(f"[ INFO ] Host: {parsed['state']} | Ports: {len(parsed['ports'])}")

                with st.spinner("[ ANALYSIS ] Risk mapping..."):
                    findings = map_risks(parsed)

                if use_cve and findings:
                    with st.spinner("[ CVE ] Querying NVD..."):
                        findings = enrich_findings_with_cves(findings)

                if use_ai and findings:
                    with st.spinner("[ AI ] Generating findings..."):
                        findings = enrich_all_findings(findings)

                with st.spinner("[ REPORT ] Building VAPT report..."):
                    report_path = generate_report(
                        project   = project,
                        target    = target,
                        hostname  = parsed.get("hostname", ""),
                        scan_type = scan_type,
                        findings  = findings,
                        notes     = notes
                    )

                save_scan(project, target, scan_type, findings, report_path, notes)

                st.success("[ COMPLETE ] VAPT Report generated.")

                st.markdown('<div class="findings-header">[ FINDINGS SUMMARY ]</div>', unsafe_allow_html=True)

                severity_color = {
                    "Critical":      "🔴",
                    "High":          "🟠",
                    "Medium":        "🟡",
                    "Low":           "🟢",
                    "Informational": "🔵"
                }

                for f in findings:
                    icon = severity_color.get(f["severity"], "⚪")
                    col_a, col_b, col_c, col_d = st.columns([1, 3, 2, 1])
                    col_a.markdown(f'<span style="color:#00ff41;">:{f["port"]}</span>', unsafe_allow_html=True)
                    col_b.markdown(f'<span style="color:#00ff41;">{f["title"]}</span>', unsafe_allow_html=True)
                    col_c.markdown(f'<span style="color:#008f26;">{f["service"]}</span>', unsafe_allow_html=True)
                    col_d.markdown(f'<span style="color:#00ff41;">{icon} {f["severity"]}</span>', unsafe_allow_html=True)

                    if f.get("cves"):
                        with st.expander(f"CVEs — port {f['port']}"):
                            for cve in f["cves"]:
                                st.markdown(
                                    f'<span style="color:#ff4444;">**{cve["id"]}**</span>'
                                    f' | Score: `{cve["score"]}` | Severity: `{cve["severity"]}`  \n'
                                    f'<span style="color:#008f26;">{cve["description"]}</span>  \n'
                                    f'[→ NVD]({cve["url"]})',
                                    unsafe_allow_html=True
                                )

                st.markdown("<br>", unsafe_allow_html=True)
                with open(report_path, "r") as rf:
                    st.download_button(
                        label     = "📄  DOWNLOAD VAPT REPORT",
                        data      = rf.read(),
                        file_name = f"vapt_report_{project}.html",
                        mime      = "text/html"
                    )

# ══ SCAN HISTORY ══
elif "Scan History" in page:

    st.markdown('<div class="findings-header">[ SCAN HISTORY DATABASE ]</div>', unsafe_allow_html=True)

    scans = get_all_scans()

    if not scans:
        st.markdown('<div class="terminal-box">> NO RECORDS FOUND. RUN A SCAN FIRST.</div>', unsafe_allow_html=True)
    else:
        for scan in scans:
            with st.expander(f"#{scan['id']} | {scan['project']} | {scan['target']} | {scan['timestamp']}"):
                st.markdown(f'<span style="color:#00ff41;">SCAN TYPE: {scan["scan_type"].upper()}</span>', unsafe_allow_html=True)
                st.markdown(f'<span style="color:#008f26;">REPORT: {scan["report_path"]}</span>', unsafe_allow_html=True)

                detail = get_scan_by_id(scan['id'])
                if detail.get("findings"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    for f in detail["findings"]:
                        st.markdown(
                            f'<span style="color:#00ff41;">▸ Port {f["port"]} | {f["title"]} | {f["severity"]}</span>',
                            unsafe_allow_html=True
                        )

                    with open(detail["report_path"], "r") as rf:
                        st.download_button(
                            label     = f"📄 DOWNLOAD REPORT #{scan['id']}",
                            data      = rf.read(),
                            file_name = f"vapt_report_{scan['project']}.html",
                            mime      = "text/html",
                            key       = f"dl_{scan['id']}"
                        )
