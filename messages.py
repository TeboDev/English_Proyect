"""
messages.py — All ZenEnglish bot messages in English.
Centralizing strings here makes translation and tone adjustments trivial.
"""

import random

# ─────────────────────────────────────────────
#  GENERAL / WELCOME
# ─────────────────────────────────────────────
WELCOME = (
    "🌿 *Welcome to ZenEnglish Bot!*\n\n"
    "I'm your personal wellness & study companion. Here's what I can do:\n\n"
    "• /setup — Set your bedtime & morning alarm\n"
    "• /pomodoro — Start a focused study session\n"
    "• /report — View your weekly sleep history\n"
    "• /help — Show this message again\n\n"
    "_Let's build healthy habits together!_ 🌙"
)

HELP = WELCOME

UNKNOWN_COMMAND = (
    "🤔 I didn't recognise that command.\n"
    "Type /help to see everything I can do for you."
)

# ─────────────────────────────────────────────
#  /setup
# ─────────────────────────────────────────────
SETUP_ASK_BEDTIME = (
    "🛏️ *Sleep Setup*\n\n"
    "What time do you usually go to bed?\n"
    "Please reply with a time in *HH:MM* format (24-hour), e.g. `22:30`."
)

SETUP_ASK_WAKETIME = (
    "🌅 Great! Now, what time do you want your morning check-in?\n"
    "Reply with a time in *HH:MM* format (24-hour), e.g. `07:00`."
)

SETUP_COMPLETE = (
    "✅ *Setup complete!*\n\n"
    "🛏️ Bedtime: *{bedtime}*\n"
    "⏰ Morning check-in: *{waketime}*\n\n"
    "I'll send you a *Digital Blackout* reminder 1 hour before bedtime "
    "and a *morning check-in* at your wake-up time. Sweet dreams! 🌙"
)

SETUP_INVALID_TIME = (
    "⚠️ That doesn't look like a valid time.\n"
    "Please use *HH:MM* format (24-hour), e.g. `22:30` or `07:00`."
)

SETUP_ALREADY_DONE = (
    "⚙️ You already have a schedule set up.\n"
    "Send /setup again to *update* your bedtime and wake-up time."
)

# ─────────────────────────────────────────────
#  DIGITAL BLACKOUT
# ─────────────────────────────────────────────
DIGITAL_BLACKOUT = (
    "📵 *Digital Blackout — 1 Hour to Bedtime!*\n\n"
    "It's time to start winding down. Here's your pre-sleep ritual:\n\n"
    "1️⃣ Put your phone face-down (or use grayscale mode)\n"
    "2️⃣ Dim your lights\n"
    "3️⃣ Avoid screens for the next hour\n"
    "4️⃣ Try reading, journaling, or light stretching\n\n"
    "_I'll go quiet now. Goodnight!_ 🌙✨\n\n"
    "I'll check in with you tomorrow morning. Rest well! 😴"
)

# ─────────────────────────────────────────────
#  MORNING CHECK-IN
# ─────────────────────────────────────────────
MORNING_CHECKIN_INTRO = (
    "☀️ *Good morning!* Rise and shine!\n\n"
    "How are you feeling today? Let's do a quick check-in. 👇"
)

MORNING_MOOD_QUESTION = "How would you rate your mood right now?"

MORNING_SLEEP_QUESTION = "How many hours did you sleep last night? (e.g. `7.5`)"

MORNING_SLEEP_INVALID = (
    "⚠️ Please enter a number between *1* and *24*, e.g. `6.5` or `8`."
)

MORNING_CHECKIN_DONE = (
    "✅ *Check-in recorded!*\n\n"
    "Mood: {mood_emoji} {mood_label}\n"
    "Sleep: 💤 {hours} hours\n\n"
    "{motivational_message}\n\n"
    "_Have a wonderful day!_ 🌟"
)

# ─────────────────────────────────────────────
#  MOOD LABELS & EMOJIS
# ─────────────────────────────────────────────
MOOD_MAP = {
    "great": ("😄", "Great"),
    "good": ("🙂", "Good"),
    "okay": ("😐", "Okay"),
    "tired": ("😴", "Tired"),
    "stressed": ("😰", "Stressed"),
}

