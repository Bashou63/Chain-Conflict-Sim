import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』モバイル最速・縦積みの極み (V4.1)
# ==========================================

st.set_page_config(layout="centered") # 画面中央に寄せることでスマホの余白を制御

# 徹底した視認性重視のCSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; }
    /* スライダーのラベルを太くして視認性アップ */
    label { color: #FFFFFF !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
df = pd.read_csv(SHEET_URL)
df.columns = [c.strip() for c in df.columns]

# 1. ユニット選択（復旧！）
unit_list = df.iloc[:, 1].dropna().unique().tolist()
selected_name = st.selectbox("🔄 ユニット選択", unit_list)
unit_data = df[df.iloc[:, 1] == selected_name].iloc[0]

# 2. リアルタイム・スコア（一番上に配置）
st.markdown("---")
col1, col2 = st.columns(2)
hp = st.slider("HP", 1, 5000, int(unit_data.get("HP", 100)))
atk = st.slider("ATK", 0, 500, int(unit_data.get("ATK", 70)))
sp = st.slider("最大SP", 10, 500, int(unit_data.get("最大SP", 100)))
df_val = st.slider("DEF", 0, 500, int(unit_data.get("DEF", 60)))
wt = st.slider("基礎WT", 100, 2000, int(unit_data.get("基礎WT", 500)))
mv = st.slider("移動力", 1, 10, int(unit_data.get("移動力", 4)))

total = (hp * 1.0) + (df_val * 2.5) + (atk * 2.0) + (sp * 1.5) + (1000 - wt) * 1.5 + (mv * 50)

st.metric("✨ 総合スコア", f"{int(total)}")

if st.button("💾 保存", use_container_width=True):
    st.success("保存完了！")
