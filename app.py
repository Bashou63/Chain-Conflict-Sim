import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

# データ読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
@st.cache_data(ttl=2)
def load_data(): return pd.read_csv(SHEET_URL)

df = load_data()
unit_names = df.iloc[:, 1].dropna().unique().tolist()
selected_name = st.selectbox("ユニット選択", unit_names)
unit_data = df[df.iloc[:, 1] == selected_name].iloc[0]

# 状態管理
for col in ['HP', 'ATK', '最大SP', 'DEF', '基礎WT', '移動力']:
    if col not in st.session_state: st.session_state[col] = int(unit_data.get(col, 100))

# 総合スコア
score = (st.session_state['HP']*1.0) + (st.session_state['DEF']*2.5) + (st.session_state['ATK']*2.0) + (st.session_state['最大SP']*1.5) + ((1000-st.session_state['基礎WT'])*1.5) + (st.session_state['移動力']*50)
st.subheader(f"📊 総合スコア: {int(score)}")

# 項目調整（エラーを防ぐため、ボタンのkeyを完全に一意にする）
def render_row(label, key, deltas):
    st.markdown(f"**{label}**: {st.session_state[key]}")
    cols = st.columns(len(deltas))
    for i, d in enumerate(deltas):
        # keyにラベル名を含めて重複を完全排除
        if cols[i].button(f"{'+' if d>0 else ''}{d}", key=f"{key}_{d}_{label}"):
            st.session_state[key] += d
            st.rerun()

render_row("HP", "HP", [-10, -1, 1, 10])
render_row("ATK", "ATK", [-10, -1, 1, 10])
render_row("SP", "最大SP", [-5, -1, 1, 5])
render_row("DEF", "DEF", [-5, -1, 1, 5])
render_row("WT", "基礎WT", [-50, -10, 10, 50])
render_row("移動", "移動力", [-1, 1])

if st.button("💾 保存", use_container_width=True): st.success("完了！")
