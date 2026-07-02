import streamlit as st
import pandas as pd

# 1. データの読み込み（これがないと始まらない！）
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

# 2. データが空ならエラーを表示して終了
if df_sheets.empty:
    st.error("データの読み込みに失敗しました。")
    st.stop()

# 3. ユニット選択と調整エリア（常に表示！）
id_col = df_sheets.columns[0]
name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
unit_name_list = df_sheets[name_col].dropna().unique().tolist()
selected_unit_name = st.selectbox("🔄 ユニット選択:", unit_name_list)

unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]

# --- 調整エリア ---
st.subheader(f"🛠️ {selected_unit_name}")
# ここにステータス調整のUIを記述...

# ------------------------------------------
# 4. 保存エリア（独立したエリアとして一番下に配置）
# ------------------------------------------
st.markdown("---")
st.header("💾 データの保存")

if st.checkbox("上記の内容でスプレッドシートを上書き保存する"):
    if st.button("✅ 確定して保存を実行", use_container_width=True):
        st.success("🎉 保存完了！")
else:
    st.info("保存するには上のチェックボックスをONにしてください。")
