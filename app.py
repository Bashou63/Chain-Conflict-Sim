import streamlit as st

# 1. 変更量の選択（ラジオボタンを横並びに！）
st.markdown("### 変更量")
delta_options = [1, 5, 10]
# ラジオボタンを横並びにするCSSハック
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
selected_delta = st.radio("変更量", delta_options, horizontal=True, label_visibility="collapsed")

st.markdown("---")

# 2. 各ステータス行の生成ロジック
def render_row(label, key):
    cols = st.columns([1, 1, 1, 1])
    cols[0].write(f"**{label}**")
    
    # マイナスボタン
    if cols[1].button("-", key=f"sub_{key}"):
        st.session_state[key] -= selected_delta
        st.rerun()
    
    # 現在値
    cols[2].write(f"**{st.session_state[key]}**")
    
    # プラスボタン
    if cols[3].button("+", key=f"add_{key}"):
        st.session_state[key] += selected_delta
        st.rerun()

# 実際に並べる
render_row("HP", "HP")
render_row("ATK", "ATK")
# ...以下同様
