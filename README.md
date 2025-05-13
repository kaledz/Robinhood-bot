# 🤖 Robinhood Trading Bot

An automated trading bot for Robinhood built with Python.  
This script executes buy and sell decisions using configurable logic and is designed for educational or testing purposes.

> ⚠️ Disclaimer: This is for **educational use only**. Automated trading can carry significant financial risk. Use responsibly and at your own risk.

---

## 📦 Project Files

| File                        | Description |
|-----------------------------|-------------|
| `sell&buy.py`              | Main logic for executing buy/sell orders |
| `smartrader.py`            | Strategy logic and trading signals |
| `Jupyterlablinuxauth.ipynb`| Setup or authentication steps in notebook form |
| `.devcontainer/`           | (Optional) Dev container settings for VSCode |

---

## 🚀 Features

- 🧠 Custom trading logic and rules
- ✅ Authenticates with Robinhood (credentials setup required)
- 📈 Execute simulated or real orders
- 💼 Can be extended with technical indicators (RSI, MACD, etc.)

---

## 🛠 Requirements

To run the bot locally:

```bash
pip install robin_stocks
You may also need:

bash
Copy
Edit
pip install pandas requests
▶️ Usage
Clone the repo:

bash
Copy
Edit
git clone https://github.com/kaledz/Robinhood-bot.git
cd Robinhood-bot
Set up authentication:

Use robin_stocks to log in via email/password or MFA

Store your credentials securely (e.g., .env, vault, or keyring)

Run the bot:

bash
Copy
Edit
python sell&buy.py
📌 Notes
This bot uses the robin_stocks package (unofficial Robinhood API)

Robinhood's API is unofficial and subject to change

Avoid high-frequency execution—Robinhood may detect and block accounts

🔒 Security Advice
Never hardcode credentials.

Use .env files and python-dotenv or a keyring

Avoid pushing secrets to GitHub

🧑‍💻 Author
Built by Kris Lederer

📜 License
MIT License – Free to use and modify.

