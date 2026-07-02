import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』HTML強制テーブルレイアウト版 (V3.9)
# ==========================================

st.set_page_config(layout="wide")

# 最強の強制CSS：テーブルの中身を無理やり横に並べる
st.markdown("""
    <style>
    .fixed-table { width: 100%; border-collapse: collapse; }
    .fixed-table td { width: 33%; padding: 2px; vertical-align: top; }
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み（省略）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
df = pd.read_csv(SHEET_URL)
df.columns = [c.strip() for c in df.columns]
unit_data = df.iloc[0]

# HTMLテーブルで入力項目を「3列」に固定する
st.subheader("🛠️ パラメーター調整")
html_table = f"""
<table class="fixed-table">
    <tr>
        <td>HP<br><input type="number" value="{unit_data.get('HP', 100)}"></td>
        <td>ATK<br><input type="number" value="{unit_data.get('ATK', 70)}"></td>
        <td>SP<br><input type="number" value="{unit_data.get('最大SP', 100)}"></td>
    </tr>
    <tr>
        <td>DEF<br><input type="number" value="{unit_data.get('DEF', 60)}"></td>
        <td>WT<br><input type="number" value="{unit_data.get('基礎WT', 500)}"></td>
        <td>移動<br><input type="number" value="{unit_data.get('移動力', 4)}"></td>
    </tr>
</table>
"""
st.markdown(html_table, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 総合スコア")
st.markdown("<h1 style='text-align: center; color: #00FF66;'>1590</h1>", unsafe_allow_html=True)
