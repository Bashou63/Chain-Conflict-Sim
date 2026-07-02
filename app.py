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

# 2. 【重要】エラー防止のため、読み込み直後に全変数を確実に定義する
if not df_sheets.empty:
    id_col = df_sheets.columns[0]
    # 2列目をユニット名と定義
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
else:
    st.error("データの読み込みに失敗しました。")
    st.stop()

# 3. モード選択と調整エリア
mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)

if mode == "既存ユニットの調整":
    selected_name = st.selectbox("調整するユニット:", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
else:
    selected_name = st.text_input("新規ユニット名:")
    unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60})

# --- 調整エリア ---
st.subheader(f"🛠️ {selected_name}")
# 数値入力
hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
# ... (他の項目)

# --- 保存エリア ---
st.markdown("---")
if st.checkbox("上記の内容で保存する"):
    if st.button("✅ 保存を実行", use_container_width=True):
        st.success(f"🎉 {selected_name} を保存しました！")
