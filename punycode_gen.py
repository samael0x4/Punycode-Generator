#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Punycode Generator Tool
 Author : samael_0x4
 GitHub : https://github.com/samael0x4
 Description : Generate homoglyphs/punycode variants for English alphabets (a-z, A-Z).
"""

import sys

# Dictionary of homoglyph variants
homoglyphs = {
    "a": ["à", "á", "â", "ã", "ä", "å", "ɑ", "а", "ạ", "ą", "ǎ", "ª"],
    "b": ["ƀ", "ƃ", "ƅ", "ь", "ҍ", "ъ", "Ь", "ß"],
    "c": ["ç", "ć", "č", "ċ", "ĉ", "ƈ", "ς"],
    "d": ["ď", "đ", "ԁ", "ժ", "ḍ", "ɗ", "ð"],
    "e": ["è", "é", "ê", "ë", "ē", "ė", "ę", "е", "ҽ", "ε", "ɘ"],
    "f": ["ƒ", "ғ", "ғ", "ʃ", "ғ"],
    "g": ["ğ", "ģ", "ǵ", "ĝ", "ɡ", "ɢ", "ġ"],
    "h": ["ĥ", "ħ", "н", "ђ", "ћ", "һ"],
    "i": ["ì", "í", "î", "ï", "ī", "į", "ι", "ӏ", "¡"],
    "j": ["ĵ", "ј", "ʝ", "ɉ"],
    "k": ["ķ", "ĸ", "κ", "к", "қ"],
    "l": ["ĺ", "ļ", "ľ", "ŀ", "ł", "ι", "ӏ", "ɫ"],
    "m": ["м", "ṃ", "ɱ", "ʍ"],
    "n": ["ñ", "ń", "ņ", "ň", "ŉ", "η", "п"],
    "o": ["ò", "ó", "ô", "õ", "ö", "ō", "ø", "ο", "σ", "о", "ɵ", "ө"],
    "p": ["ρ", "р", "ƿ", "þ", "ҏ"],
    "q": ["զ", "ʠ"],
    "r": ["ŕ", "ŗ", "ř", "г", "ѓ"],
    "s": ["ś", "š", "ş", "ș", "ѕ", "ʂ", "ṡ"],
    "t": ["ţ", "ť", "ŧ", "τ", "т", "ҭ"],
    "u": ["ù", "ú", "û", "ü", "ū", "ů", "ű", "ų", "µ"],
    "v": ["ν", "ѵ", "ṿ"],
    "w": ["ŵ", "ш", "ԝ", "ɯ"],
    "x": ["х", "ҳ", "ẋ", "×"],
    "y": ["ý", "ÿ", "ŷ", "у", "ү", "ў"],
    "z": ["ź", "ž", "ż", "ƶ", "ʐ", "ᴢ"],
}

# Add uppercase variants automatically
for k in list(homoglyphs.keys()):
    homoglyphs[k.upper()] = [glyph.upper() for glyph in homoglyphs[k] if glyph.isalpha()]

def banner():
    print(r"""
  ____                              _       ____                 
 |  _ \ _   _ _ __  _   _  ___ ___ | |__   / ___| ___ _ __  _   _ 
 | |_) | | | | '_ \| | | |/ __/ _ \| '_ \  \___ \/ __| '_ \| | | |
 |  __/| |_| | | | | |_| | (_| (_) | | | |  ___) \__ \ |_) | |_| |
 |_|    \__,_|_| |_|\__, |\___\___/|_| |_| |____/|___/ .__/ \__, |
                    |___/                            |_|    |___/ 

        🔥 Punycode Generator by samael_0x4 🔥
    """)

def main():
    banner()
    while True:
        print("\nOptions:")
        print("1) Enter Alphabet")
        print("2) Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            char = input("\nEnter an alphabet (a-z or A-Z): ").strip()
            if char in homoglyphs:
                print(f"\n[+] Punycode / homoglyph variants for '{char}':\n")
                for glyph in homoglyphs[char]:
                    print(glyph)
            else:
                print("\n[-] Invalid input! Please enter a single alphabet (a-z or A-Z).")
        elif choice == "2":
            print("\n[!] Exiting... Stay hacking 👾\n")
            sys.exit(0)
        else:
            print("\n[-] Invalid choice, try again.")

if __name__ == "__main__":
    main()
