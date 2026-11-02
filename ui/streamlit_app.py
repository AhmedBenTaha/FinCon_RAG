import html
import sys
from pathlib import Path

import streamlit as st

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.generation.chain import FinConRAGPipeline
from src.ingestion.run_ingestion import run_ingestion_pipeline

st.set_page_config(
    page_title="FinCon & Regulatory RAG Assistant",
    page_icon="💼",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────
#  Theme & Animations (UI only)
# ──────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-0: #070b18;
    --bg-1: #0d1326;
    --card: rgba(255, 255, 255, 0.045);
    --card-border: rgba(255, 255, 255, 0.10);
    --violet: #8b5cf6;
    --indigo: #6366f1;
    --cyan: #22d3ee;
    --pink: #f472b6;
    --emerald: #34d399;
    --amber: #fbbf24;
    --text: #e8ecf8;
    --muted: #9aa4c4;
}

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    color: var(--text);
}

/* ── Animated background ─────────────────────────────── */
.stApp {
    background:
        radial-gradient(900px 500px at 8% -5%, rgba(139, 92, 246, 0.22), transparent 60%),
        radial-gradient(800px 500px at 100% 5%, rgba(34, 211, 238, 0.16), transparent 60%),
        radial-gradient(700px 500px at 50% 110%, rgba(244, 114, 182, 0.12), transparent 60%),
        linear-gradient(180deg, var(--bg-0), var(--bg-1));
    background-attachment: fixed;
}

header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1200px; }

/* ── Scrollbar ───────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: linear-gradient(var(--violet), var(--cyan)); border-radius: 10px; }
::-webkit-scrollbar-track { background: transparent; }

/* ── Keyframes ───────────────────────────────────────── */
@keyframes fadeUp   { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeIn   { from { opacity: 0; } to { opacity: 1; } }
@keyframes gradMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes floaty   { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes pulseGlow{ 0%,100% { box-shadow: 0 0 0 0 rgba(139,92,246,.45); } 50% { box-shadow: 0 0 0 12px rgba(139,92,246,0); } }
@keyframes shimmer  { 0% { transform: translateX(-120%); } 100% { transform: translateX(120%); } }
@keyframes blink    { 0%,100% { opacity: 1; } 50% { opacity: .35; } }
@keyframes barFill  { from { width: 0; } }

/* ── Hero ────────────────────────────────────────────── */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.4rem 2.2rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(139,92,246,.20), rgba(34,211,238,.10) 55%, rgba(244,114,182,.14));
    border: 1px solid var(--card-border);
    backdrop-filter: blur(14px);
    box-shadow: 0 25px 60px -25px rgba(99, 102, 241, .55);
    animation: fadeUp .8s ease both;
}
.hero::before {
    content: "";
    position: absolute; inset: -2px;
    background: conic-gradient(from 0deg, transparent, rgba(139,92,246,.35), transparent 30%);
    animation: spin 9s linear infinite;
    z-index: 0;
    opacity: .45;
}
.hero::after {
    content: "";
    position: absolute; inset: 1px;
    border-radius: 23px;
    background: linear-gradient(135deg, rgba(10,14,30,.92), rgba(13,19,38,.88));
    z-index: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
.hero > * { position: relative; z-index: 1; }

.hero-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    padding: .3rem .85rem; border-radius: 999px;
    font-size: .75rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
    color: var(--cyan);
    background: rgba(34,211,238,.10);
    border: 1px solid rgba(34,211,238,.35);
}
.hero-badge .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--emerald); animation: blink 1.6s infinite; }

.hero-title {
    margin: .9rem 0 .4rem 0;
    font-size: clamp(1.8rem, 3.6vw, 2.9rem);
    font-weight: 800; line-height: 1.15;
    background: linear-gradient(90deg, #fff, #c4b5fd, #67e8f9, #f9a8d4, #fff);
    background-size: 300% 100%;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradMove 8s ease infinite;
}
.hero-icon { display: inline-block; animation: floaty 3.2s ease-in-out infinite; -webkit-text-fill-color: initial; }
.hero-sub { color: var(--muted); font-size: 1.02rem; max-width: 760px; margin-bottom: 1.2rem; }

.chips { display: flex; flex-wrap: wrap; gap: .55rem; }
.chip {
    padding: .38rem .8rem; border-radius: 999px; font-size: .78rem; font-weight: 500;
    color: var(--text);
    background: rgba(255,255,255,.06);
    border: 1px solid var(--card-border);
    transition: all .25s ease;
    animation: fadeUp .8s ease both;
}
.chip:nth-child(1) { animation-delay: .15s; } .chip:nth-child(2) { animation-delay: .25s; }
.chip:nth-child(3) { animation-delay: .35s; } .chip:nth-child(4) { animation-delay: .45s; }
.chip:hover { transform: translateY(-3px); border-color: var(--violet); background: rgba(139,92,246,.18); }

/* ── Section titles ──────────────────────────────────── */
.section-title {
    display: flex; align-items: center; gap: .6rem;
    margin: 1.8rem 0 .9rem 0;
    font-size: 1.3rem; font-weight: 700;
    animation: fadeUp .6s ease both;
}
.section-title::after {
    content: ""; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--card-border), transparent);
}

