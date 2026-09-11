import streamlit as st
import asyncio
import itertools
import re
import html
from agent.browser_agent import run_shopping_task, run_multi_item_task

st.set_page_config(page_title="Smart Shopping Agent", page_icon="🛍️", layout="centered")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700;900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root {
    --bg: #0B1A18;
    --surface: #12231E;
    --accent: #F2A93B;
    --accent-2: #D64550;
    --text: #F5EFE0;
    --text-muted: #93A69C;
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'IBM Plex Sans', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 900;
    font-size: 2.6rem;
    line-height: 1.15;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px dashed #2A403A;
    padding-bottom: 1.5rem;
}

div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
    background: var(--surface);
    border: 1px dashed #3A554D;
    border-radius: 4px;
    color: var(--text);
    font-family: 'IBM Plex Sans', sans-serif;
    padding: 0.7rem;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent);
    box-shadow: none;
}

.stButton > button {
    background: var(--accent);
    color: #0B1A18;
    font-weight: 600;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.5rem;
    font-family: 'IBM Plex Sans', sans-serif;
}
.stButton > button:hover {
    background: var(--accent-2);
    color: var(--text);
}

div[data-testid="column"] .stButton > button {
    background: var(--surface);
    color: var(--text);
    border: 1px dashed #3A554D;
    font-size: 0.85rem;
    padding: 0.4rem 0.6rem;
}
div[data-testid="column"] .stButton > button:hover {
    background: var(--accent);
    color: #0B1A18;
    border-color: var(--accent);
}

.tag-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--surface);
    border-left: 3px solid var(--accent);
    border-radius: 2px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.tag-badge {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: var(--accent);
    min-width: 2rem;
}
.tag-name {
    flex: 1;
    font-size: 0.92rem;
    color: var(--text);
    line-height: 1.4;
}
.tag-price {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--accent);
    white-space: nowrap;
    border-left: 1px dashed #3A554D;
    padding-left: 1rem;
}

.site-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 3px;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.site-badge.amazon {
    background: #2A403A;
    color: #F2A93B;
}
.site-badge.flipkart {
    background: #2A3A4A;
    color: #5DADE2;
}

.result-header {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text);
    margin: 1.5rem 0 1rem 0;
}

.section-divider {
    border-top: 1px dashed #2A403A;
    margin: 2.5rem 0;
}

div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid #22362F;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown('<div class="hero-title">Shop smarter,<br>hands-free.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Tell the agent what you need — it browses Amazon.in and Flipkart to find and compare the best matches.</div>', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; gap:1rem; margin-bottom:2rem;">
    <div style="flex:1; background:var(--surface); border-radius:4px; padding:1rem; text-align:center;">
        <div style="font-size:1.5rem;">1️⃣</div>
        <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.3rem;">Tell us what you need</div>
    </div>
    <div style="flex:1; background:var(--surface); border-radius:4px; padding:1rem; text-align:center;">
        <div style="font-size:1.5rem;">2️⃣</div>
        <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.3rem;">Agent browses & compares</div>
    </div>
    <div style="flex:1; background:var(--surface); border-radius:4px; padding:1rem; text-align:center;">
        <div style="font-size:1.5rem;">3️⃣</div>
        <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.3rem;">Get the best pick</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


def parse_results(text):
    items = []
    blocks = re.split(r'\n?\d+\.\s+', text)[1:]
    blocks = [b for b in blocks if b.strip()]
    for block in blocks:
        price_match = re.search(r'(₹\s?[\d,]+\.?\d*|\$\s?[\d,]+\.?\d*)', block)
        if not price_match:
            continue
        price = price_match.group(1).replace(" ", "")
        name_part = block.split(price_match.group(0))[0]
        name_part = re.split(r'(?i)price\s*:?\s*$', name_part)[0]
        name_part = name_part.replace('**', '')
        name_part = re.sub(r'\s*[-–—|:]\s*$', '', name_part)
        name_part = ' '.join(name_part.split())
        if name_part:
            items.append({"name": name_part.strip(" -–—|"), "price": price})
    return items[:3]

def add_site_badges(text):
    text = re.sub(
        r'\(?Amazon\.in\)?',
        '<span class="site-badge amazon">AMAZON.IN</span>',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'\(?Flipkart\.com\)?',
        '<span class="site-badge flipkart">FLIPKART</span>',
        text,
        flags=re.IGNORECASE
    )
    return text

