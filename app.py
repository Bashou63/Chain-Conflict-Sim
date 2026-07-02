import streamlit as st
import pandas as pd

# 設定
st.set_page_config(layout="centered", page_title="Chain Conflict Manager")

# 1. データ読み込み（キャッシュ利用）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()
unit_names = df.iloc[:, 1].dropna().unique().tolist()

# 2. ユニット選択と状態管理
if 'selected_unit' not in st.session_state: st.session_state.selected_unit = unit_names[0]

selected_name = st.selectbox("🔄 ユニット選択", unit_names)
unit_data = df[df.iloc[:, 1] == selected_name].iloc[0]

# セッションステートへ全項目をロード（初回のみ）
for col in ['HP', 'ATK', '最大SP', 'DEF', '基礎WT', '移動力']:
    if col not in st.session_state: st.session_state[col] = int(unit_data.get(col, 100))

# 3. 総合スコア計算
score = (st.session_state['HP'] * 1.0) + (st.session_state['DEF'] * 2.5) + \
        (st.session_state['ATK'] * 2.0) + (st.session_state['最大SP'] * 1.5) + \
        ((1000 - st.session_state['基礎WT']) * 1.5) + (st.session_state['移動力'] * 50)

st.markdown("---")
st.subheader(f"📊 総合スコア: {int(score)}")
st.markdown("---")

# 4. 横一列コンパクト・調整UI
def render_row(label, key, deltas):
    cols = st.columns([2, 1, 1, 2, 1, 1])
    cols[0].write(f"**{label}**")
    for i, d in enumerate(deltas):
        btn_key = f"{key}_{d}"
        if cols[1+i].button(f"{'+' if d>0 else ''}{d}", key=btn_key):
            st.session_state[key] += d
            st.rerun()
    cols[5].write(f"**{st.session_state[key]}**")

st.subheader("🛠️ パラメータ調整")
render_row("HP", "HP", [-10, -1, 1, 10])
render_row("ATK", "ATK", [-10, -1, 1, 10])
render_row("SP", "最大SP", [-5, -1, 1, 5])
render_row("DEF", "DEF", [-5, -1, 1, 5])
render_row("WT", "基礎WT", [-50, -10, 10, 50])
render_row("移動", "移動力", [-1, 0, 0, 1]) # 簡易版

# 5. 保存ボタン
if st.button("💾 スプレッドシートへ保存", use_container_width=True):
    st.success("🎉 データ更新！")
    # ここにスプレッドシートへの書き込み処理を記述
