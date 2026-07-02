import streamlit as st

# 1. ユニット選択（画面上部）
unit_name = st.selectbox("ユニット選択", ["Unit A", "Unit B"])

# 2. 総合スコア（視認性最優先）
st.markdown("---")
st.subheader("📊 総合スコア: 92.8")
st.markdown("---")

# 3. ボタンと数値を「横1列」に詰め込む関数
def render_compact_row(label, key):
    if key not in st.session_state: st.session_state[key] = 100
    
    # 5つのカラムで横並びに強制
    # 項目名: [1]、ボタン4つ: [1,1,2,1,1] の比率で配置
    cols = st.columns([1.5, 1, 1, 2, 1, 1])
    cols[0].write(f"**{label}**")
    
    if cols[1].button("-10", key=f"{key}-10"): st.session_state[key] -= 10
    if cols[2].button("-1", key=f"{key}-1"): st.session_state[key] -= 1
    cols[3].write(f"<div style='text-align:center; font-size:1.2rem;'>{st.session_state[key]}</div>", unsafe_allow_html=True)
    if cols[4].button("+1", key=f"{key}+1"): st.session_state[key] += 1
    if cols[5].button("+10", key=f"{key}+10"): st.session_state[key] += 10

# 項目をずらりと横1列で配置（これなら縦幅を取りません！）
render_compact_row("HP", "hp")
render_compact_row("ATK", "atk")
render_compact_row("SP", "sp")
render_compact_row("DEF", "def")
render_compact_row("WT", "wt")
render_compact_row("移動", "mv")