/* ── Glass cards ─────────────────────────────────────── */
.glass {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.1rem 1.25rem;
    backdrop-filter: blur(10px);
    transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease;
    animation: fadeUp .7s ease both;
}
.glass:hover { transform: translateY(-4px); border-color: rgba(139,92,246,.55); box-shadow: 0 18px 40px -20px rgba(139,92,246,.6); }

/* ── Stats ───────────────────────────────────────────── */
.stat-label { font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }
.stat-value {
    font-size: 1.9rem; font-weight: 800; margin-top: .2rem;
    background: linear-gradient(90deg, var(--violet), var(--cyan));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── Entity badges ───────────────────────────────────── */
.ent-wrap { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .4rem; }
.ent {
    display: inline-flex; align-items: center; gap: .45rem;
    padding: .32rem .75rem; border-radius: 10px; font-size: .82rem; font-weight: 500;
    background: linear-gradient(135deg, rgba(139,92,246,.18), rgba(34,211,238,.12));
    border: 1px solid rgba(139,92,246,.4);
    transition: transform .2s ease;
    animation: fadeIn .6s ease both;
}
.ent:hover { transform: scale(1.06) rotate(-1deg); }
.ent .lbl { font-size: .68rem; padding: .08rem .45rem; border-radius: 6px; background: rgba(34,211,238,.18); color: var(--cyan); font-weight: 700; }

/* ── Query expansion ─────────────────────────────────── */
.expansion {
    border-left: 4px solid var(--cyan);
    background: linear-gradient(90deg, rgba(34,211,238,.10), transparent);
    border-radius: 0 14px 14px 0;
    padding: .9rem 1.1rem; margin-top: 1rem;
    animation: fadeUp .7s ease both;
}
.expansion b { color: var(--cyan); }
.expansion code { color: #fde68a; background: rgba(0,0,0,.35); padding: .15rem .4rem; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: .85rem; }

/* ── Sources ─────────────────────────────────────────── */
.src-card { display: flex; align-items: center; gap: .8rem; padding: .85rem 1rem; }
.src-ico {
    width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center; font-size: 1.1rem;
    background: linear-gradient(135deg, var(--violet), var(--indigo)); flex-shrink: 0;
}
.src-name { font-weight: 600; font-size: .9rem; word-break: break-word; }
.src-tag { font-size: .7rem; color: var(--muted); }

/* ── Score bars ──────────────────────────────────────── */
.score-row { margin: .5rem 0; }
.score-head { display: flex; justify-content: space-between; font-size: .78rem; color: var(--muted); margin-bottom: .25rem; }
.score-head b { color: var(--text); font-family: 'JetBrains Mono', monospace; }
.bar { height: 7px; border-radius: 10px; background: rgba(255,255,255,.08); overflow: hidden; }
.bar > span { display: block; height: 100%; border-radius: 10px; animation: barFill 1.2s cubic-bezier(.2,.8,.2,1) both; }
.bar.rerank > span { background: linear-gradient(90deg, var(--violet), var(--pink)); }
.bar.rrf    > span { background: linear-gradient(90deg, var(--cyan), var(--emerald)); }

.rank-pill {
    display: inline-block; padding: .15rem .7rem; border-radius: 999px; font-weight: 700; font-size: .78rem;
    background: linear-gradient(90deg, var(--amber), var(--pink)); color: #1b1030; margin-right: .5rem;
}
.mono { font-family: 'JetBrains Mono', monospace; font-size: .82rem; color: #c4b5fd; word-break: break-all; }

/* ── Streamlit widgets ───────────────────────────────── */
.stTextInput input, .stTextArea textarea, div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.06) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    transition: all .25s ease;
}
.stTextInput input { padding: .9rem 1rem !important; font-size: 1rem !important; }
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,.25) !important;
}
.stTextInput label, .stSelectbox label, .stSlider label { color: var(--muted) !important; font-weight: 600 !important; }

