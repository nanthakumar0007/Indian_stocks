# 📋 TRADING RULES — DayTrade Pro (US 🇺🇸 + India 🇮🇳)

> **PRINT THIS. READ IT BEFORE EVERY SESSION.**
> The difference between a growing account and a blown account is discipline, not luck.

---

## ⚠️ GOLDEN RULES (Both Markets)

1. **ONE trade per day maximum** — the scanner gives one pick; take it or skip it
2. **Never risk more than half your profit target** — 2:1 reward:risk minimum
3. **Hard stop losses, no exceptions** — enter the stop order immediately after buying
4. **Close at target — don't get greedy** — a hit target is a WIN, log it and stop
5. **Never revenge trade** — lost today? Done for today. Scanner runs again tomorrow
6. **Never trade with borrowed money / margin beyond your set budget**
7. **Empty scan result = no trade day** — the filters rejecting everything IS the system working
8. **Paper trade any new strategy for 2-3 weeks first** — track win rate before real money

---

## 🇺🇸 US MARKET APP (trading_assistant.py)

### Budget & Targets
| Setting | Rule |
|---------|------|
| Budget | Slider $1 - $1000 (you choose) |
| Profit target | 2% of budget (auto-calculated) |
| Stop loss | Half the target move (2:1 ratio) |
| Example | $35 budget → +$0.70 target / -$0.35 stop |
| Example | $500 budget → +$10 target / -$5 stop |

### The 4 Scanners
| # | Scanner | Buy | Sell | Notes |
|---|---------|-----|------|-------|
| 1️⃣ | Overnight Swing | Near close today | Tomorrow 9:30-10:30 AM ET | Overnight gap risk |
| 2️⃣ | Same-Day | Now | Before 3:55 PM ET | Best 9:30 AM - 2 PM ET |
| 3️⃣ | Any-Day Option | Now | TODAY at any profit | Premium ≤ budget/100 |
| 4️⃣ | Friday 0DTE | 9:30-10 AM ET | When green, NEVER past 3 PM | Expires worthless at close |

### US Market Hours (from India)
- 9:30 AM - 4:00 PM ET = **8:00 PM - 2:30 AM IST** (winter) / 7:00 PM - 1:30 AM IST (summer DST)

### Options-Specific Rules
- Cheap options (premium < $0.50) are LOTTERY TICKETS — most expire worthless
- Sell the moment you're happy — theta decay eats value every minute
- 0DTE: never hold past 3 PM ET; the contract goes to $0 at close
- Assume 100% loss when you buy — only use money you can burn

---

## 🇮🇳 INDIA MARKET APP (india_trading.py)

### Budget & Targets
| Setting | Rule |
|---------|------|
| Budget | Slider ₹1,000 - ₹100,000 |
| Net target | Slider ₹50 - ₹1,000 (AFTER charges) |
| Default | ₹10,000 budget → ₹100 net = ~1.1-1.2% stock move |
| Stop loss | Half the target move |

### The 2 Scanners
| # | Scanner | Buy | Sell | Charge Model |
|---|---------|-----|------|--------------|
| 1️⃣ | Intraday (MIS) | Anytime | Before 3:20 PM (auto square-off) | Brokerage ≤₹20/leg, STT 0.025% sell |
| 2️⃣ | BTST | 3:00-3:25 PM | Tomorrow 9:15-10 AM | ₹0 brokerage, STT 0.1% BOTH sides |

### India Market Hours
- **9:15 AM - 3:30 PM IST**, Monday-Friday (closed on exchange holidays)
- Best intraday scan window: 9:30 AM - 2:30 PM
- Best BTST scan window: after 2:30 PM

### Charges the App Already Accounts For ✅
- Brokerage (discount-broker rates), STT, exchange transaction charges, GST 18%, SEBI fees, stamp duty
- The sell target is solved so profit AFTER these = your net target exactly

### Taxes the App Does NOT Include ⚠️
- **Intraday profits** = speculative business income → taxed at YOUR SLAB RATE
- **BTST profits** = short-term capital gains (STCG)
- Keep records; consult a CA at year-end
- Verify charge estimates against your own broker's brokerage calculator

---

## 🛑 STOP LOSS DISCIPLINE (Non-Negotiable)

- [ ] Place the stop order IMMEDIATELY after your buy fills
- [ ] NEVER move a stop further away ("it'll bounce back" = famous last words)
- [ ] Stop hit = trade over = close the app for the day
- [ ] If stopped out, DO NOT re-enter the same stock that day

## 🎯 TAKE-PROFIT DISCIPLINE

- [ ] Target hit = SELL. Immediately. Fully.
- [ ] Do not "let it run" — the math of this system depends on consistent small wins
- [ ] Hit 70% of target and momentum dying? Taking it early is fine. Holding past target is not.

---

## 🚨 SKIP THE TRADE IF ANY OF THESE APPLY

- [ ] Major news day (Fed/RBI policy, budget day, election results, big earnings)
- [ ] Market gapped >1.5% at open (chaos days break the pattern filters)
- [ ] The scanner pick's RSI/volume numbers look stale (data delay ~15 min — sanity-check price at your broker first)
- [ ] You already traded today
- [ ] You're angry, tired, or "need to make back" a loss
- [ ] The price at your broker is already PAST the sell target (you missed it — skip)

---

## 📊 WEEKLY REVIEW (Every Friday / Saturday)

| Metric | This Week | Target |
|--------|-----------|--------|
| Trades taken | ___ | ≤ 5 |
| Wins | ___ | — |
| Losses | ___ | — |
| Win rate | ___% | > 55% |
| Net P&L | ___ | Positive |
| Rules broken | ___ | **0** |

**After 20 trades:** if win rate < 50%, STOP and reassess. Do not scale up a losing system.

---

## 💬 SAY THIS BEFORE EVERY TRADE

> "I am buying ___ shares of ___ at ___ with a stop at ___ and target at ___.
> If wrong, I lose ___. If right, I make ___. I exit at my levels, not my emotions."

Takes 10 seconds. Saves accounts.

---

## ⚠️ FINAL DISCLAIMER

This app produces **heuristic screens**, not predictions. No scanner can guarantee profit — markets
move against good setups regularly. SEBI's own research found ~70% of Indian retail intraday traders
lose money; US statistics are similar. Data is delayed 15-20 minutes. Trade only money you can afford
to lose completely. This is not financial advice — consult a licensed / SEBI-registered advisor.

**Trade mechanical. Trade small. Live to trade tomorrow.** 📈
