import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』モバイル強制横並び・最終版 (V3.8)
# ==========================================

st.set_page_config(layout="wide", page_title="Chain Conflict")

# スマホの縦画面でも「絶対に3つ横並び」を維持するCSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    /* 入力コンテナを強制的に横並びにするクラス */
    .flex-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }
    .flex-item {
        flex: 1 1 30%; /* 30%の幅を維持させて3つ並べる */
        min-width: 80px;
    }
    .stNumberInput label { font-size: 0.6rem !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み（省略）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

df_sheets = load_data()

if not df_sheets.empty:
    id_col = df_sheets.columns[0]
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    
    selected_unit_name = st.selectbox("🔄 ユニット選択", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]

    # スコア計算
    hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
    atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
    sp = st.number_input("SP", value=int(unit_data.get("最大SP", 100)))
    df_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
    wt = st.number_input("WT", value=int(unit_data.get("基礎WT", 500)))
    mv = st.number_input("移動", value=int(unit_data.get("移動力", 4)))

    durability = (hp * 1.0) + (df_val * 2.5)
    offensive = (atk * 2.0) + (sp * 1.5)
    total = durability + offensive + (1000 - wt) * 1.5 + (mv * 50)
    
    # リアルタイム表示を一番上に持ってきて、その後に入力項目を配置する構成
    st.markdown("---")
    st.subheader("📊 総合スコア")
    st.markdown(f"<h1 style='text-align: center; color: #00FF66;'>{int(total)}</h1>", unsafe_allow_html=True)
    
    # 入力項目を無理やり横に並べるためのHTML構造
    st.markdown('<div class="flex-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="flex-item">HP:{hp}</div><div class="flex-item">ATK:{atk}</div><div class="flex-item">SP:{sp}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
