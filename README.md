## 🔗 PunyChain
Homoglyph Generator + Header Scanner + Weak CSP Detector + PoC Builder


### ⚡About
--> PunyChain is a bug bounty & red team recon tool that helps you:

🔠 Generate homoglyph (punycode) variants for alphabets and domains

🌐 Detect possible punycode phishing vectors (IDN homograph attacks)

🕵️ Scan websites for missing/weak security headers

⚠️ Detect weak Content-Security-Policy (CSP) configurations

🚀 Suggest PoC payloads for chaining homoglyphs with CSP misconfigs → Account Takeover potential



---
## 🔧 Installation
 🐧 Linux (Ubuntu/Debian/Kali)
 Install git if not installed
```bash
sudo apt update && sudo apt install git -y
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
pip install -r requirements.txt
python3 punychain.py -h

```

 🍏 macOS
 Install Homebrew if missing
 ```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
pip3 install -r requirements.txt
python3 punychain.py -h

```
 🪟 Windows (PowerShell)

Install Git

Download from: https://git-scm.com/downloads/win  

During install, check “Add Git to PATH”.

Clone repo and install requirements
```bash
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
pip install -r requirements.txt
python punychain.py -h

```


## 📋 Requirements
```bash
Python 3.8+
requests
beautifulsoup4
colorama
```

## 🧑‍💻 Usage Examples
```bash
# Show help
punychain -h

# Generate homoglyphs for single alphabet
punychain -a a

# Generate homoglyph domain variants
punychain -d tesla.com

# Scan headers & weak CSP for a target
punychain -u https://target.com
```

## 🔥 Example
```bash
$ punychain -d google.com

gооgle.com  --> xn--ggle-0nda.com
gοogle.com  --> xn--ggle-v2a9629b.com
```
```bash
$ punychain -u https://target.com

[FOUND] Content-Security-Policy: script-src https://target.com
[MISSING] Strict-Transport-Security
[!] Weak CSP detected → Potential for homoglyph injection!
[POC] Try hosting a script on homoglyph domain and inject via CSP
```

### 📜 License

MIT License © 2025 samael_0x4

### ⚖️ Disclaimer

This tool is for educational and security research purposes only.
Do not use against systems you don’t have permission to test.
The author takes no responsibility for misuse.

### 💬 Support

GitHub: samael0x4 
Issues: Open an issue on this repo
