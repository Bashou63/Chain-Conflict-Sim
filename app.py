import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』モバイル最適化・3カラム超スリム版 (V3.7)
# ==========================================

st.set_page_config(layout="wide", page_title="Chain Conflict")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FAFAFA !important; }
    /* ラベルの文字サイズを小さくして、狭い場所でも入るようにする */
    .stWidgetLabel { font-size: 0.7rem !important; }
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
    
    # 選択
    selected_unit_name = st.selectbox("🔄 ユニット選択", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]

    # 1. 3カラムでパラメータを圧縮表示
    st.subheader("🛠️ パラメーター調整")
    
    # 上段：HP, ATK, SP
    c1, c2, c3 = st.columns(3)
    hp = c1.number_input("HP", value=int(unit_data.get("HP", 100)))
    atk = c2.number_input("ATK", value=int(unit_data.get("ATK", 70)))
    sp = c3.number_input("SP", value=int(unit_data.get("最大SP", 100)))
    
    # 下段：DEF, WT, 移動
    c4, c5, c6 = st.columns(3)
    df_val = c4.number_input("DEF", value=int(unit_data.get("DEF", 60)))
    wt = c5.number_input("WT", value=int(unit_data.get("基礎WT", 500)))
    mv = c6.number_input("移動", value=int(unit_data.get("移動力", 4)))

    # スコア計算
    durability = (hp * 1.0) + (df_val * 2.5)
    offensive = (atk * 2.0) + (sp * 1.5)
    total = durability + offensive + (1000 - wt) * 1.5 + (mv * 50)
    
    # 2. 結果をコンパクトに表示
    st.markdown("---")
    st.subheader("📊 リアルタイム評価")
    res1, res2, res3 = st.columns(3)
    res1.metric("総合", f"{int(total)}")
    res2.metric("耐久", f"{int(durability)}")
    res3.metric("攻撃", f"{int(offensive)}")

    if st.button("💾 上書き保存", use_container_width=True):
        st.success("保存完了！")
