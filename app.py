import streamlit as st
from engine.router import process

st.set_page_config(
    page_title="Adaptive AI Inference Engine",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------
# Session State Initialization
# -------------------------------

if "rule_count" not in st.session_state:
    st.session_state.rule_count = 0

if "cache_count" not in st.session_state:
    st.session_state.cache_count = 0

if "ai_count" not in st.session_state:
    st.session_state.ai_count = 0

# -------------------------------
# Sidebar Dashboard
# -------------------------------

st.sidebar.title("📊 Live Statistics")

total = (
    st.session_state.rule_count
    + st.session_state.cache_count
    + st.session_state.ai_count
)

saved = 0

if total > 0:
    saved = (
        (st.session_state.rule_count + st.session_state.cache_count)
        / total
    ) * 100

st.sidebar.metric("Questions Asked", total)
st.sidebar.metric("Rule Hits", st.session_state.rule_count)
st.sidebar.metric("Cache Hits", st.session_state.cache_count)
st.sidebar.metric("AI Calls", st.session_state.ai_count)
st.sidebar.metric("AI Calls Saved", f"{saved:.1f}%")

st.sidebar.markdown("---")

st.sidebar.info(
    """
### Adaptive AI Inference Engine

Current Features

✅ Rule Engine

✅ Cache Engine

✅ AI Routing

✅ Live Metrics
"""
)

# -------------------------------
# Main Title
# -------------------------------

st.title("⚡ Adaptive AI Inference Engine")

st.write(
    "This system minimizes unnecessary AI inference by checking local rules "
    "and cached responses before sending requests to an AI model."
)

# -------------------------------
# User Input
# -------------------------------

question = st.text_input("Ask a question")

if st.button("Send"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    result = process(question)

    # -------------------------------
    # Update Statistics
    # -------------------------------

    if result["source"] == "Rule Engine":
        st.session_state.rule_count += 1

    elif result["source"] == "Cache":
        st.session_state.cache_count += 1

    else:
        st.session_state.ai_count += 1

    # -------------------------------
    # Display Answer
    # -------------------------------

    st.success(result["answer"])

    st.divider()

    st.subheader("Inference Details")
    st.divider()

    st.subheader("Decision Timeline")

    for step in result.get("timeline", []):
        st.write(step)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Execution Time",
        f"{result['metrics']['time']} ms"
    )

    col2.metric(
        "RAM Usage",
        f"{result['metrics']['ram']} MB"
    )

    col3.metric(
        "CPU Usage",
        f"{result['metrics']['cpu']} %"
    )

    st.divider()

    st.subheader("Routing Decision")

    if result["source"] == "Rule Engine":
        st.success("✅ Answered by Rule Engine")

    elif result["source"] == "Cache":
        st.warning("⚡ Answered by Cache (AI Call Avoided)")

    else:
        st.info("🤖 Answered by AI")

    st.divider()

    st.subheader("Inference Path")

    if result["source"] == "Rule Engine":

        st.code(
"""User
  │
  ▼
Rule Engine
  │
  ▼
Answer"""
        )

    elif result["source"] == "Cache":

        st.code(
"""User
  │
  ▼
Rule Engine
  │
(No Rule)
  │
  ▼
Cache
  │
(Cache Hit)
  │
  ▼
Answer"""
        )

    else:

        st.code(
"""User
  │
  ▼
Rule Engine
  │
(No Rule)
  │
  ▼
Cache
  │
(Cache Miss)
  │
  ▼
AI Model
  │
  ▼
Store in Cache
  │
  ▼
Answer"""
        )