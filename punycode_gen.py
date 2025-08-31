#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Punycode / Homoglyph Generator Tool
# Author   : samael_0x4
# Version  : 1.1
# Purpose  : Generate homoglyphs & punycode for alphabets or full domains.
# Use Case : Bug bounty, phishing detection, IDN homograph attacks testing.
#

import sys
import itertools

# ================================
# Homoglyph mapping dictionary
# ================================
homoglyphs = {
    "a": ["à", "á", "â", "ã", "ä", "å", "ā", "ă", "ą", "ɑ", "α", "а"],
    "b": ["ƀ", "ƃ", "ɓ", "β", "Ъ", "Ь", "ъ", "ь"],
    "c": ["ç", "ć", "ĉ", "ċ", "č", "ƈ", "ς", "с"],
    "d": ["ď", "đ", "ḋ", "ḑ", "ḍ", "ḓ", "ɖ", "ԁ"],
    "e": ["è", "é", "ê", "ë", "ē", "ĕ", "ė", "ę", "ě", "ε", "е"],
    "f": ["ƒ", "ḟ", "ғ", "ſ"],
    "g": ["ğ", "ĝ", "ġ", "ģ", "ɡ", "ǵ", "ḡ", "ց"],
    "h": ["ĥ", "ħ", "ɦ", "н", "һ"],
    "i": ["ì", "í", "î", "ï", "ī", "ĭ", "į", "ı", "ɩ", "ι", "і"],
    "j": ["ĵ", "ј", "ʝ"],
    "k": ["ķ", "ƙ", "ǩ", "κ", "к"],
    "l": ["ĺ", "ļ", "ľ", "ŀ", "ł", "ι", "ӏ", "ⅼ"],
    "m": ["ɱ", "м", "ṃ"],
    "n": ["ñ", "ń", "ņ", "ň", "ŉ", "ŋ", "η", "п"],
    "o": ["ò", "ó", "ô", "õ", "ö", "ō", "ŏ", "ő", "ο", "о", "օ"],
    "p": ["ṕ", "ṗ", "ρ", "р"],
    "q": ["զ", "ʠ"],
    "r": ["ŕ", "ŗ", "ř", "г"],
    "s": ["ś", "ŝ", "ş", "š", "ѕ", "ṡ"],
    "t": ["ţ", "ť", "ŧ", "τ", "т"],
    "u": ["ù", "ú", "û", "ü", "ū", "ŭ", "ů", "ű", "ų", "υ", "ц"],
    "v": ["ν", "ѵ", "ṽ"],
    "w": ["ŵ", "ẁ", "ẃ", "ẅ", "ш"],
    "x": ["ẋ", "ẍ", "х", "χ"],
    "y": ["ý", "ÿ", "ŷ", "ў", "у"],
    "z": ["ź", "ż", "ž", "ƶ", "ẓ", "ȥ", "ʐ", "ᴢ"],
}

# Add uppercase versions automatically
for k in list(homoglyphs.keys()):
    homoglyphs[k.upper()] = [c.upper() for c in homoglyphs[k] if c.isalpha()]


# ================================
# Banner
# ================================
def banner():
    print(r"""
   ██████╗ ██╗   ██╗███╗   ██╗██╗   ██╗ ██████╗ ██████╗ ███████╗
   ██╔══██╗██║   ██║████╗  ██║██║   ██║██╔═══██╗██╔══██╗██╔════╝
   ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██║   ██║██████╔╝███████╗
   ██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║██║   ██║██╔═══╝ ╚════██║
   ██║     ╚██████╔╝██║ ╚████║╚██████╔╝╚██████╔╝██║     ███████║
   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝
             PUNYCODE / HOMOGLYPH GENERATOR v1.1
                   coded by: samael_0x4
    """)


# ================================
# Single alphabet homoglyphs
# ================================
def show_homoglyphs(letter):
    """Show homoglyphs + punycode for a single letter"""
    if letter in homoglyphs:
        print(f"\n[+] Homoglyphs for '{letter}':\n")
        results = []
        for glyph in homoglyphs[letter]:
            try:
                punycode = glyph.encode("idna").decode("utf-8")
            except Exception:
                punycode = "(no punycode)"
            line = f"{glyph}   ->   {punycode}"
            results.append(line)
            print(line)

        save_results(results)

    else:
        print("⚠️ No homoglyphs available for this letter.")


# ================================
# Word / Domain homoglyph variants
# ================================
def generate_domain_variants(word):
    """Generate punycode variants for a full word/domain"""
    word = word.strip()
    print(f"\n[+] Variants for '{word}':\n")

    # Split domain (avoid replacing dots)
    parts = word.split(".")
    main = parts[0]

    # For each character, collect homoglyph choices
    choices = []
    for ch in main:
        if ch in homoglyphs:
            choices.append([ch] + homoglyphs[ch])
        else:
            choices.append([ch])

    results = []

    # Generate ALL combinations (⚠️ can be huge for long words!)
    for combo in itertools.product(*choices):
        candidate = "".join(combo)
        domain = candidate + ("." + ".".join(parts[1:]) if len(parts) > 1 else "")
        try:
            punycode = domain.encode("idna").decode("utf-8")
        except Exception:
            punycode = "(no punycode)"
        line = f"{domain}   ->   {punycode}"
        results.append(line)
        print(line)

    save_results(results)


# ================================
# Save Results Option
# ================================
def save_results(results):
    """Ask user to save results to file"""
    save = input("\n[?] Save results to file? (y/n): ").strip().lower()
    if save == "y":
        filename = "punycode_output.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print(f"[+] Results saved to {filename}")


# ================================
# Main menu
# ================================
def main():
    banner()
    print("Select an option:")
    print(" [a] Single Alphabet")
    print(" [b] Word / Domain")
    choice = input("\n> ").strip().lower()

    if choice == "a":
        letter = input("Enter Alphabet (a-z or A-Z): ").strip()
        if len(letter) != 1 or not letter.isalpha():
            print("❌ Please enter a single alphabet (a-z or A-Z)")
            sys.exit(1)
        show_homoglyphs(letter)

    elif choice == "b":
        word = input("Enter word/domain: ").strip()
        if not word:
            print("❌ Please enter a valid word/domain")
            sys.exit(1)
        generate_domain_variants(word)

    else:
        print("❌ Invalid option, choose [a] or [b]")


# ================================
# Run
# ================================
if __name__ == "__main__":
    main()
