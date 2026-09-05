import streamlit as st

from src.chatbot import answer_question
from src.claim_verifier import verify_claim
from src.ingest import ensure_seed_data


st.set_page_config(page_title="HealthGuard AI", page_icon="🏥", layout="wide")

ensure_seed_data()

st.markdown(
    """
    <style>
    .main .block-container { max-width: 980px; padding-top: 2rem; }
    .source-box {
        border: 1px solid #d7dee8;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.35rem 0;
        background: #f8fafc;
    }
    .status {
        display: inline-block;
        padding: .25rem .55rem;
        border-radius: 999px;
        background: #e8f5ee;
        border: 1px solid #b7e1c8;
        font-size: .9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("HealthGuard AI")
st.caption("Evidence-based healthcare assistant using local Ollama + RAG")

st.info(
    "HealthGuard AI provides general, evidence-based health information. "
    "It does not diagnose conditions, prescribe treatment, recommend medication doses, "
    "or replace a qualified healthcare professional."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Mode")
    mode = st.radio("Choose how to ask", ["Chat", "Verify Claim"], label_visibility="collapsed")
    st.caption("Powered only by local Ollama")
    st.divider()
    st.subheader("Demo questions")
    examples = [
        "Are antibiotics effective against viral infections such as common cold and flu?",
        "Is drinking a large amount of water very quickly always the fastest and safest way to treat dehydration?",
        "If antibiotics don't work against viruses, why might a doctor still prescribe them?",
        "Should someone start leftover antibiotics at home?",
        "What are the causes of soil salinity and how can farmers reduce it?",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example
    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown("**Sources**")
            for source in message["sources"]:
                title = source.get("title") or source.get("source") or "Source"
                url = source.get("url", "")
                st.markdown(f"- [{title}]({url})" if url else f"- {title}")

prompt = st.session_state.pop("pending_prompt", None) or st.chat_input(
    "Ask a healthcare question..." if mode == "Chat" else "Paste a health claim to verify..."
)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving evidence and checking safety..."):
            if mode == "Verify Claim":
                result = verify_claim(prompt)
            else:
                result = answer_question(prompt, st.session_state.messages)

        st.markdown(result["answer"])
        st.markdown(f"<span class='status'>{result['evidence_status']}</span>", unsafe_allow_html=True)

        if result.get("sources"):
            st.markdown("**Sources**")
            for source in result["sources"]:
                title = source.get("title") or source.get("source") or "Source"
                url = source.get("url", "")
                st.markdown(f"- [{title}]({url})" if url else f"- {title}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result.get("sources", []),
        }
    )
