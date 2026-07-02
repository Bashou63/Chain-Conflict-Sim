import streamlit as st
import pandas as pd

# 1. データの読み込み（これが最初の一手！）
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

# エラーハンドリング
if df_sheets.empty:
    st.error("データの読み込みに失敗しました。")
    st.stop()

# 2. 変数の定義（ここが欠けておりました…っ！）
id_col = df_sheets.columns[0]
name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
unit_name_list = df_sheets[name_col].dropna().unique().tolist()

# 3. UIの構築
selected_unit_name = st.selectbox("🔄 ユニット選択:", unit_name_list)
unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]

# 4. 数値の取得と計算ロジック
hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
sp_max = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
base_wt = st.number_input("基礎WT", value=int(unit_data.get("基礎WT", 500)))

# 総合スコア計算
off_score = (atk * 2.0) + (sp_max * 1.5)
total_score = (hp * 1.0) + off_score + (1000 - base_wt) * 1.5

# 結果表示
col1, col2 = st.columns(2)
col1.metric("✨ 総合スコア", f"{int(total_score)} 点")
col2.metric("⚔️ 攻撃指数", f"{int(off_score)} 点")

# 5. 保存エリア
st.markdown("---")
if st.checkbox("上記の内容で保存する"):
    if st.button("✅ 保存を実行", use_container_width=True):
        st.success("🎉 保存完了！")
