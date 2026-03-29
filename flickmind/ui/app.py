import os
import sys
import time
import streamlit as st
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

st.set_page_config(
    page_title="FlickMind",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #070b14;
    color: #e2e8f4;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #0b1120;
    border-right: 1px solid #1a2540;
}

.fm-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    letter-spacing: -1px;
    color: #fff;
    text-align: center;
    line-height: 1;
}
.fm-logo span { color: #6366f1; }

.fm-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: #3d4f6e;
    text-align: center;
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 20px;
}

.status-ok {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: #10b981;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}
.status-err {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    color: #ef4444;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.sidebar-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: #2a3a58;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 8px;
    margin-top: 16px;
}

.coll-card {
    background: #0f1a2e;
    border: 1px solid #1a2a45;
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.coll-card-icon { font-size: 1.3rem; line-height: 1; }
.coll-card-name {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    color: #c8d6f0;
}
.coll-card-desc { font-size: 0.67rem; color: #3d4f6e; margin-top: 2px; }

.stButton > button {
    background: #0f1a2e !important;
    color: #7c9cc0 !important;
    border: 1px solid #1a2a45 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #162035 !important;
    color: #a5bfe0 !important;
    border-color: #2d4a70 !important;
}

.chat-user {
    background: linear-gradient(135deg, #111c33, #0f1a2e);
    border: 1px solid #1e3057;
    border-radius: 0 12px 12px 12px;
    padding: 14px 18px;
    margin: 10px 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    line-height: 1.6;
}
.chat-assistant {
    background: #0b1120;
    border: 1px solid #161f35;
    border-left: 3px solid #6366f1;
    border-radius: 0 12px 12px 12px;
    padding: 14px 18px;
    margin: 10px 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.92rem;
    line-height: 1.7;
}
.chat-label-user {
    font-family: 'Syne', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 3px;
    color: #6366f1;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 6px;
}
.chat-label-ai {
    font-family: 'Syne', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 3px;
    color: #a78bfa;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 6px;
}

.coll-badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.67rem;
    letter-spacing: 1px;
    color: #818cf8;
    margin-right: 4px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.mood-tag {
    display: inline-block;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.67rem;
    color: #fbbf24;
    margin-right: 4px;
    font-family: 'DM Sans', sans-serif;
}

.transform-card {
    background: #0b1120;
    border: 1px solid #1a2540;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 8px 0;
}
.transform-card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: #a5b4fc;
    letter-spacing: 0.5px;
}
.transform-card-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    color: #7c8fb0;
    margin-top: 6px;
    line-height: 1.55;
}

.token-info {
    font-size: 0.68rem;
    color: #2a3a58;
    text-align: right;
    margin-top: 8px;
    font-family: 'DM Sans', sans-serif;
}

.page-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}
.page-header-icon {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border-radius: 12px;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
}
.page-header-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #e2e8f4;
}
.page-header-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: #3d4f6e;
}

