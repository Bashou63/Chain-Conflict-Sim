import streamlit as st

# 1. ユニット選択とスコア（常に上部）
selected_name = st.selectbox("ユニット選択", ["Unit A", "Unit B"])
st.subheader("📊 総合スコア: 7066")

# 2. 2カラムでステータスを左右に配置（縦幅を半分にする）
st.markdown("---")
c1, c2 = st.columns(2)

# 右と左に半分ずつ配置
with c1:
    st.write("**HP**")
    st.write(f"{st.session_state.get('HP', 116)}")
    # ボタンは縦に並べるが、スペースを極小にする
    if st.button("-10", key="hp-10"): pass 
    if st.button("+10", key="hp+10"): pass

with c2:
    st.write("**ATK**")
    st.write(f"{st.session_state.get('ATK', 100)}")
    if st.button("-10", key="atk-10"): pass
    if st.button("+10", key="atk+10"): pass

# ※この構成なら、縦に伸びることなく、情報を画面の左右に詰め込めます！