def extract_chart_data(comparison_text):
    """Extracts lowest price per site per category for a bar chart."""
    import pandas as pd
    categories = re.split(r'\n(?=[A-Za-z ]+:\n)', comparison_text)
    data = []
    for block in categories:
        cat_match = re.match(r'([A-Za-z ]+):', block)
        if not cat_match:
            continue
        category = cat_match.group(1).strip()
        amazon_prices = re.findall(r'Amazon\.in.*?₹([\d,]+)', block)
        flipkart_prices = re.findall(r'Flipkart\.com.*?₹([\d,]+)', block)
        if amazon_prices:
            data.append({"Category": category, "Site": "Amazon.in", "Price": min(int(p.replace(",", "")) for p in amazon_prices)})
        if flipkart_prices:
            data.append({"Category": category, "Site": "Flipkart", "Price": min(int(p.replace(",", "")) for p in flipkart_prices)})
    return pd.DataFrame(data) if data else None

def run_with_progress(coro, messages, interval=4):
    """Runs an async agent task while cycling through status messages in the UI."""
    status_placeholder = st.empty()

    async def _runner():
        msg_cycle = itertools.cycle(messages)
        task = asyncio.ensure_future(coro)
        while not task.done():
            status_placeholder.info(next(msg_cycle))
            await asyncio.sleep(interval)
        return await task

    result = asyncio.run(_runner())
    status_placeholder.empty()
    return result


# ================= SECTION 1: Quick Search =================
st.markdown('<div class="result-header">Quick search</div>', unsafe_allow_html=True)

st.markdown("**Quick picks:**")
preset_cols = st.columns(4)
presets = {
    "🎧 Earbuds": "wireless earbuds",
    "🔌 Charger": "phone charger",
    "🔊 Speaker": "bluetooth speaker",
    "🎒 Bag": "laptop bag",
}
for col, (label, query) in zip(preset_cols, presets.items()):
    with col:
        if st.button(label, key=f"preset_{label}", use_container_width=True):
            st.session_state["query_input"] = query
            st.rerun()

user_query = st.text_input(
    "What are you looking for?",
    placeholder="e.g. wireless earbuds under ₹500",
    key="query_input"
)

search_clicked = st.button("🔍  Search", key="quick_search_btn")

