# LocalShare
Share your files in localhost
# 📂 Local File Server

A lightweight Flask-based local file server — host **any folder or single file** on your machine and share/download over your local network. No cloud, no drama.

---

## ✨ Features

- 📁 Browse files from any directory
- ⬇️ Download individual files
- 📦 Download entire folders as **ZIP** — no manual zipping needed
- 📄 Share a **single file** directly by passing its path
- ⬆️ Upload files from the browser into the hosted folder
- 🔢 Human-readable file sizes (KB, MB, GB)
- 🌐 LAN access — open from any device on the same Wi-Fi

---

## 📁 Project Structure

```
local-file-server/
├── server.py
├── requirements.txt
└── templates/
    └── index.html
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/local-file-server.git
cd local-file-server
```

### 2. Install dependencies

```bash
pip install flask werkzeug
```

---

## ▶️ Usage

### Host a full directory

```bash
# Windows
python server.py --dir "C:\Users\YourName\Downloads"

# Linux / Mac
python server.py --dir /home/yourname/videos
```

### Host a single file

```bash
python server.py --dir "C:\wallpapers\spider-man.jpg"
```

> Works with any file type — images, ZIPs, videos, PDFs, etc.

### Using an environment variable

```bash
# Windows
set FILE_SERVER_DIR=C:\Users\YourName\Documents
python server.py

# Linux / Mac
export FILE_SERVER_DIR=/home/yourname/myfiles
python server.py
```

### Default (no args)

Creates and uses a `shared/` folder next to `server.py`.

---

## 🌐 Access

Open in browser on your machine:
```
http://localhost:5000
```

From another device on the same Wi-Fi:
```
http://192.168.x.x:5000
```

> Find your IP:  
> Windows → `ipconfig`  
> Linux/Mac → `ip a` or `ifconfig`

---

## 📦 requirements.txt

```
flask
werkzeug
```

---

## 🛡️ Note

Intended for **local/LAN use only**. Do not expose to the public internet.
