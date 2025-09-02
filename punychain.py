#!/usr/bin/env python3
"""
PunyChain - Homoglyph Generator + Header Scanner + Weak CSP Detector + POC Builder
Author: samael_0x4
GitHub: https://github.com/samael0x4/PunyChain

This tool helps bug bounty hunters and security researchers by:
1. Generating homoglyph (punycode) variants of alphabets or domains.
2. Scanning target websites for security headers.
3. Detecting weak CSP (Content-Security-Policy).
4. Building simple PoC payloads when chaining homoglyphs with CSP misconfigs.

Usage Example (after installation):
-----------------------------------
$ punychain -h
$ punychain -a a
$ punychain -d tesla.com
$ punychain -u https://target.com
"""

import argparse
import requests
from colorama import Fore, Style, init
import idna

# Initialize colorama for colored CLI output
init(autoreset=True)

# --------------------------------------
# Homoglyph Variants
# --------------------------------------
HOMOGLYPHS = {
    "a": ["à", "á", "â", "ã", "ä", "å", "ɑ", "а"],
    "e": ["è", "é", "ê", "ë", "℮", "е"],
    "i": ["ì", "í", "î", "ï", "ι", "і"],
    "o": ["ò", "ó", "ô", "õ", "ö", "ο", "о", "օ"],
    "u": ["ù", "ú", "û", "ü", "μ", "ս"],
    "c": ["ç", "ϲ", "с"],
    "A": ["À", "Á", "Â", "Ã", "Ä", "Å", "А"],
    "E": ["È", "É", "Ê", "Ë", "Е"],
    "I": ["Ì", "Í", "Î", "Ï", "І"],
    "O": ["Ò", "Ó", "Ô", "Õ", "Ö", "О"],
    "U": ["Ù", "Ú", "Û", "Ü", "Ս"],
    "C": ["Ç", "Ϲ", "С"],
}

# --------------------------------------
# Generate homoglyphs for a single alphabet
# --------------------------------------
def generate_for_alphabet(letter):
    if letter in HOMOGLYPHS:
        print(Fore.CYAN + f"\n[+] Homoglyphs for '{letter}':")
        for char in HOMOGLYPHS[letter]:
            print("   " + char)
    else:
        print(Fore.RED + "[!] No homoglyphs available for this character.")

# --------------------------------------
# Generate homoglyph domains from input
# --------------------------------------
def generate_for_domain(domain):
    print(Fore.CYAN + f"\n[+] Homoglyph domain variants for: {domain}")
    for letter, variants in HOMOGLYPHS.items():
        if letter.lower() in domain.lower():
            for variant in variants:
                new_domain = domain.replace(letter, variant)
                try:
                    puny = idna.encode(new_domain).decode()
                    print(f"   {new_domain}  -->  {puny}")
                except Exception:
                    pass

# --------------------------------------
# Header Scanner
# --------------------------------------
def scan_headers(url):
    print(Fore.CYAN + f"\n[+] Scanning headers for: {url}")
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        # Show security-related headers
        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "Referrer-Policy",
        ]

        for h in security_headers:
            if h in headers:
                print(Fore.GREEN + f"[FOUND] {h}: {headers[h]}")
            else:
                print(Fore.RED + f"[MISSING] {h}")

        # Weak CSP detection
        if "Content-Security-Policy" in headers:
            csp = headers["Content-Security-Policy"]
            if "*" in csp or "http:" in csp:
                print(Fore.YELLOW + "[!] Weak CSP detected → Potential for homoglyph injection!")
                print(Fore.MAGENTA + f"[POC] Try hosting a script on homoglyph domain and inject via CSP: {csp}")

    except Exception as e:
        print(Fore.RED + f"[!] Error fetching {url}: {e}")

# --------------------------------------
# Main function (entry point for setup.py)
# --------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PunyChain - Homoglyph Generator + Header Scanner + Weak CSP Detector")
    parser.add_argument("-a", "--alphabet", help="Generate homoglyphs for a single alphabet (e.g. -a a)")
    parser.add_argument("-d", "--domain", help="Generate homoglyph variants for a domain (e.g. -d tesla.com)")
    parser.add_argument("-u", "--url", help="Scan target URL for headers and weak CSP (e.g. -u https://target.com)")

    args = parser.parse_args()

    if args.alphabet:
        generate_for_alphabet(args.alphabet)
    elif args.domain:
        generate_for_domain(args.domain)
    elif args.url:
        scan_headers(args.url)
    else:
        parser.print_help()

# Standard Python entry point
if __name__ == "__main__":
    main()
