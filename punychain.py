#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
punychain.py
Punycode + Chain Tool (Homoglyph recon + header/CSP scanner + POC builder)
Author : samael_0x4
"""

import sys
import argparse
import socket
import idna
import requests
from urllib.parse import urlparse

# -------------------------
# Basic homoglyph mapping (extend as needed)
# -------------------------
homoglyphs = {
    "a": ["à", "á", "â", "ã", "ä", "å", "ɑ", "ạ", "ă", "ą", "ª", "ā"],
    "b": ["Ƅ", "ь", "ɓ", "ƅ", "ъ", "ʙ", "฿", "ḅ", "ḇ", "ƀ"],
    "c": ["ç", "ć", "č", "ċ", "ĉ", "ƈ", "ȼ", "ς"],
    "d": ["ď", "ḍ", "ḋ", "ḏ", "đ", "ɗ", "ð"],
    "e": ["è", "é", "ê", "ë", "ē", "ė", "ę", "ȩ", "ɇ", "ẹ"],
    "g": ["ğ", "ĝ", "ġ", "ģ", "ɡ", "ǵ", "ḡ"],
    "i": ["ì", "í", "î", "ï", "ĩ", "ī", "į", "ı", "ɨ"],
    "o": ["ò", "ó", "ô", "õ", "ö", "ō", "ø", "ǿ", "ọ", "ơ", "º"],
    "u": ["ù", "ú", "û", "ü", "ũ", "ū", "ŭ", "ů", "ű", "ų", "ư"],
    "A": ["À", "Á", "Â", "Ã", "Ä", "Å", "Ā", "Ą", "Ȧ", "Ǎ", "Α"],
    "B": ["Β", "ß", "฿", "Ƀ", "Ḃ", "Ḅ", "Ḇ"],
    "C": ["Ç", "Ć", "Č", "Ĉ", "Ċ", "Ƈ", "Ȼ"],
    "D": ["Ď", "Ḋ", "Ḍ", "Ḏ", "Đ", "Ð"],
    "E": ["È", "É", "Ê", "Ë", "Ē", "Ė", "Ę", "Ȩ", "Ẹ"],
    "O": ["Ò", "Ó", "Ô", "Õ", "Ö", "Ō", "Ø", "Ǿ", "Ọ", "Ơ", "Θ"],
    "U": ["Ù", "Ú", "Û", "Ü", "Ũ", "Ū", "Ŭ", "Ů", "Ű", "Ų", "Ư"]
}
# add uppercase for lower entries (for entries missing)
for k in list(homoglyphs.keys()):
    if k.islower():
        homoglyphs.setdefault(k.upper(), [c.upper() for c in homoglyphs[k] if c.isalpha()])

# -------------------------
# Helpers
# -------------------------
def to_punycode(s: str) -> str:
    """Return IDNA punycode representation of a unicode string (domain label)."""
    try:
        return idna.encode(s).decode('utf-8')
    except Exception:
        try:
            return s.encode('idna').decode('utf-8')
        except Exception:
            return "(no punycode)"

def generate_homoglyphs_for_domain(domain: str):
    """
    For domain (like example.com) generate variants for the main label.
    Returns list of candidate domain strings (unicode).
    """
    if not domain:
        return []
    parsed = urlparse(domain) if '//' in domain else None
    domain_clean = parsed.netloc if parsed else domain
    # split first label only (left-most) to generate variants
    parts = domain_clean.split('.')
    if len(parts) == 0:
        return []
    main = parts[0]
    rest = parts[1:]
    # For each char, choices = original + homoglyphs if exist
    choices = []
    for ch in main:
        if ch in homoglyphs:
            choices.append([ch] + homoglyphs[ch])
        else:
            choices.append([ch])
    # Build combinations (careful: exponential). We'll limit depth automatically for long main labels.
    max_combinations = 2000  # safety guard
    from itertools import product, islice
    combos = product(*choices)
    results = []
    for idx, combo in enumerate(combos):
        if idx >= max_combinations:
            break
        candidate_main = ''.join(combo)
        candidate = '.'.join([candidate_main] + rest) if rest else candidate_main
        results.append(candidate)
    return results

def resolve_domain(domain: str) -> bool:
    """Try DNS resolution for domain; return True if resolves."""
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

# -------------------------
# Header + CSP analysis
# -------------------------
def fetch_headers(target_url: str, timeout=10):
    """Fetch headers via GET (no body) and return headers dict (or None)."""
    try:
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
        resp = requests.get(target_url, timeout=timeout, allow_redirects=True, headers={'User-Agent': 'punychain/1.0'})
        return resp.status_code, resp.headers
    except Exception as e:
        return None, {"error": str(e)}

def analyze_security_headers(headers: dict):
    """Return analysis dict describing missing/weak headers."""
    report = {
        "has_csp": False,
        "csp": None,
        "weak_csp": False,
        "csp_issues": [],
        "missing_headers": [],
        "other_notes": []
    }

    if not headers or 'error' in headers:
        report["other_notes"].append(f"Error fetching headers: {headers.get('error') if isinstance(headers, dict) else headers}")
        return report

    csp = headers.get('Content-Security-Policy') or headers.get('content-security-policy')
    if csp:
        report["has_csp"] = True
        report["csp"] = csp
        # very simple heuristic checks for risky policies
        lower = csp.lower()
        if "unsafe-inline" in lower or "unsafe-eval" in lower:
            report["weak_csp"] = True
            report["csp_issues"].append("contains unsafe-inline or unsafe-eval")
        if "*" in lower or "data:" in lower or "http:" in lower:
            report["weak_csp"] = True
            report["csp_issues"].append("wildcard/data/http sources allowed")
        # if script-src missing but default-src present, still warn
        if "script-src" not in lower and "default-src" not in lower:
            report["weak_csp"] = True
            report["csp_issues"].append("no script-src or default-src directives")
    else:
        report["missing_headers"].append("Content-Security-Policy (missing)")

    # check other headers
    xfo = headers.get('X-Frame-Options') or headers.get('x-frame-options')
    if not xfo:
        report["missing_headers"].append("X-Frame-Options (missing)")
    hsts = headers.get('Strict-Transport-Security') or headers.get('strict-transport-security')
    if not hsts:
        report["missing_headers"].append("Strict-Transport-Security (missing)")

    csp_report = report
    return csp_report

# -------------------------
# POC builder
# -------------------------
def build_poc_html(target_site: str, attacker_domain: str):
    """
    Returns a simple HTML proof-of-concept that, if loaded by a page that allows attacker_domain
    by CSP/script-src, will load attacker script. This is a POC generator only (no auto-exploitation).
    """
    safe_attacker = attacker_domain
    poc = f"""<!-- PunyChain POC: load attacker JS from {safe_attacker} -->
