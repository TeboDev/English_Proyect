# ZenEnglish 🌿

> A Telegram bot that helps students build healthy sleep habits and focused study sessions — 100% in English.

---

## Features

| Feature | Command / Trigger |
|---|---|
| Initial setup | `/setup` |
| Pomodoro timer (25 min) | `/pomodoro` |
| Morning check-in & mood survey | `/checkin` (or auto at wake time) |
| Digital Blackout reminder | Automatic — 1 hr before bedtime |
| Weekly sleep report | `/report` |
| Help menu | `/start` or `/help` |

---

## Quick Start

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd zen-english-bot
```

### 2. Create your virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # Linux / macOS
# .venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your bot on Telegram
1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **API token** you receive

### 5. Set your token
```bash
cp .env.example .env
# Edit .env and paste your token:
# BOT_TOKEN=123456789:ABCdef...
```

### 6. Run the bot
```bash
python main.py
```

---

## Project Structure

```
zen-english-bot/
├── main.py              # Entry point — wires everything together
├── database.py          # SQLite helpers (users, sleep_logs)
├── scheduler.py         # APScheduler jobs (Digital Blackout, morning check-in)
├── messages.py          # All English messages & motivational quotes
├── handlers/
│   ├── general.py       # /start, /help, unknown command
│   ├── setup.py         # /setup conversation
│   ├── pomodoro.py      # /pomodoro command
│   ├── checkin.py       # /checkin conversation (mood + sleep hours)
│   └── report.py        # /report command
├── .env.example         # Template — copy to .env and fill in token
├── requirements.txt     # Python dependencies
└── zenbot.db            # SQLite database (auto-created at startup)
```

---

## Scheduled Notifications

All times are stored and compared in **UTC**. When you run `/setup`:
- Enter your **bedtime** in UTC (e.g. if your local time is UTC-5 and you sleep at 22:00 local, enter `03:00`)
- Enter your **wake-up time** in UTC similarly

> **Tip:** Use a timezone converter or just add/subtract your UTC offset.

---

## Deployment (Railway / Render)

1. Push the project to GitHub (**without `.env`!**)
2. Create a new service on [Railway](https://railway.app) or [Render](https://render.com)
3. Add `BOT_TOKEN` as an environment variable in the dashboard
4. Set the start command to `python main.py`
5. Deploy 🚀

---

## Team

| Member | Role |
|---|---|
| Tania Guerra | Project lead, code review & integration |
| Sebastián Fernández | Bot message design & user flow |
| Liquinchano Robinho | Documentation & README |
| Writer (TBD) | English messages & motivational content |
| Finder (TBD) | API research, libraries & hosting options |

---

## License

MIT — free to use and modify.
