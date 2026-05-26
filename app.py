import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
import base64

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🔐 CryptoVault",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* dark background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }

/* ── Hero title ── */
.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}
.hero-sub {
    text-align: center;
    color: #6b7280;
    font-size: 1.05rem;
    margin-bottom: 2.5rem;
    letter-spacing: 0.02em;
}

/* ── Cards ── */
.card-grid {
    display: flex;
    gap: 1.25rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.card {
    background: linear-gradient(145deg, #13131f, #1a1a2e);
    border: 1px solid #2a2a45;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    width: 200px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    text-decoration: none;
}
.card:hover {
    border-color: #7c3aed;
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(124, 58, 237, 0.25);
}
.card-emoji { font-size: 2.8rem; margin-bottom: 0.75rem; }
.card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #e2e2f0;
    line-height: 1.3;
}
.card-desc { font-size: 0.78rem; color: #6b7280; margin-top: 0.4rem; }

/* ── Section pages ── */
.page-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 2rem;
}
.page-emoji { font-size: 2.2rem; }
.page-title {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Result boxes ── */
.result-box {
    background: #0f0f1a;
    border: 1px solid #2a2a45;
    border-left: 4px solid #7c3aed;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #a78bfa;
    word-break: break-all;
    line-height: 1.6;
}
.result-label {
    font-size: 0.75rem;
    color: #6b7280;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.success-box {
    background: #0a1f17;
    border: 1px solid #065f46;
    border-left: 4px solid #34d399;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1.25rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    color: #6ee7b7;
    word-break: break-word;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    line-height: 1.75;
    max-width: 100%;
}
.error-box {
    background: #1f0a0a;
    border: 1px solid #7f1d1d;
    border-left: 4px solid #f87171;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.88rem;
    color: #fca5a5;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1f1f35;
    margin: 2rem 0;
}

/* ── Streamlit widget overrides ── */
.stTextInput > label, .stTextArea > label {
    color: #9ca3af !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}
.stTextInput input, .stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
    color: #e2e2f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.35) !important;
}

/* back button */
.back-btn > button {
    background: transparent !important;
    border: 1px solid #2a2a45 !important;
    color: #9ca3af !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.85rem !important;
}
.back-btn > button:hover {
    border-color: #7c3aed !important;
    color: #a78bfa !important;
    background: transparent !important;
    transform: none !important;
    box-shadow: none !important;
}

/* info callout */
.info-callout {
    background: #0f1629;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    font-size: 0.82rem;
    color: #93c5fd;
    margin-bottom: 1.25rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page: str):
    st.session_state.page = page
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="hero-title">🔐 CryptoVault</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Military-grade encryption at your fingertips · Powered by <b>Fernet</b></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card" style="border-color:#2a2a45;">
            <div class="card-emoji">🗝️</div>
            <div class="card-title">Generate a Key</div>
            <div class="card-desc">Generate a secret key</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="go_keygen", use_container_width=True):
            go("keygen")

    with col2:
        st.markdown("""
        <div class="card" style="border-color:#2a2a45;">
            <div class="card-emoji">🔒</div>
            <div class="card-title">Encrypt Message</div>
            <div class="card-desc">Lock your message securely</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="go_encrypt", use_container_width=True):
            go("encrypt")

    with col3:
        st.markdown("""
        <div class="card" style="border-color:#2a2a45;">
            <div class="card-emoji">🔓</div>
            <div class="card-title">Decrypt Message</div>
            <div class="card-desc">Unlock your secret message</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open →", key="go_decrypt", use_container_width=True):
            go("decrypt")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    # FIRST
    st.markdown("""
    <div style="
        text-align:center; 
        color:#374151; 
        font-size:1rem; 
        margin-top:1rem;
        font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;
    ">
        🛡️ All encryption happens locally in your browser session &nbsp;·&nbsp; No data is stored or transmitted
    </div>

    <div style="
        text-align:center; 
        color:#4b5563; 
        font-size:2.3rem; 
        margin-top:0.8rem;
        font-weight:600;
        font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;
    ">
        Crafted with ☕ and code by Yuvraj
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KEY GENERATION PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "keygen":
    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="back_keygen"):
            go("home")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <span class="page-emoji">🗝️</span>
        <span class="page-title">Generate a Key</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-callout">
        💡 A <b>Fernet key</b> is a randomly generated 256-bit secret. Keep it safe — 
        without it you <b>cannot</b> decrypt your messages! 🚨
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        generate_clicked = st.button("✨ Generate Key", key="gen_btn", use_container_width=True)

    if generate_clicked:
        key = Fernet.generate_key().decode()
        st.session_state.generated_key = key

    if "generated_key" in st.session_state and st.session_state.generated_key:
        st.markdown('<div class="result-label">🔑 Your Secret Key</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{st.session_state.generated_key}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:1rem; font-size:0.82rem; color:#6b7280; text-align:center;">
            📋 Copy this key and store it somewhere safe.<br>
            🔁 Hit the button again to generate a fresh key.
        </div>
        """, unsafe_allow_html=True)

        # copy-to-clipboard convenience via st.code
        st.code(st.session_state.generated_key, language=None)

    # SECOND
    st.markdown("""
    <div style="
        text-align:center; 
        color:#4b5563; 
        font-size:2.3rem; 
        margin-top:2.5rem;
        font-weight:600;
        font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;
    ">
        Crafted with ☕ and code by Yuvraj
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENCRYPT PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "encrypt":
    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="back_encrypt"):
            go("home")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <span class="page-emoji">🔐</span>
        <span class="page-title">Encrypt Message</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-callout">
        🗝️ Paste your <b>Fernet key</b> below (generated from the Key page), 
        then type your secret message. We'll lock it up tight! 💪
    </div>
    """, unsafe_allow_html=True)

    enc_key = st.text_input(
        "🔑 Encryption Key",
        placeholder="Paste your Fernet key here…",
        key="enc_key_input",
    )
    plain_text = st.text_area(
        "📝 Plain Text Message",
        placeholder="Type your secret message here…",
        height=130,
        key="plain_input",
    )

    encrypt_clicked = st.button("🔒 Encrypt Message", key="enc_btn", use_container_width=False)

    if encrypt_clicked:
        if not enc_key.strip():
            st.markdown('<div class="error-box">⚠️ Please provide an encryption key!</div>', unsafe_allow_html=True)
        elif not plain_text.strip():
            st.markdown('<div class="error-box">⚠️ Please enter a message to encrypt!</div>', unsafe_allow_html=True)
        else:
            try:
                f = Fernet(enc_key.strip().encode())
                encrypted = f.encrypt(plain_text.encode()).decode()
                st.session_state.encrypted_result = encrypted
            except Exception:
                st.markdown('<div class="error-box">❌ Invalid key format! Make sure you\'re using a valid Fernet key 🗝️</div>', unsafe_allow_html=True)
                st.session_state.encrypted_result = None

    if st.session_state.get("encrypted_result"):
        st.markdown('<div class="result-label">🔐 Encrypted Message</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{st.session_state.encrypted_result}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:0.75rem; font-size:0.82rem; color:#6b7280; text-align:center;">
            ✅ Message encrypted successfully! Share it safely.<br>
            🚨 The recipient will need your <b>key</b> to decrypt it.
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state.encrypted_result, language=None)

    # SECOND
    st.markdown("""
    <div style="
        text-align:center; 
        color:#4b5563; 
        font-size:2.3rem; 
        margin-top:2.5rem;
        font-weight:600;
        font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;
    ">
        Crafted with ☕ and code by Yuvraj
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DECRYPT PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "decrypt":
    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="back_decrypt"):
            go("home")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="page-header">
        <span class="page-emoji">🔓</span>
        <span class="page-title">Decrypt Message</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-callout">
        🕵️ Enter the <b>original key</b> used to encrypt the message and 
        paste the encrypted ciphertext below to reveal the secret! 🎉
    </div>
    """, unsafe_allow_html=True)

    dec_key = st.text_input(
        "🔑 Decryption Key",
        placeholder="Paste your Fernet key here…",
        key="dec_key_input",
    )
    cipher_text = st.text_area(
        "🔐 Encrypted Message",
        placeholder="Paste your encrypted message here…",
        height=130,
        key="cipher_input",
    )

    decrypt_clicked = st.button("🔓 Decrypt Message", key="dec_btn", use_container_width=False)

    if decrypt_clicked:
        if not dec_key.strip():
            st.markdown('<div class="error-box">⚠️ Please provide a decryption key!</div>', unsafe_allow_html=True)
        elif not cipher_text.strip():
            st.markdown('<div class="error-box">⚠️ Please enter an encrypted message!</div>', unsafe_allow_html=True)
        else:
            try:
                f = Fernet(dec_key.strip().encode())
                decrypted = f.decrypt(cipher_text.strip().encode()).decode()
                st.session_state.decrypted_result = decrypted
                st.session_state.decrypt_error = None
            except InvalidToken:
                st.session_state.decrypt_error = "❌ Decryption failed! The key or encrypted message is incorrect. Double-check both and try again 🔍"
                st.session_state.decrypted_result = None
            except Exception as e:
                st.session_state.decrypt_error = f"❌ Something went wrong: {str(e)}"
                st.session_state.decrypted_result = None

    if st.session_state.get("decrypt_error"):
        st.markdown(f'<div class="error-box">{st.session_state.decrypt_error}</div>', unsafe_allow_html=True)

    if st.session_state.get("decrypted_result"):
        st.markdown('<div class="result-label">✉️ Decrypted Message</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="success-box">🎉 &nbsp;{st.session_state.decrypted_result}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="margin-top:0.75rem; font-size:0.82rem; color:#6b7280; text-align:center;">
            ✅ Message decrypted successfully! Your secret is revealed 🤫
        </div>
        """, unsafe_allow_html=True)

    # SECOND
    st.markdown("""
    <div style="
        text-align:center; 
        color:#4b5563; 
        font-size:2.3rem; 
        margin-top:2.5rem;
        font-weight:600;
        font-family:Segoe UI Emoji, Apple Color Emoji, Noto Color Emoji, sans-serif;
    ">
        Crafted with ☕ and code by Yuvraj
    </div>
    """, unsafe_allow_html=True)