.stat-box {
    background: #0b1120;
    border: 1px solid #1a2540;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #6366f1;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    color: #3d4f6e;
    margin-top: 4px;
    font-family: 'DM Sans', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stTextInput > div > div > input {
    background-color: #0b1120 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 10px !important;
    color: #e2e8f4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

.stFormSubmitButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    padding: 10px 22px !important;
}

hr { border-color: #1a2540 !important; }

details > summary {
    background: #0b1120 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #7c9cc0 !important;
    padding: 10px 14px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Client management ────────────────────────────────────

def init_client():
    if "weaviate_client" not in st.session_state:
        import weaviate
        try:
            client = weaviate.connect_to_weaviate_cloud(
                cluster_url=os.environ["WEAVIATE_URL"],
                auth_credentials=weaviate.auth.AuthApiKey(os.environ["WEAVIATE_API_KEY"]),
                headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
            )
            st.session_state["weaviate_client"] = client
            st.session_state["client_error"] = None
        except Exception as e:
            st.session_state["weaviate_client"] = None
            st.session_state["client_error"] = str(e)


def reconnect_client():
    old = st.session_state.pop("weaviate_client", None)
    if old:
        try:
            old.close()
        except Exception:
            pass
    st.session_state.pop("client_error", None)
    init_client()


# ─── Sidebar ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="fm-logo">Flick<span>Mind</span></div>'
            '<div class="fm-tagline">AI Cinema Intelligence</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.markdown('<div class="sidebar-label">Database</div>', unsafe_allow_html=True)
        if st.session_state.get("weaviate_client"):
            st.markdown('<span class="status-ok">● Connected to Weaviate</span>', unsafe_allow_html=True)
        else:
            err = st.session_state.get("client_error", "Not connected")
            st.markdown(f'<span class="status-err">● {err[:55]}</span>', unsafe_allow_html=True)
            if st.button("🔄 Retry connection", use_container_width=True):
                reconnect_client()
                st.rerun()

        st.markdown("---")

        st.markdown('<div class="sidebar-label">Collections</div>', unsafe_allow_html=True)
        for icon, name, desc in [
            ("🎥", "Movies", "12 films · rating, plot, awards"),
            ("📺", "TVSeries", "10 shows · network, seasons, status"),
            ("🎬", "Directors", "6 directors · biography & style"),
        ]:
            st.markdown(
                f'<div class="coll-card">'
                f'<div class="coll-card-icon">{icon}</div>'
                f'<div><div class="coll-card-name">{name}</div>'
                f'<div class="coll-card-desc">{desc}</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown('<div class="sidebar-label">Quick Stats</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="stat-box"><div class="stat-num">28</div><div class="stat-label">Items</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="stat-box"><div class="stat-num">3</div><div class="stat-label">Collections</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="stat-box"><div class="stat-num">AI</div><div class="stat-label">Powered</div></div>', unsafe_allow_html=True)

        if st.session_state.get("last_usage"):
            st.markdown("---")
            st.markdown('<div class="sidebar-label">Last Query</div>', unsafe_allow_html=True)
            usage = st.session_state["last_usage"]
            if isinstance(usage, int) and usage > 0:
                st.caption(f"Tokens used: {usage}")
            elif isinstance(usage, dict):
                total = usage.get("total_tokens") or usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                if total:
                    st.caption(f"Tokens used: {total}")

        st.markdown("---")
        st.markdown('<div class="sidebar-label">Example Queries</div>', unsafe_allow_html=True)
        for eq in [
            "Recommend a high-rated crime film",
            "What is Nolan's directing style?",
            "How many HBO series have rating above 9?",
            "I want something dark and psychologically intense",
            "Which TV series are still ongoing?",
            "Compare Parasite and Oldboy",
        ]:
            if st.button(eq, key=f"ex_{eq[:22]}", use_container_width=True):
                if st.session_state.get("prefill_query") != eq:
                    st.session_state["prefill_query"] = eq
                    st.rerun()

        st.markdown("---")
        st.markdown('<div class="sidebar-label">Transformation Agent</div>', unsafe_allow_html=True)
        st.caption("Enrich data with AI-generated properties")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎥 ai_summary", use_container_width=True):
                st.session_state["run_transform"] = "movies"
        with col2:
            if st.button("📺 ai_tags", use_container_width=True):
                st.session_state["run_transform"] = "series"

        st.markdown("---")
        if st.button("🗑️ Clear chat history", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state.pop("last_usage", None)
            st.rerun()


# ─── Transformation handler ───────────────────────────────

def handle_transformation():
    transform_type = st.session_state.pop("run_transform", None)
    if not transform_type:
        return

    client = st.session_state.get("weaviate_client")
    if not client:
        st.error("Weaviate is not connected. Check your .env file.")
        return

    from agents.transformation_agent import (
        add_ai_summary_to_movies,
        add_ai_tags_to_series,
        wait_for_workflow,
        get_transformed_samples,
    )

    with st.expander("🔄 Transformation Agent – Results", expanded=True):
        with st.spinner("Transformation Agent running — please wait (~1-3 min)..."):
            try:
                if transform_type == "movies":
                    wf_id = add_ai_summary_to_movies(client)
                    status = wait_for_workflow(client, "Movies", wf_id, timeout_sec=120)
                    if status == "completed":
                        samples = get_transformed_samples(client, "Movies", "ai_summary", limit=4)
                        st.success(f"✓ Transformation complete! (workflow: `{wf_id[:16]}...`)")
                        st.markdown("**Sample ai_summary results:**")
                        for s in samples:
                            st.markdown(
                                f'<div class="transform-card">'
                                f'<div class="transform-card-title">{s["title"]}</div>'
                                f'<div class="transform-card-body">{s.get("ai_summary", "—")}</div>'
                                f"</div>",
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning(f"Status: **{status}**. Check your Weaviate Cloud Console.")
                else:
                    wf_id = add_ai_tags_to_series(client)
                    status = wait_for_workflow(client, "TVSeries", wf_id, timeout_sec=120)
                    if status == "completed":
                        samples = get_transformed_samples(client, "TVSeries", "ai_tags", limit=4)
                        st.success(f"✓ Transformation complete! (workflow: `{wf_id[:16]}...`)")
                        st.markdown("**Sample ai_tags results:**")
                        for s in samples:
                            tags = s.get("ai_tags", "")
                            tag_html = " ".join(
                                f'<span class="mood-tag">{t.strip()}</span>'
                                for t in tags.split(",") if t.strip()
                            )
                            st.markdown(
                                f'<div class="transform-card">'
                                f'<div class="transform-card-title">{s["title"]}</div>'
                                f'<div class="transform-card-body">{tag_html}</div>'
                                f"</div>",
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning(f"Status: **{status}**. Check your Weaviate Cloud Console.")
            except Exception as e:
                st.error(f"Transformation Agent error: {e}")


# ─── NEW: Mood Search ─────────────────────────────────────

MOOD_MAP = {
    "🌑 Dark & Intense": "dark psychological intense thriller crime drama",
    "😂 Fun & Light": "comedy fun feel-good lighthearted entertaining",
    "🤯 Mind-Bending": "mind-bending twist complex philosophical surreal",
    "❤️ Romantic": "romance love emotional heartwarming relationship",
    "🚀 Action & Epic": "action epic adventure spectacle blockbuster",
    "🏆 Award-Winning": "Oscar award critically acclaimed masterpiece prestigious",
}

def render_mood_filter():
    st.markdown("---")
    st.markdown(
        '<div class="page-header">'
        '<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);border-radius:12px;'
        'width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;">🎭</div>'
        '<div><div class="page-header-title">Mood Search</div>'
        '<div class="page-header-sub">Pick a vibe — FlickMind finds the perfect match</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, (mood, _) in enumerate(MOOD_MAP.items()):
        with cols[i % 3]:
            if st.button(mood, key=f"mood_{i}", use_container_width=True):
                query = f"Recommend something with this vibe: {MOOD_MAP[mood]}"
                if st.session_state.get("prefill_query") != query:
                    st.session_state["prefill_query"] = query
                    st.rerun()


# ─── Chat ─────────────────────────────────────────────────

def render_chat():
    st.markdown("---")
    st.markdown(
        '<div class="page-header">'
        '<div style="background:linear-gradient(135deg,#4f46e5,#6366f1);border-radius:12px;'
        'width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;">🎥</div>'
        '<div><div class="page-header-title">Ask FlickMind</div>'
        '<div class="page-header-sub">Multi-collection Query Agent with full conversation memory</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">'
                f'<div class="chat-label-user">You</div>'
                f"{msg['content']}"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            badges_html = ""
            if msg.get("collections"):
                badges_html = '<div style="margin-bottom:8px">' + "".join(
                    f'<span class="coll-badge">{c}</span>' for c in msg["collections"]
                ) + "</div>"

            usage_html = ""
            if msg.get("usage"):
                usage = msg["usage"]
                total = 0
                if isinstance(usage, int):
                    total = usage
                elif isinstance(usage, dict):
                    total = usage.get("total_tokens") or usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                if total:
                    usage_html = f'<div class="token-info">~{total} tokens</div>'

            st.markdown(
                f'<div class="chat-assistant">'
                f'<div class="chat-label-ai">FlickMind</div>'
                f"{badges_html}"
                f"{msg['content']}"
                f"{usage_html}"
                f"</div>",
                unsafe_allow_html=True,
            )

    prefill = st.session_state.pop("prefill_query", "")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Question:",
            value=prefill,
            placeholder="e.g. Recommend a Korean thriller with a high rating...",
            label_visibility="collapsed",
        )
        send = st.form_submit_button("Send →", use_container_width=False)

    if send and user_input.strip():
        client = st.session_state.get("weaviate_client")
        if not client:
            st.error("Weaviate is not connected. Check your .env file.")
            return

        st.session_state["messages"].append({"role": "user", "content": user_input})

        from agents.query_agent import ask
        history_for_agent = st.session_state["messages"][:-1]

        with st.spinner("Searching the database..."):
            try:
                result = ask(user_input, client, conversation_history=history_for_agent)
                answer = result["answer"]
                collections_used = result.get("collections", [])
                usage = result.get("usage")
            except Exception as e:
                answer = f"⚠️ Error executing query: {e}"
                collections_used = []
                usage = None

        st.session_state["messages"].append({
            "role": "assistant",
            "content": answer,
            "collections": collections_used,
            "usage": usage,
        })
        if usage:
            st.session_state["last_usage"] = usage

        st.rerun()


# ─── NEW: Export conversation ─────────────────────────────

def render_export():
    messages = st.session_state.get("messages", [])
    if not messages:
        return
    st.markdown("---")
    with st.expander("📥 Export conversation"):
        lines = []
        for m in messages:
            role = "You" if m["role"] == "user" else "FlickMind"
            lines.append(f"{role}: {m['content']}\n")
        export_text = "\n".join(lines)
        st.download_button(
            label="⬇️ Download as .txt",
            data=export_text,
            file_name="flickmind_conversation.txt",
            mime="text/plain",
        )


# ─── Main ─────────────────────────────────────────────────

def main():
    required = ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        st.error(
            f"Missing environment variables: **{', '.join(missing)}**\n\n"
            "Copy `.env.example` → `.env` and fill in your credentials."
        )
        st.stop()

    init_client()
    render_sidebar()
    handle_transformation()
    render_mood_filter()
    render_chat()
    render_export()


if __name__ == "__main__":
    main()
