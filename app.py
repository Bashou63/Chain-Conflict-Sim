import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』最終兵器・メイン最上部固定版 (V3.5)
# ==========================================

st.set_page_config(layout="wide", page_title="Chain Conflict シミュレータ")

# 漆黒のテーマ（ダークモード）
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
    
    # ユニット選択（上のスコアが見えるよう、まずは選択させる）
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    selected_unit_name = st.selectbox("🔄 調整するユニットを選択:", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]
    
    # パラメータ入力（ここの数値を動かすとすぐ下のロジックが動く）
    col1, col2 = st.columns(2)
    with col1:
        hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
        atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
        sp_max = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
    with col2:
        def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
        base_wt = st.number_input("基礎WT", value=int(unit_data.get("基礎WT", 500)))
        move_val = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))

    # スコア計算
    durability = (hp * 1.0) + (def_val * 2.5)
    offensive = (atk * 2.0) + (sp_max * 1.5)
    total = durability + offensive + (1000 - base_wt) * 1.5 + (move_val * 50)

    # ------------------------------------------
    # 🥇 【最重要】スコア表示をプログラムの「最初」に配置！
    # ------------------------------------------
    # 画面のトップに常にこれを置くことで、スマホでも視認性を維持します
    st.markdown("---")
    top_container = st.container()
    with top_container:
        st.subheader("📊 リアルタイム評価")
        c1, c2, c3 = st.columns(3)
        c1.metric("総合", f"{int(total)}")
        c2.metric("耐久", f"{int(durability)}")
        c3.metric("攻撃", f"{int(offensive)}")
    st.markdown("---")
    
    if st.button("💾 上書き保存"):
        st.success("更新完了！")
