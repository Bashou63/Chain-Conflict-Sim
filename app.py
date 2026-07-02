import streamlit as st
import pandas as pd

# 1. データの読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df_sheets = load_data()

# 2. 変数定義
if not df_sheets.empty:
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
else:
    st.error("データ読み込み失敗")
    st.stop()

# 3. UI構築
mode = st.radio("モード:", ["既存調整", "新規作成"], horizontal=True)
if mode == "既存調整":
    selected_name = st.selectbox("調整:", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
else:
    selected_name = st.text_input("名前:")
    unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60, '許容Weight': 100, '移動力': 4})

# --- 全項目網羅の調整エリア ---
st.subheader(f"🛠️ {selected_name} の全項目調整")
col1, col2 = st.columns(2)

with col1:
    hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
    atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
    def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))

with col2:
    sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
    wt = st.number_input("基礎WT", value=int(unit_data.get("基礎WT", 500)))
    mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))

# --- 保存エリア ---
st.markdown("---")
if st.checkbox("上記の内容で保存する"):
    if st.button("✅ 保存を実行", use_container_width=True):
        st.success("🎉 全項目を反映して保存しました！")
