import streamlit as st

# ボタン群を横に並べるための関数（columnsを駆使）
def render_compact_row(label, key, val):
    # 1行を [ラベル, 数値, -10, -1, +1, +10] の比率で分割
    cols = st.columns([2, 1, 1, 1, 1, 1])
    
    cols[0].write(f"**{label}**")
    cols[1].write(f"**{val}**")
    
    if cols[2].button("-10", key=f"{key}_m10"): st.session_state[key] -= 10
    if cols[3].button("-1",  key=f"{key}_m1"):  st.session_state[key] -= 1
    if cols[4].button("+1",  key=f"{key}_p1"):  st.session_state[key] += 1
    if cols[5].button("+10", key=f"{key}_p10"): st.session_state[key] += 10

# 総合スコア（一番上に固定）
st.subheader("📊 総合スコア: 7066")
st.markdown("---")

# 横並びでの配置（HPから順に）
# これにより、縦の長さがこれまでの1/4になります！
render_compact_row("HP", "HP", st.session_state.get("HP", 116))
render_compact_row("ATK", "ATK", st.session_state.get("ATK", 100))
render_compact_row("SP", "SP", st.session_state.get("SP", 100))
# ...以下同様にDEF, WT, 移動と続く