.stButton > button {
    position: relative; overflow: hidden;
    border-radius: 14px; border: 1px solid var(--card-border);
    background: rgba(255,255,255,.06); color: var(--text);
    font-weight: 600; padding: .65rem 1.4rem;
    transition: all .3s ease;
}
.stButton > button:hover { transform: translateY(-2px); border-color: var(--violet); color: #fff; box-shadow: 0 10px 25px -10px rgba(139,92,246,.7); }
.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, var(--violet), var(--indigo), var(--cyan));
    background-size: 200% 200%;
    border: none; color: #fff;
    animation: gradMove 6s ease infinite, pulseGlow 2.6s infinite;
}
.stButton > button[kind="primary"]::after {
    content: ""; position: absolute; top: 0; left: 0; width: 60%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,.35), transparent);
    animation: shimmer 2.8s infinite;
}
.stButton > button[kind="primary"]:hover { transform: translateY(-3px) scale(1.02); }

/* ── Sidebar ─────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13,19,38,.97), rgba(7,11,24,.97));
    border-right: 1px solid var(--card-border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
.side-brand {
    display: flex; align-items: center; gap: .7rem; padding: .8rem; border-radius: 16px;
    background: linear-gradient(135deg, rgba(139,92,246,.22), rgba(34,211,238,.12));
    border: 1px solid var(--card-border); margin-bottom: 1rem;
}
.side-brand .logo { font-size: 1.6rem; animation: floaty 3s ease-in-out infinite; }
.side-brand .t { font-weight: 800; line-height: 1.1; }
.side-brand .s { font-size: .7rem; color: var(--muted); }

/* ── Expanders & containers ──────────────────────────── */
div[data-testid="stExpander"] {
    background: var(--card); border: 1px solid var(--card-border) !important;
    border-radius: 16px; overflow: hidden; animation: fadeUp .7s ease both;
}
div[data-testid="stExpander"] summary { font-weight: 600; }
div[data-testid="stExpander"] summary:hover { color: var(--cyan); }

div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"] .answer-marker) {
    background: linear-gradient(135deg, rgba(139,92,246,.10), rgba(34,211,238,.06));
    border: 1px solid rgba(139,92,246,.35) !important;
    border-radius: 20px;
    box-shadow: 0 25px 50px -30px rgba(139,92,246,.7);
    animation: fadeUp .8s ease both;
}

.stAlert { border-radius: 14px; animation: fadeUp .5s ease both; }
code { font-family: 'JetBrains Mono', monospace !important; }
hr { border-color: var(--card-border) !important; }

