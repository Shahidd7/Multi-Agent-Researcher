import streamlit as st
from pipeline import run_research_pipeline


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0b0f19;
        color: #f5f7fa;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #ffffff, #8b9cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Cards */
    .card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
    }

    .muted {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    /* Agent status */
    .agent-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 1rem;
        min-height: 130px;
    }

    .agent-icon {
        font-size: 1.7rem;
    }

    .agent-name {
        font-weight: 700;
        font-size: 1rem;
        margin-top: 0.3rem;
    }

    .agent-status {
        color: #22c55e;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }

    /* Score */
    .score-card {
        background: linear-gradient(
            135deg,
            #111827,
            #171d32
        );
        border: 1px solid #29324a;
        border-radius: 18px;
        padding: 1.5rem;
        text-align: center;
    }

    .score {
        font-size: 3.5rem;
        font-weight: 800;
    }

    /* Source */
    .source-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #080c14;
        border-right: 1px solid #1f2937;
    }

    /* Button */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        height: 3rem;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🔎 AI Research Agent")

    st.markdown(
        """
        <div class="muted">
        Multi-agent web research system powered by
        LLMs, Tavily and web scraping.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ⚙️ Pipeline")

    st.markdown(
        """
        **01** 🔍 Search Agent  
        Finds relevant sources using Tavily.

        **02** 📖 Reader Agent  
        Scrapes and extracts useful information.

        **03** ✍️ Writer Agent  
        Creates the final research report.

        **04** 🧑‍⚖️ Critic Agent  
        Reviews and scores the report.
        """
    )

    st.divider()

    st.markdown("### 🧠 Stack")

    st.caption("LangChain")
    st.caption("LangGraph / Agents")
    st.caption("Groq")
    st.caption("Tavily")
    st.caption("BeautifulSoup")
    st.caption("FastAPI / Python")
    st.caption("Streamlit")

    st.divider()

    st.caption("AI Research Agent • 2026")


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    '<div class="hero-title">AI Research Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Research the web. Read the evidence. Write the report. Critique the result.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# QUERY SECTION
# ---------------------------------------------------------

st.markdown("### 🔍 What do you want to research?")

topic = st.text_area(
    label="Research topic",
    placeholder=(
        "Example: Compare the latest open-source AI models "
        "released in 2026."
    ),
    height=100,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    research_button = st.button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )

if clear_button:
    st.session_state.pop("research_state", None)
    st.rerun()


# ---------------------------------------------------------
# RESEARCH EXECUTION
# ---------------------------------------------------------

if research_button:

    if not topic.strip():

        st.warning("Please enter a research topic first.")

    else:

        with st.status(
            "🤖 AI agents are researching...",
            expanded=True
        ) as status:

            st.write("🔍 Search Agent → searching the web...")
            st.write("📖 Reader Agent → analyzing relevant sources...")
            st.write("✍️ Writer Agent → generating research report...")
            st.write("🧑‍⚖️ Critic Agent → reviewing the report...")

            try:

                result = run_research_pipeline(topic.strip())

                st.session_state["research_state"] = result
                st.session_state["topic"] = topic.strip()

                status.update(
                    label="✅ Research completed",
                    state="complete",
                    expanded=False
                )

            except Exception as e:

                status.update(
                    label="❌ Research failed",
                    state="error"
                )

                st.error(f"Something went wrong: {e}")


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if "research_state" in st.session_state:

    state = st.session_state["research_state"]

    st.divider()

    # -----------------------------------------------------
    # AGENT PIPELINE
    # -----------------------------------------------------

    st.markdown("### 🤖 Agent Pipeline")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="agent-box">
                <div class="agent-icon">🔍</div>
                <div class="agent-name">Search Agent</div>
                <div class="agent-status">● Completed</div>
                <div class="muted">Tavily web search</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="agent-box">
                <div class="agent-icon">📖</div>
                <div class="agent-name">Reader Agent</div>
                <div class="agent-status">● Completed</div>
                <div class="muted">Web page scraping</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="agent-box">
                <div class="agent-icon">✍️</div>
                <div class="agent-name">Writer Agent</div>
                <div class="agent-status">● Completed</div>
                <div class="muted">Report generation</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            """
            <div class="agent-box">
                <div class="agent-icon">🧑‍⚖️</div>
                <div class="agent-name">Critic Agent</div>
                <div class="agent-status">● Completed</div>
                <div class="muted">Quality evaluation</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # -----------------------------------------------------
    # RESEARCH REPORT
    # -----------------------------------------------------

    st.markdown("### 📄 Research Report")

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(state.get("report", "No report generated."))

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # CRITIC
    # -----------------------------------------------------

    st.markdown("### 🧑‍⚖️ Research Evaluation")

    feedback = state.get(
        "feedback",
        "No critic feedback available."
    )

    # Try to extract score
    score_text = "N/A"

    for line in feedback.splitlines():

        if "Score:" in line:
            score_text = line.replace("Score:", "").strip()
            break

    score_col, feedback_col = st.columns([1, 3])

    with score_col:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="muted">Research Score</div>
                <div class="score">{score_text}</div>
                <div class="muted">AI Critic Evaluation</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feedback_col:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(feedback)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # AGENT TRACE / PROOF
    # -----------------------------------------------------

    st.markdown("### 🔬 Agent Trace")

    st.caption(
        "Expand these sections to see what each stage of the pipeline produced."
    )

    with st.expander("🔍 Search Agent — Tavily Results"):

        st.markdown(
            state.get(
                "search_results",
                "No search results."
            )
        )

    with st.expander("📖 Reader Agent — Scraped Content"):

        st.markdown(
            state.get(
                "scraped_content",
                "No scraped content."
            )
        )

    with st.expander("🧠 Full Pipeline State"):

        st.json(
            {
                "topic": st.session_state.get("topic"),
                "search_results": state.get("search_results"),
                "scraped_content": state.get("scraped_content"),
                "report": state.get("report"),
                "feedback": state.get("feedback")
            }
        )


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.divider()

    st.caption(
        "Built with Python • LangChain • Groq • Tavily • BeautifulSoup • Streamlit"
    )