# ─────────────────────────────────────────────
#  MOTIVATIONAL MESSAGES
# ─────────────────────────────────────────────
_MOTIVATIONAL_GREAT = [
    "🔥 You're on fire! Keep that energy all day long.",
    "⭐ Feeling great is your superpower — use it wisely!",
    "🚀 Amazing! Today has big things written all over it.",
]

_MOTIVATIONAL_GOOD = [
    "💪 Good vibes only! You've got this.",
    "🌈 A good mood is the best foundation for a great day.",
    "✨ Keep it up — steady and strong wins the race.",
]

_MOTIVATIONAL_OKAY = [
    "🌤️ 'Okay' is a great starting point. Take it one step at a time.",
    "🧘 Be gentle with yourself today — small wins matter.",
    "💡 Even on average days, you can do extraordinary things.",
]

_MOTIVATIONAL_TIRED = [
    "☕ A little tired? Take breaks, hydrate, and be kind to yourself.",
    "🌙 Rest is productive. Pace yourself today.",
    "💤 Remember: even a 10-minute nap can recharge your mind.",
]

_MOTIVATIONAL_STRESSED = [
    "🫂 Take a deep breath. You've handled hard days before — you've got this.",
    "🧘 Stress is temporary. Focus on one task at a time.",
    "🌊 When the waves feel big, remember you know how to swim.",
]

_MOTIVATIONAL_DEFAULT = [
    "🌿 Every day is a fresh start. Make the most of it!",
    "💫 You showed up today — that already counts for a lot.",
    "🎯 Set one intention for today and watch what happens.",
]

MOTIVATIONAL_POOL = {
    "great": _MOTIVATIONAL_GREAT,
    "good": _MOTIVATIONAL_GOOD,
    "okay": _MOTIVATIONAL_OKAY,
    "tired": _MOTIVATIONAL_TIRED,
    "stressed": _MOTIVATIONAL_STRESSED,
    "default": _MOTIVATIONAL_DEFAULT,
}


def get_motivational(mood_key: str) -> str:
    pool = MOTIVATIONAL_POOL.get(mood_key, MOTIVATIONAL_POOL["default"])
    return random.choice(pool)


# ─────────────────────────────────────────────
#  POMODORO
# ─────────────────────────────────────────────
POMODORO_START = (
    "🍅 *Pomodoro Session Started!*\n\n"
    "Focus mode ON — *25 minutes* of deep work ahead.\n"
    "Put distractions aside and give it your best shot!\n\n"
    "_I'll ping you when it's time to take a break._ ⏱️"
)

POMODORO_BREAK = (
    "⏸️ *Break Time!*\n\n"
    "Great work! Take a *5-minute* break:\n"
    "• Stand up and stretch 🧘\n"
    "• Drink some water 💧\n"
    "• Rest your eyes (look 20 ft away for 20 seconds) 👀\n\n"
    "Send /pomodoro to start your next session when ready!"
)

POMODORO_ALREADY_RUNNING = (
    "⏱️ A Pomodoro session is *already running*.\n"
    "I'll remind you when it's time to break. Stay focused! 💪"
)

POMODORO_NO_SETUP = (
    "⚠️ Please run /setup first so I know your timezone context."
)

# ─────────────────────────────────────────────
#  /report
# ─────────────────────────────────────────────
REPORT_HEADER = "📊 *Weekly Sleep Report*\n\n"

REPORT_ROW = "• {date} — 💤 {hours}h  {mood_emoji} {mood_label}\n"

REPORT_AVERAGE = "\n📈 *7-day average sleep:* {avg:.1f} hours"

REPORT_EMPTY = (
    "📭 No sleep records found yet.\n"
    "Complete your morning check-in each day and your history will appear here!"
)

REPORT_FOOTER = (
    "\n\n_Use /setup to update your schedule or /pomodoro to study!_"
)

# ─────────────────────────────────────────────
#  NIGHT SILENCE
# ─────────────────────────────────────────────
NIGHT_SILENCE_ACTIVE = (
    "🌙 *Night Silence is active.*\n"
    "I'm resting too! I'll be back with your morning check-in. Goodnight! 😴"
)
