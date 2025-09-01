# PunyChain — Punycode / Homoglyph Recon & CSP Chain Tool
**PunyChain** (by `samael_0x4`) extends punycode/homoglyph recon with a header scanner, weak-CSP detector, and POC builder to help bug hunters test chained attack surfaces (homoglyphs → header misconfig → code load).

---

## Features
- Generate homoglyph variants for domains and single alphabet characters.
- Fetch headers and analyze Content-Security-Policy & security headers.
- Detect weak CSP indicators (`unsafe-inline`, wildcards, missing script-src).
- Generate local POC HTML snippets showing how a homoglyph-hosted script could be loaded.
- Optional DNS resolution check for generated homoglyph domains.

---

## Install (Linux / macOS / Windows)

```bash
# clone repo
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
```

# create venv (recommended)
```bash
python3 -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows PowerShell
```
# install deps
```bash
pip install -r requirements.txt
```
# run directly
```bash
python punychain.py -h
```

### 📋 Requirements

Python 3.x

### 🧑‍💻 Usage Examples
1) Show homoglyphs for a single character
```bash
python punychain.py -a a
```
2) Scan headers / CSP for a target
```bash
python punychain.py -d tesla.com --scan-headers
```
3) Generate homoglyph variants for a domain
```bash
python punychain.py -d tesla.com --generate
```
4) Generate variants + try DNS resolution + generate POC files
```bash
python punychain.py -d tesla.com --generate --resolve --build-pocs

# This will write poc_*.html files to current directory for quick review.
```
### How it helps bug hunters

Recon layer: find homoglyph domains that impersonate the target (used in phishing or resource hosting).

Detection layer: identify weak CSPs and missing headers that could allow external script loading.

POC layer: produce quick test files to demonstrate how a homoglyph-hosted script would be included if the CSP allows it.

### 📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.

### Ethics & Disclaimer

This tool is for authorized security testing only (bug bounty programs, pentests with permission, educational labs). Do NOT use this against systems you don't have permission to test. The author (samael_0x4) is not responsible for misuse.

### 💬 Support

GitHub: samael0x4 
Issues: Open an issue on this repo