if search_clicked:
    if not user_query.strip():
        st.warning("Please enter a search query first.")
    else:
        clean_query = user_query.strip()
        task = (
            f"Go to Amazon.in, search for '{clean_query}'. "
            f"List the names and prices (in INR) of the top 3 results. "
            f"Do not change delivery location or currency settings."
        )
        try:
            quick_messages = [
                "🔍 Searching Amazon.in...",
                "📄 Reading search results...",
                "🧮 Picking the top matches...",
            ]
            result = run_with_progress(run_shopping_task(task), quick_messages)
            final_answer = result.final_result()
            final_answer = final_answer.split("Attachments:")[0].strip()

            st.markdown(f'<div class="result-header">Top matches for "{html.escape(clean_query)}"</div>', unsafe_allow_html=True)
            items = parse_results(final_answer)
            if items:
                for i, item in enumerate(items, 1):
                    st.markdown(f"""
                    <div class="tag-card">
                        <div class="tag-badge">{i:02d}</div>
                        <div class="tag-name">{html.escape(item['name'])}</div>
                        <div class="tag-price">{html.escape(item['price'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(final_answer)

            st.session_state.history.insert(0, {"query": clean_query, "result": final_answer})
        except Exception as e:
            st.error(
                "⚠️ The agent hit an unexpected issue while browsing "
                "(this can happen if a site is slow or temporarily unavailable). "
                "Please try again — it usually works on a retry."
            )
            with st.expander("Technical details"):
                st.code(str(e))

# ================= SECTION 2: Multi-Item Budget Planner =================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="result-header">Smart shopping list</div>', unsafe_allow_html=True)
st.caption("Give the agent a list of items and a total budget — it compares Amazon.in and Flipkart and picks the best combination.")

st.markdown("**Quick bundles:**")
bundle_cols = st.columns(3)
bundles = {
    "🎧🔌 Audio + Charging": "bluetooth earbuds, phone charger",
    "🎒💻 Travel Kit": "laptop bag, phone charger, power bank",
    "🔊🎧 Sound Combo": "bluetooth speaker, wireless earbuds",
}
for col, (label, combo) in zip(bundle_cols, bundles.items()):
    with col:
        if st.button(label, key=f"bundle_{label}", use_container_width=True):
            st.session_state["items_input"] = combo
            st.rerun()

items_input = st.text_input(
    "What items do you need? (comma-separated)",
    placeholder="e.g. phone charger, bluetooth earbuds",
    key="items_input"
)

budget_input = st.number_input(
    "Total budget (₹)",
    min_value=100,
    max_value=100000,
    value=1000,
    step=100
)
plan_clicked = st.button("🛍️  Plan My Purchase", key="plan_btn")

if plan_clicked:
    if not items_input.strip():
        st.warning("Please enter at least one item.")
    else:
        items = [i.strip() for i in items_input.split(",") if i.strip()]
        try:
            plan_messages = [
                "🔍 Searching Amazon.in...",
                "🔍 Searching Flipkart.com...",
                "⚖️ Comparing prices and ratings...",
                "🧠 AI is selecting the best combination...",
            ]
            result = run_with_progress(run_multi_item_task(items, budget_input), plan_messages)
            final_answer = result.final_result()
            final_answer = final_answer.split("Attachments:")[0].strip()

                        # Split main recommendation from full comparison list
            if "FULL COMPARISON:" in final_answer:
                main_part, comparison_part = final_answer.split("FULL COMPARISON:", 1)
            else:
                main_part, comparison_part = final_answer, None

            st.markdown('<div class="result-header">Recommended combination</div>', unsafe_allow_html=True)
            st.markdown(add_site_badges(main_part.strip()), unsafe_allow_html=True)

            if comparison_part:
                with st.expander("📊 See full comparison (all options considered)"):
                    chart_df = extract_chart_data(comparison_part)
                    if chart_df is not None and not chart_df.empty:
                        st.markdown("**Lowest price per site:**")
                        pivot_df = chart_df.pivot(index="Category", columns="Site", values="Price")
                        st.bar_chart(pivot_df)
                        st.markdown("---")
                    st.markdown(add_site_badges(comparison_part.strip()), unsafe_allow_html=True)
            
            # Extract total combined price for the budget bar
            total_match = re.search(r'Total Combined Price\*{0,2}:?\*{0,2}\s*₹\s?([\d,]+\.?\d*)', final_answer, re.IGNORECASE)
            if total_match:
                spent = float(total_match.group(1).replace(",", ""))
                budget = float(budget_input)
                pct = min(spent / budget, 1.0)
                remaining = budget - spent

                st.markdown(f"""
                <div style="margin-top: 1.5rem;">
                    <div style="display:flex; justify-content:space-between; font-family:'IBM Plex Mono', monospace; font-size:0.9rem; color: var(--text-muted); margin-bottom:0.4rem;">
                        <span>₹{spent:,.0f} spent</span>
                        <span>₹{budget:,.0f} budget</span>
                    </div>
                    <div style="background:#1C332C; border-radius:4px; height:10px; overflow:hidden;">
                        <div style="background: var(--accent); width:{pct*100}%; height:100%;"></div>
                    </div>
                    <div style="font-size:0.85rem; color: var(--text-muted); margin-top:0.4rem;">
                        {pct*100:.0f}% of budget used — ₹{remaining:,.0f} remaining
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.session_state.history.insert(0, {
                "query": f"{', '.join(items)} (₹{budget_input})",
                "result": final_answer
            })
        except Exception as e:
            st.error(
                "⚠️ The agent hit an unexpected issue while browsing "
                "(this can happen if a site is slow or temporarily unavailable). "
                "Please try again — it usually works on a retry."
            )
            with st.expander("Technical details"):
                st.code(str(e))

# ================= SECTION 3: History =================
if st.session_state.history:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="result-header">Recent searches</div>', unsafe_allow_html=True)
    for i, entry in enumerate(st.session_state.history):
        with st.expander(f"🔁 {entry['query']}"):
            st.markdown(entry["result"])