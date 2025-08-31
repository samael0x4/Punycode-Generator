#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: samael_0x4
Tool: punycode_gen
Description: A hacker-style tool to generate homoglyphs (single alphabet variants) 
             or punycode (domain variants).
"""

import sys

# ---------------- Banner ---------------- #
def banner():
    print(r"""
██████╗ ██╗   ██╗███╗   ██╗██╗   ██╗ ██████╗ ██████╗ ███████╗
██╔══██╗██║   ██║████╗  ██║╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║██╔██╗ ██║ ╚████╔╝ ██║   ██║██████╔╝███████╗
██╔═══╝ ██║   ██║██║╚██╗██║  ╚██╔╝  ██║   ██║██╔═══╝ ╚════██║
██║     ╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝██║     ███████║
╚═╝      ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚══════╝
                 Punycode & Homoglyph Generator
                    coded by samael_0x4
    """)

# ---------------- Homoglyph Variants ---------------- #
# Unicode homoglyph variants for alphabets
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

# ---------------- Functions ---------------- #
def generate_homoglyphs(letter):
    """Generate homoglyphs for a single alphabet"""
    if letter in homoglyphs:
        print(f"\n[+] Homoglyph variants for '{letter}':\n")
        for var in homoglyphs[letter]:
            print(var)
    else:
        print("\n[-] No homoglyphs found for this character. Try a-z or A-Z.")

def generate_punycode(domain):
    """Generate punycode for domain"""
    try:
        puny = domain.encode("idna").decode("utf-8")
        print(f"\n[+] Domain: {domain}")
        print(f"[+] Punycode: {puny}")
    except Exception as e:
        print(f"[-] Error encoding domain: {e}")

# ---------------- Main ---------------- #
def main():
    banner()
    while True:
        print("\nChoose an option:")
        print(" 1) Generate homoglyphs for single alphabet")
        print(" 2) Generate punycode for a domain")
        print(" 3) Exit")
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            letter = input("\nEnter Alphabet (a-z or A-Z): ").strip()
            generate_homoglyphs(letter)

        elif choice == "2":
            domain = input("\nEnter Domain (example: google.com): ").strip()
            generate_punycode(domain)

        elif choice == "3":
            print("\n[!] Exiting... Stay Hacker! 👾\n")
            sys.exit(0)

        else:
            print("[-] Invalid choice, try again.")

if __name__ == "__main__":
    main()
