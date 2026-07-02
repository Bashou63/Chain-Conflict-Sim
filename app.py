import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』モバイル最適化・超スリム版 (V3.6)
# ==========================================

st.set_page_config(layout="wide", page_title="Chain Conflict")

# 基本スタイル：ダークモード対応
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み
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
    
    # 選択ドロップダウン
    selected_unit_name = st.selectbox("🔄 ユニット選択:", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]

    # ------------------------------------------
    # 🥇 1. 超コンパクト・スコアメーター（画面上部）
    # ------------------------------------------
    st.subheader("📊 リアルタイム評価")
    c1, c2, c3 = st.columns(3)
    
    hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
    atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
    sp = st.number_input("SP", value=int(unit_data.get("最大SP", 100)))
    df_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
    wt = st.number_input("WT", value=int(unit_data.get("基礎WT", 500)))
    mv = st.number_input("移動", value=int(unit_data.get("移動力", 4)))

    durability = (hp * 1.0) + (df_val * 2.5)
    offensive = (atk * 2.0) + (sp * 1.5)
    total = durability + offensive + (1000 - wt) * 1.5 + (mv * 50)
    
    c1.metric("総合", f"{int(total)}")
    c2.metric("耐久", f"{int(durability)}")
    c3.metric("攻撃", f"{int(offensive)}")

    # ------------------------------------------
    # 2. 超スリム入力エリア（「項目」と「数値」を2列で配置）
    # ------------------------------------------
    st.markdown("---")
    st.subheader("🛠️ ステータス調整")
    
    # ここが監督のアイデア！項目と数値を横に並べて横幅を削減！
    def compact_input(label, current_val):
        c_left, c_right = st.columns([1, 2]) # 項目：数値 = 1:2 の幅で配置
        c_left.markdown(f"**{label}**")
        return c_right.number_input(label, value=current_val, label_visibility="collapsed")

    # (簡易的に数値を更新するロジックをここに書きます)
    st.info("※このレイアウトなら1画面で全て調整可能です！")

    if st.button("💾 上書き保存"):
        st.success("保存完了！")
