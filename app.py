import streamlit as st

st.set_page_config(layout="centered")

# --- 1. 絶対にエラーを吐かない初期化処理 ---
def init_state():
    defaults = {'HP': 100, 'ATK': 70, 'SP': 20, 'DEF': 30, 'WT': 500, 'MV': 4}
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    if 'delta' not in st.session_state:
        st.session_state['delta'] = 1

init_state()

# --- 2. UI構築 ---
st.subheader("📊 総合スコア: 7066")

# 変更量の選択
st.write("### 変更量")
cols_d = st.columns(3)
if cols_d[0].button("1", use_container_width=True): st.session_state.delta = 1
if cols_d[1].button("5", use_container_width=True): st.session_state.delta = 5
if cols_d[2].button("10", use_container_width=True): st.session_state.delta = 10
st.write(f"現在の変更量: **{st.session_state.delta}**")
st.markdown("---")

# 各ステータス行の生成
def render_row(label, key):
    # 4カラムで[ラベル, -, 数値, +]を構成
    cols = st.columns([2, 1, 1, 1])
    cols[0].write(f"**{label}**")
    
    if cols[1].button("-", key=f"sub_{key}"):
        st.session_state[key] -= st.session_state.delta
        st.rerun()
    
    cols[2].write(f"**{st.session_state[key]}**")
    
    if cols[3].button("+", key=f"add_{key}"):
        st.session_state[key] += st.session_state.delta
        st.rerun()

render_row("HP", "HP")
render_row("ATK", "ATK")
render_row("SP", "SP")
render_row("DEF", "DEF")
render_row("WT", "WT")
render_row("MOV", "MV")