.footer { text-align: center; color: var(--muted); font-size: .8rem; margin-top: 3rem; animation: fadeIn 1.5s ease both; }
.footer b { background: linear-gradient(90deg, var(--violet), var(--cyan)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def esc(value) -> str:
    """Escape any dynamic value before injecting it into HTML."""
    return html.escape(str(value))


def section(icon: str, title: str):
    st.markdown(f'<div class="section-title"><span>{icon}</span><span>{title}</span></div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
#  Hero header
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <span class="hero-badge"><span class="dot"></span> Production Hybrid RAG • Live</span>
        <div class="hero-title"><span class="hero-icon">💼</span> FinCon & Financial Regulatory Intelligence Assistant</div>
        <div class="hero-sub">
            Ask complex financial controlling &amp; regulatory questions and get grounded, citation-backed answers
            powered by hybrid retrieval and cross-encoder reranking.
        </div>
        <div class="chips">
            <span class="chip">🧬 Hybrid Retrieval</span>
            <span class="chip">🌳 Hierarchical Parent-Child Indexing</span>
            <span class="chip">🎯 Cross-Encoder Reranker</span>
            <span class="chip">📌 Citation Enforcement</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
#  Sidebar: Controls & Ingestion
# ──────────────────────────────────────────────────────────────
st.sidebar.markdown(
    """
    <div class="side-brand">
        <div class="logo">💼</div>
        <div><div class="t">FinCon RAG</div><div class="s">Regulatory Intelligence</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ Configuration & Pipeline")
top_k = st.sidebar.slider("Top-K Rerank Results", min_value=1, max_value=8, value=3)

if st.sidebar.button("🔄 Run Document Ingestion"):
    with st.spinner("Parsing documents & building Hybrid Indexes..."):
        try:
            run_ingestion_pipeline()
            st.sidebar.success("Ingestion and indexing complete!")
        except Exception as e:
            st.sidebar.error(f"Ingestion failed: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 2026 Financial Standards Queries")
sample_queries = [
    "What is the mandatory timeline for Form 8-K disclosure under SEC Item 1.05 for material cybersecurity incidents?",
    "What are the differences between Scope 1, Scope 2, and Scope 3 emissions under IFRS S2 in 2026?",
    "What are the eligibility criteria and turnover thresholds for EU CSRD Wave 2 compliance in 2026?",
    "What is the Basel III Endgame capital output floor percentage for risk-weighted assets?",
    "What confidence level is required for Expected Shortfall under the FRTB market risk framework?"
]

selected_sample = st.sidebar.selectbox("Choose a 2026 sample query:", [""] + sample_queries)


# Initialize pipeline
@st.cache_resource
def get_pipeline():
    return FinConRAGPipeline()


pipeline = get_pipeline()

# ──────────────────────────────────────────────────────────────
#  Main query input
# ──────────────────────────────────────────────────────────────
section("🧠", "Ask a Question")
user_query = st.text_input(
    "Enter your Financial Controlling / Accounting Question:",
    value=selected_sample if selected_sample else "",
    placeholder="e.g. What is the Basel III Endgame output floor?",
)

if st.button("🔍 Search & Analyze", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Executing Hybrid Retrieval, Reranking & Synthesis..."):
            result = pipeline.run(query=user_query, top_k_rerank=top_k)

            chunks = result.get("retrieved_child_chunks", []) or []
            sources = result.get("sources", []) or []
            entities = result.get("entities", []) or []

            # Quick stats row (display only)
            best_rerank = max([c.get("rerank_score", 0.0) or 0.0 for c in chunks], default=0.0)
            s1, s2, s3, s4 = st.columns(4)
            stats = [
                ("Sources Cited", len(sources)),
                ("Chunks Retrieved", len(chunks)),
                ("Entities Found", len(entities)),
                ("Best Rerank Score", f"{best_rerank:.3f}"),
            ]
            for col, (label, value) in zip((s1, s2, s3, s4), stats):
                col.markdown(
                    f'<div class="glass"><div class="stat-label">{label}</div><div class="stat-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )

            # 1. Answer section
            section("📝", "Financial Controlling Synthesis")
            with st.container(border=True):
                st.markdown('<span class="answer-marker"></span>', unsafe_allow_html=True)
                st.markdown(result["answer"])

            # Pre-Retrieval NER & Transformation
            if entities:
                ent_html = "".join(
                    f'<span class="ent">🏷️ {esc(e["text"])} <span class="lbl">{esc(e["label"])}</span></span>'
                    for e in entities
                )
                st.markdown(
                    f'<div class="glass" style="margin-top:1rem"><div class="stat-label">Recognized Financial Entities (spaCy)</div>'
                    f'<div class="ent-wrap">{ent_html}</div></div>',
                    unsafe_allow_html=True,
                )

            if result.get("expanded_query") and result.get("expanded_query") != user_query:
                st.markdown(
                    f'<div class="expansion">🔄 <b>Pre-Retrieval Query Expansion:</b> <code>{esc(result["expanded_query"])}</code></div>',
                    unsafe_allow_html=True,
                )

            # 2. Citations & Sources
            st.markdown("---")
            section("📚", "Source Attributions")
            cols = st.columns(len(sources) if sources else 1)
            for i, src in enumerate(sources):
                cols[i % len(cols)].markdown(
                    f'<div class="glass src-card" style="animation-delay:{i * 0.08:.2f}s">'
                    f'<div class="src-ico">📄</div>'
                    f'<div><div class="src-name">{esc(src)}</div><div class="src-tag">Verified source</div></div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            # 3. Transparent Retrieval Deep Dive
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            with st.expander("🔍 Deep Dive: Inspect Retrieved Child Chunks & Reranker Scores"):
                for idx, chunk in enumerate(chunks, start=1):
                    rerank = chunk.get("rerank_score", 0.0) or 0.0
                    rrf = chunk.get("rrf_score", 0.0) or 0.0
                    rerank_pct = max(0, min(100, rerank * 100)) if 0 <= rerank <= 1 else max(8, min(100, (rerank + 10) * 5))
                    rrf_pct = max(4, min(100, rrf * 60 * 100 / 1.0 if rrf <= 1 else 100))

                    st.markdown(
                        f'<span class="rank-pill">Rank {idx}</span><span class="mono">{esc(chunk["id"])}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"""
                        <div class="score-row">
                            <div class="score-head"><span>Cross-Encoder Rerank Score</span><b>{rerank:.4f}</b></div>
                            <div class="bar rerank"><span style="width:{rerank_pct:.1f}%"></span></div>
                        </div>
                        <div class="score-row">
                            <div class="score-head"><span>RRF Score</span><b>{rrf:.4f}</b></div>
                            <div class="bar rrf"><span style="width:{rrf_pct:.1f}%"></span></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.text_area(f"Child Chunk #{idx} Content", chunk["text"], height=100, key=f"child_{idx}")
                    st.markdown(
                        f'**Parent ID:** `{chunk.get("parent_id")}` | **Metadata:** {chunk.get("metadata")}'
                    )
                    st.markdown("---")

            # 4. Expanded Parent Contexts
            with st.expander("📖 Deep Dive: Full Parent Context Sent to LLM"):
                st.code(result["context_used"], language="markdown")

st.markdown(
    '<div class="footer">Built with ❤️ using <b>Hybrid RAG</b> • Streamlit • Cross-Encoder Reranking</div>',
    unsafe_allow_html=True,
)