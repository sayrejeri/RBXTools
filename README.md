# RBXTools

A collection of **local, open-source Roblox utility tools** designed to help users manage their accounts safely and transparently.

> ⚠️ **This project runs locally on your machine.  
> Your account data is never collected, logged, or transmitted to us.**

---

## ✨ Features

### Roblox Unfollow Tool
- Unfollow users you are following
- Optional filters: 
  - Unfollow **non-friends only** (NOT YET ADDED)
  - Unfollow **offline users only** (NOT YET ADDED)
- Automatic rate-limit handling
- Generates a **log file** of all unfollowed users
- Can be stopped and resumed safely

---

## 🔒 Security & Privacy (Important)

- This tool **runs locally on your computer**
- Your `.ROBLOSECURITY` cookie is:
  - ❌ NOT uploaded
  - ❌ NOT stored remotely
  - ❌ NOT logged or saved automatically
- The source code is fully open-source — you can review everything it does

⚠️ **Never share your `.ROBLOSECURITY` cookie with anyone.**  
Anyone with it can fully access your Roblox account.

After using the tool, it is recommended that you **log out of Roblox** in your browser to invalidate the cookie.

---

## 🖥️ How It Works

1. The script uses Roblox’s public APIs
2. Authentication is done using your existing browser session
3. Requests are sent at a safe rate to avoid spam or abuse detection
4. Every unfollow is logged locally to a text file

---

## 📦 Installation Options

### Option A: Windows EXE (Recommended)
- Download the latest `.exe` from the **Releases** page
- No Python installation required
- Runs entirely on your PC

### Option B: Run from Source (Advanced)
1. Install **Python 3.10+**
2. Install dependencies:
   ```bash
   pip install requests
3. Run:

   ```bash
   python unfollow.py
   ```

---

## 📄 Output Files

Each run creates a log file in the same folder:

```
unfollowed_<robloxId>_YYYYMMDD_HHMMSS.txt
```

Format:

```
USER_ID    USERNAME
```

---

## ❗ Disclaimer

This project is **not affiliated with Roblox Corporation**.

Use of this tool is at your own risk.
You are responsible for complying with Roblox’s Terms of Service.

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it, but **without warranty**.

---

## 🤝 Contributing

Pull requests and improvements are welcome.

If you have ideas for:

* additional filters
* better UI
* performance improvements
* new Roblox tools

Feel free to open an issue or PR.

---

## ⭐ Acknowledgments

Built for educational and personal account-management purposes.

If you find this useful, consider starring the repo ⭐

```

---
