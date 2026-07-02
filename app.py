import streamlit as st

# ステートの初期化（一度だけ実行）
if 'hp' not in st.session_state: st.session_state.hp = 100

def update_val(key, delta):
    st.session_state[key] += delta

# UIエリア
st.subheader("総合スコア: 92.8")

# HP調整の例（1行でコンパクトに）
c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
if c1.button("-10", key="hp-10"): update_val('hp', -10)
if c2.button("-1", key="hp-1"): update_val('hp', -1)
c3.text(f"HP: {st.session_state.hp}")
if c4.button("+1", key="hp+1"): update_val('hp', 1)
if c5.button("+10", key="hp+10"): update_val('hp', 10)
