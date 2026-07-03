import streamlit as st
from datetime import datetime
import pytz
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Indian Profitable Stocks", page_icon="🇮🇳", layout="centered")

st.markdown("""
<style>
    h1, h2 { text-align: center; }
    .metric { background: #f0f2f6; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #FF9933; }
    .success { border-left-color: #2ecc71; }
    .stButton > button { width: 100%; padding: 12px; font-weight: bold; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Indian Profitable Stocks")
IST = pytz.timezone('Asia/Kolkata')
now = datetime.now(IST)

# Market hours: 9:15 AM - 3:30 PM IST, Mon-Fri
market_open = now.weekday() < 5 and (9, 15) <= (now.hour, now.minute) <= (15, 30)
status = "🟢 MARKET OPEN" if market_open else "🔴 MARKET CLOSED (9:15 AM - 3:30 PM IST, Mon-Fri)"
st.markdown(f"<div style='text-align:center'>🕐 {now.strftime('%I:%M %p IST')} | 📅 {now.strftime('%a, %d %b %Y')}<br><strong>{status}</strong></div>", unsafe_allow_html=True)

with st.expander("⚠️ DISCLAIMER - READ FIRST"):
    st.error("""**NOT FINANCIAL ADVICE / SEBI-அங்கீகரிக்கப்படாதது.** These are heuristic screens on delayed data.
    No scanner guarantees profit. Intraday trading loses money for most retail traders (SEBI's own study: ~70% of
    intraday traders lose money). You are solely responsible for all trades. Consult a SEBI-registered advisor.""")

st.divider()

# ============================================================================
# 💰 BUDGET & TARGET
# ============================================================================

BUDGET = st.slider("💰 Trading Budget (₹)", min_value=1000, max_value=100000, value=10000, step=500)
NET_TARGET = st.slider("🎯 Net Profit Target per Trade (₹, after all charges)", min_value=50, max_value=1000, value=100, step=25)

# Clear stale results if inputs changed
sig = f"{BUDGET}-{NET_TARGET}"
if st.session_state.get('last_sig') != sig:
    for key in ['res_intraday', 'res_btst']:
        st.session_state[key] = None
    st.session_state['last_sig'] = sig

for key in ['res_intraday', 'res_btst']:
    if key not in st.session_state:
        st.session_state[key] = None

# ============================================================================
# 🧾 INDIAN CHARGES CALCULATOR (discount broker, e.g., Zerodha-style)
# ============================================================================

def charges_intraday(buy_val, sell_val):
    """Equity intraday: brokerage min(₹20, 0.03%) per leg + STT + txn + GST + SEBI + stamp"""
    brokerage = min(20, 0.0003 * buy_val) + min(20, 0.0003 * sell_val)
    stt = 0.00025 * sell_val                      # 0.025% sell side only
    txn = 0.0000297 * (buy_val + sell_val)        # NSE ~0.00297%
    gst = 0.18 * (brokerage + txn)
    sebi = 0.000001 * (buy_val + sell_val)
    stamp = 0.00003 * buy_val                     # 0.003% buy side
    return brokerage + stt + txn + gst + sebi + stamp


def charges_delivery(buy_val, sell_val):
    """Equity delivery / BTST: ₹0 brokerage + STT 0.1% both sides + txn + GST + SEBI + stamp"""
    brokerage = 0
    stt = 0.001 * (buy_val + sell_val)            # 0.1% both sides
    txn = 0.0000297 * (buy_val + sell_val)
    gst = 0.18 * (brokerage + txn)
    sebi = 0.000001 * (buy_val + sell_val)
    stamp = 0.00015 * buy_val                     # 0.015% buy side
    return brokerage + stt + txn + gst + sebi + stamp


# ============================================================================
# 📋 NSE WATCHLIST (liquid stocks across price ranges)
# ============================================================================

WATCHLIST = [
    # Cheap & volatile (good for small budgets)
    'SUZLON.NS', 'IDEA.NS', 'YESBANK.NS', 'IRFC.NS', 'NHPC.NS', 'IOC.NS',
    'BHEL.NS', 'SAIL.NS', 'GAIL.NS', 'PNB.NS', 'ZOMATO.NS', 'BEL.NS',
    'ONGC.NS', 'NTPC.NS', 'TATASTEEL.NS', 'COALINDIA.NS', 'ITC.NS',
    # Mid-priced liquid
    'TATAMOTORS.NS', 'SBIN.NS', 'WIPRO.NS', 'TATAPOWER.NS', 'INFY.NS',
    'HINDALCO.NS', 'VEDL.NS', 'JSWSTEEL.NS', 'ADANIPOWER.NS', 'DLF.NS',
    # Higher-priced (used when budget allows)
    'HDFCBANK.NS', 'ICICIBANK.NS', 'RELIANCE.NS', 'AXISBANK.NS', 'LT.NS',
]


def load_yf():
    try:
        import yfinance as yf
        import pandas as pd
        return yf, pd
    except Exception:
        return None, None


def rsi(series, period=14):
    try:
        delta = series.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = -delta.where(delta < 0, 0).rolling(period).mean()
        val = 100 - (100 / (1 + gain / loss))
        v = float(val.iloc[-1])
        return None if v != v else v
    except Exception:
        return None


def fetch_hist(yf, ticker, period='30d', interval='1d'):
    try:
        h = yf.Ticker(ticker).history(period=period, interval=interval)
        return h if h is not None and len(h) >= 10 else None
    except Exception:
        return None


def build_pick(t, price, shares, gross_target, charges_fn, r, extra):
    buy_val = price * shares
    # Iterate: needed sell price such that (sell_val - buy_val - charges) >= NET_TARGET
    move = gross_target / shares
    for _ in range(5):  # few iterations converge fast
        sell_price = price + move
        sell_val = sell_price * shares
        ch = charges_fn(buy_val, sell_val)
        move = (NET_TARGET + ch) / shares
    sell_price = round(price + move, 2)
    ch = charges_fn(buy_val, sell_price * shares)
    return {
        'ticker': t.replace('.NS', ''), 'price': round(price, 2), 'shares': shares,
        'buy_val': round(buy_val, 2), 'sell_target': sell_price,
        'move_needed': round(move, 2), 'move_pct': round(move / price * 100, 2),
        'charges': round(ch, 2), 'gross_profit': round(NET_TARGET + ch, 2),
        'stop': round(price - move / 2, 2), 'rsi': round(r, 1), **extra
    }


def scan_india(yf, pd, progress, mode='intraday'):
    """mode: 'intraday' (buy & sell today) or 'btst' (buy today, sell tomorrow)"""
    charges_fn = charges_intraday if mode == 'intraday' else charges_delivery
    results = []
    for i, t in enumerate(WATCHLIST):
        progress.progress((i + 1) / len(WATCHLIST))
        h = fetch_hist(yf, t)
        if h is None:
            continue
        price = float(h['Close'].iloc[-1])
        if price > BUDGET or price < 1:
            continue
        shares = int(BUDGET / price)
        if shares < 1:
            continue
        r = rsi(h['Close'])
        if r is None:
            continue
        avg_vol = float(h['Volume'].iloc[-11:-1].mean())
        vol_ratio = float(h['Volume'].iloc[-1]) / avg_vol if avg_vol > 0 else 0
        avg_range = float((h['High'] - h['Low']).tail(10).mean())
        avg_range_pct = avg_range / price * 100

        pick = build_pick(t, price, shares, NET_TARGET, charges_fn, r,
                          {'vol': round(vol_ratio, 2), 'avg_range_pct': round(avg_range_pct, 2)})

        # Filters: momentum zone + the needed move must fit inside typical daily range
        if mode == 'intraday':
            if r < 40 or r > 70:
                continue
            if avg_range < pick['move_needed'] * 1.3:
                continue
        else:  # BTST — lean on momentum + gap tendency
            if r < 45 or r > 68:
                continue
            if avg_range < pick['move_needed']:
                continue
        pick['score'] = vol_ratio + (avg_range_pct / 2) + (r - 40) / 30
        results.append(pick)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def show_pick(best, hold_text, mode_label):
    st.success(f"✅ **{best['ticker']}** (NSE) — TOP PICK")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Buy At (approx)", f"₹{best['price']}")
        st.metric("Stop Loss", f"₹{best['stop']}")
    with c2:
        st.metric(f"Sell Target", f"₹{best['sell_target']}")
        st.metric("Quantity", f"{best['shares']} shares")
    st.markdown(f"""
    <div class='metric success'>
    <strong>📊 Setup ({mode_label})</strong><br>
    Capital used: ₹{best['buy_val']:,.0f} of ₹{BUDGET:,}<br>
    Move needed: ₹{best['move_needed']}/share ({best['move_pct']}%) — avg daily range is {best['avg_range_pct']}%<br>
    Gross profit at target: ₹{best['gross_profit']} → charges ₹{best['charges']} → <strong>Net ₹{NET_TARGET}</strong><br>
    RSI: {best['rsi']} | Volume: {best['vol']}x | {hold_text}
    </div>
    """, unsafe_allow_html=True)


def run_scan(mode):
    yf, pd = load_yf()
    if yf is None:
        st.error("Data library failed to load. Refresh and try again.")
        return None
    progress = st.progress(0)
    with st.spinner("Scanning NSE stocks (20-60 sec)..."):
        results = scan_india(yf, pd, progress, mode=mode)
    progress.empty()
    return results if results else []


# ============================================================================
# UI
# ============================================================================

st.subheader(f"NSE Scanners — Net ₹{NET_TARGET} after charges")

with st.expander(f"1️⃣ ☀️ Intraday (MIS) — buy now, sell before 3:20 PM today", expanded=False):
    st.caption("Charges model: intraday — brokerage ≤₹20/leg, STT 0.025% sell-side, GST, stamp")
    if st.button("🔍 SCAN NOW", key="b1"):
        st.session_state.res_intraday = run_scan('intraday')
    res = st.session_state.res_intraday
    if res == []:
        st.warning("❌ No setups pass filters right now. Best window: 9:30 AM - 2:30 PM IST on trading days.")
    elif res:
        show_pick(res[0], "Sell: at target or before 3:20 PM (MIS auto-squareoff)", "Intraday MIS")
        if len(res) > 1:
            st.caption("Runner-ups:")
            for r in res[1:4]:
                st.write(f"**{r['ticker']}** ₹{r['price']} → ₹{r['sell_target']} ({r['move_pct']}%) | RSI {r['rsi']} | Vol {r['vol']}x")

with st.expander(f"2️⃣ 🌙 BTST — buy today, sell tomorrow morning", expanded=False):
    st.caption("Charges model: delivery — ₹0 brokerage, STT 0.1% both sides, stamp 0.015%")
    if st.button("🔍 SCAN NOW", key="b2"):
        st.session_state.res_btst = run_scan('btst')
    res = st.session_state.res_btst
    if res == []:
        st.warning("❌ No BTST setups pass filters. Try scanning after 2:30 PM IST for better signals.")
    elif res:
        show_pick(res[0], "Buy: 3:00-3:25 PM today | Sell: tomorrow 9:15-10:00 AM", "BTST Delivery")
        if len(res) > 1:
            st.caption("Runner-ups:")
            for r in res[1:4]:
                st.write(f"**{r['ticker']}** ₹{r['price']} → ₹{r['sell_target']} ({r['move_pct']}%) | RSI {r['rsi']} | Vol {r['vol']}x")

st.divider()
st.markdown(f"""
<div style='font-size:12px;color:#999;text-align:center'>
⚠️ Heuristic screens, not guarantees. Data delayed ~15 min. Charge estimates assume discount-broker rates —
verify with your broker's calculator. Intraday profits are taxed as speculative business income (slab rate);
BTST as STCG. Trade responsibly. 🇮🇳📈
</div>
""", unsafe_allow_html=True)
