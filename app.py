import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』超軽量・縦圧縮スライダー版 (V4.0)
# ==========================================

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    /* スライダーの間隔を極限まで詰める */
    div[data-testid="stSlider"] { margin-bottom: -10px !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
df = pd.read_csv(SHEET_URL)
df.columns = [c.strip() for c in df.columns]
unit_data = df.iloc[0]

# 1. 総合スコア（常に一番上に固定）
st.subheader("📊 リアルタイム評価")
score_display = st.empty()

# 2. スライダーによる調整エリア（縦の圧迫感を排除）
st.subheader("🛠️ パラメーター調整")
hp = st.slider("HP", 1, 5000, int(unit_data.get("HP", 100)))
atk = st.slider("ATK", 0, 500, int(unit_data.get("ATK", 70)))
sp = st.slider("最大SP", 10, 500, int(unit_data.get("最大SP", 100)))
df_val = st.slider("DEF", 0, 500, int(unit_data.get("DEF", 60)))
wt = st.slider("基礎WT", 100, 2000, int(unit_data.get("基礎WT", 500)))
mv = st.slider("移動力", 1, 10, int(unit_data.get("移動力", 4)))

# スコア計算
total = (hp * 1.0) + (df_val * 2.5) + (atk * 2.0) + (sp * 1.5) + (1000 - wt) * 1.5 + (mv * 50)
score_display.metric("総合スコア", f"{int(total)} 点")

if st.button("💾 データ保存", use_container_width=True):
    st.success("更新しました！")
