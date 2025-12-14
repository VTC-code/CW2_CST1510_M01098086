import streamlit as st
import pandas as pd
from pathlib import Path
import importlib
import os

# Support both new (openai>=1.0.0) and legacy (openai<1.0.0) packages.
try:
    openai_mod = importlib.import_module("openai")
    OpenAI = getattr(openai_mod, "OpenAI", None)
    has_openai_v1 = OpenAI is not None
    openai_legacy = openai_mod
except Exception:
    OpenAI = None
    has_openai_v1 = False
    openai_legacy = None

# ------------------------------------------------------
# STREAMLIT SETUP
# ------------------------------------------------------
st.set_page_config(page_title="AI Chat", layout="wide")
st.title("AI Chat")

# ------------------------------------------------------
# OPENAI CLIENT (NEW API)
# ------------------------------------------------------
# Resolve API key from Streamlit secrets or environment
api_key = None
try:
    api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    api_key = None
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY")

# Build client for either new or legacy SDK
client = None
if api_key:
    if has_openai_v1 and OpenAI is not None:
        client = OpenAI(api_key=api_key)
    else:
        # Legacy client: set the api_key on the module and use it directly as `client`.
        if openai_legacy is not None:
            openai_legacy.api_key = api_key
            client = openai_legacy
        else:
            client = None
else:
    client = None
MODEL_NAME = "gpt-4o-mini"

# ------------------------------------------------------
# DATA SELECTION
# ------------------------------------------------------
base_dir = Path(__file__).parents[1]
data_dir = base_dir / "DATA"

choice = st.selectbox(
    "Dataset context",
    ["Cyber Incidents", "Datasets metadata", "IT tickets"]
)

def find_preview(choice):
    files = []

    if choice == "Cyber Incidents":
        files = list(data_dir.glob("cyber_incidents*.csv")) + list(base_dir.glob("cyber_incidents*.csv"))
    elif choice == "IT tickets":
        files = list(data_dir.glob("it_tickets*.csv")) + list(base_dir.glob("it_tickets*.csv"))
    else:
        files = (
            list(data_dir.glob("*metadata*.csv"))
            + list(data_dir.glob("*meta*.csv"))
            + list(base_dir.glob("*metadata*.csv"))
            + list(base_dir.glob("*.csv"))
        )

    if not files:
        return None, None, None

    fp = files[0]
    try:
        df = pd.read_csv(fp, nrows=20)
        preview_csv = df.head(10).to_csv(index=False)
        meta = {"path": str(fp), "columns": list(df.columns)}
        return fp, preview_csv, meta
    except Exception as e:
        return fp, None, {"error": str(e)}

fp, preview_csv, meta = find_preview(choice)

if fp:
    st.markdown(f"**Using:** `{fp}`")
    if st.checkbox("Show table preview"):
        st.dataframe(pd.read_csv(fp).head(10), use_container_width=True)
else:
    st.info("No CSV found for selected context.")

# ------------------------------------------------------
# CHAT STATE
# ------------------------------------------------------
if "ai_history" not in st.session_state:
    st.session_state.ai_history = []

# ------------------------------------------------------
# CHAT INPUT UI
# ------------------------------------------------------
col_msg, col_send = st.columns([8, 1])

with col_msg:
    user_input = st.text_area("Message", height=140)

with col_send:
    send = st.button("Send")

if st.button("Clear conversation"):
    st.session_state.ai_history = []
    st.rerun()

# ------------------------------------------------------
# SYSTEM PROMPT
# ------------------------------------------------------
system_prompt = (
    "You are a concise and helpful AI assistant. "
    "Use the dataset context when answering."
)

if preview_csv:
    system_prompt += f"\n\nDataset preview:\n{preview_csv[:3000]}"

messages = [{"role": "system", "content": system_prompt}]
messages.extend(st.session_state.ai_history)

# ------------------------------------------------------
# SEND MESSAGE (STREAMING)
# ------------------------------------------------------
if send and user_input.strip():
    st.session_state.ai_history.append(
        {"role": "user", "content": user_input}
    )
    messages.append({"role": "user", "content": user_input})

    out_box = st.empty()
    partial = ""

    try:
        # Prefer the modern OpenAI client (v1+)
        if hasattr(client, "chat") and hasattr(client.chat, "completions"):
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.2,
                stream=True,
            )
        else:
            # Fallback for older openai packages that expose ChatCompletion
            # (this will work if openai.ChatCompletion exists)
            try:
                import openai as _openai
                stream = _openai.ChatCompletion.create(model=MODEL_NAME, messages=messages, temperature=0.2, stream=True)
            except Exception as e2:
                raise

        for chunk in stream:
            # Support multiple possible chunk shapes from different SDK versions
            content_piece = None
            # new-style: object with .choices[0].delta.content
            try:
                if hasattr(chunk, "choices") and chunk.choices:
                    ch0 = chunk.choices[0]
                    # delta content (chat streaming)
                    if hasattr(ch0, "delta") and getattr(ch0.delta, "content", None) is not None:
                        content_piece = ch0.delta.content
                    # legacy text field
                    elif getattr(ch0, "text", None) is not None:
                        content_piece = ch0.text
            except Exception:
                content_piece = None

            # dict-like fallback
            if content_piece is None:
                try:
                    # chunk may be a dict
                    if isinstance(chunk, dict):
                        choices = chunk.get("choices") or []
                        if choices:
                            delta = choices[0].get("delta") or {}
                            content_piece = delta.get("content") or choices[0].get("text")
                except Exception:
                    content_piece = None

            if content_piece:
                partial += content_piece
                out_box.markdown(partial.replace("\n", "  \n"))

        st.session_state.ai_history.append({"role": "assistant", "content": partial})

    except Exception as e:
        # Surface a clearer message and hint for migration
        msg = str(e)
        if "ChatCompletion" in msg and "no longer supported" in msg:
            st.error("OpenAI SDK migration issue: your environment is using a mixture of old and new OpenAI SDK APIs.\nTry running `pip install --upgrade openai` to use the new API or pin to the old interface with `pip install openai==0.28`.")
        else:
            st.error(f"API error: {e}")

# ------------------------------------------------------
# SHOW RECENT CONVERSATION
# ------------------------------------------------------
if st.session_state.ai_history:
    st.divider()
    st.subheader("Conversation (recent)")
    for msg in st.session_state.ai_history[-6:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")
