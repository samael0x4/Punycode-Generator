## 🔗 PunyChain
Homoglyph Generator + DNS Resolver + Header Scanner + Weak CSP Detector + PoC Builder


### ⚡ About

PunyChain is a bug bounty & red team recon tool that helps you:

🔠 Generate homoglyph (punycode) variants for alphabets and domains

🌐 Detect possible punycode phishing vectors (IDN homograph attacks)

🕵️ Scan websites for missing/weak security headers

⚠️ Detect weak Content-Security-Policy (CSP) configurations

🔍 Check which homoglyph domains are Alive/Dead via DNS resolve

🚀 Build PoC HTML files to demonstrate homoglyph + CSP chaining


---
## 🔧 Installation
 🐧 Linux (Ubuntu/Debian/Kali)
 Install git if not installed
```bash
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
pip install -r requirements.txt
python3 punychain.py

```

 🍏 macOS
 Install Homebrew if missing
 ```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
git clone https://github.com/samael0x4/PunyChain.git
cd PunyChain
pip3 install -r requirements.txt
python3 punychain.py


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
python punychain.py


```


## 📋 Requirements
```bash
Python 3.8+
requests
beautifulsoup4
colorama
```

## 🧑‍💻 Usage Examples
Run the tool directly:
```bash
python3 punychain.py

```

## 💡 Tips for Bug Hunters

DNS resolver helps you spot which homoglyph domains are active.

If CSP is weak (*, http:, unsafe-inline) → use PoC builder for quick exploitation demo.

PoC HTML can be attached to bug bounty reports for better impact.

Try homoglyphs in subdomains, login forms, and email spoofing tests.

### 📜 License

MIT License © 2025 samael_0x4

### ⚖️ Disclaimer

This tool is for educational and security research purposes only.
Do not use against systems you don’t have permission to test.
The author takes no responsibility for misuse.

### 💬 Support

GitHub: samael0x4 
Issues: Open an issue on this repo