<!doctype html>
<html>
<head><meta charset="utf-8"><title>PunyChain POC</title></head>
<body>
<h3>PunyChain POC for {target_site}</h3>
<!-- If the target's CSP allows scripts from {safe_attacker}, this script will run -->
<script src="https://{safe_attacker}/poc.js"></script>
</body>
</html>
"""
    return poc

# -------------------------
# CLI / menu
# -------------------------
def scan_and_suggest(target):
    print(f"[+] Scanning headers for: {target}")
    code, headers = fetch_headers(target)
    if code is None:
        print(f"[-] Failed to fetch headers: {headers.get('error')}")
        return
    print(f"[+] HTTP status: {code}")
    print("[+] Relevant headers:")
    for k in ('Content-Security-Policy', 'content-security-policy', 'X-Frame-Options', 'x-frame-options', 'Strict-Transport-Security', 'strict-transport-security'):
        if k in headers:
            print(f"  {k}: {headers[k]}")
    analysis = analyze_security_headers(headers)
    if analysis["has_csp"]:
        print("\n[+] CSP detected:")
        print(f"  {analysis['csp']}")
    else:
        print("\n[!] No CSP detected (or header absent)")

    if analysis["weak_csp"]:
        print("\n[!] Weak CSP indicators found:")
        for i in analysis["csp_issues"]:
            print("  -", i)
    if analysis["missing_headers"]:
        print("\n[!] Missing security headers:")
        for i in analysis["missing_headers"]:
            print("  -", i)

    # If CSP weak or missing, recommend homoglyph chaining
    if analysis["weak_csp"] or ("Content-Security-Policy" not in headers and "content-security-policy" not in headers):
        print("\n[+] Suggestion: try homoglyph domains for script-hosting & build POC snippets.")
    else:
        print("\n[+] CSP seems reasonably restrictive — homoglyph attack vector may be limited, still check edge cases.")

def run_homoglyph_and_chain(domain, resolve_check=False, build_pocs=False, max_show=30):
    print(f"[+] Generating homoglyph candidates for: {domain}")
    variants = generate_homoglyphs_for_domain(domain)
    if not variants:
        print("[-] No variants generated (domain parsing issue or empty).")
        return
    print(f"[+] Generated {len(variants)} variants (showing up to {max_show}):")
    shown = 0
    results = []
    for v in variants:
        puny = to_punycode(v)
        row = {"domain": v, "puny": puny}
        if resolve_check:
            row["resolves"] = resolve_domain(v)
        results.append(row)
        if shown < max_show:
            resolv = row.get("resolves", "N/A")
            print(f"  {v}  ->  {puny}  (resolves: {resolv})")
            shown += 1
    if len(variants) > max_show:
        print("  ... (truncated output)")

    if build_pocs:
        print("\n[+] Building POC HTML snippets for first homoglyph variants (not hosted):")
        for idx, r in enumerate(results[:min(10, len(results))]):
            poc = build_poc_html(domain, r["domain"])
            filename = f"poc_{idx+1}_{r['domain'].replace('.', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(poc)
            print(f"  - Saved POC to {filename}")

def main_cli():
    parser = argparse.ArgumentParser(prog="punychain", description="PunyChain: homoglyph recon + header/CSP scanner + POC builder")
    parser.add_argument("-d", "--domain", help="Target domain or host (example: example.com or https://example.com)")
    parser.add_argument("-a", "--alphabet", help="Show homoglyphs for a single alphabet character (a/A)")
    parser.add_argument("--scan-headers", action="store_true", help="Fetch and analyze headers/CSP for the target domain")
    parser.add_argument("--generate", action="store_true", help="Generate homoglyph variants for the domain")
    parser.add_argument("--resolve", action="store_true", help="Try DNS resolve generated variants")
    parser.add_argument("--build-pocs", action="store_true", help="Build local POC HTML files for variants (saved to cwd)")
    args = parser.parse_args()

    if args.alphabet:
        ch = args.alphabet.strip()
        if len(ch) != 1:
            print("Please supply a single alphabet character.")
            sys.exit(1)
        # show homoglyphs for character
        arr = homoglyphs.get(ch) or homoglyphs.get(ch.upper())
        if not arr:
            print("No homoglyphs found for that character.")
            sys.exit(0)
        print(f"Homoglyphs for '{ch}':")
        for g in arr:
            print(f"  {g}   ->   {to_punycode(g)}")
        sys.exit(0)

    if not args.domain:
        print("Use -d <domain> or -a <alphabet>. See -h for help.")
        sys.exit(0)

    domain = args.domain.strip()
    if args.scan_headers:
        scan_and_suggest(domain)
    if args.generate:
        run_homoglyph_and_chain(domain, resolve_check=args.resolve, build_pocs=args.build_pocs)
    if not args.scan_headers and not args.generate:
        # default interactive behavior
        print("\nRunning combined flow: scan headers + generate variants (no resolve, no POCs).")
        scan_and_suggest(domain)
        run_homoglyph_and_chain(domain, resolve_check=False, build_pocs=False)

if __name__ == "__main__":
    main_cli()
