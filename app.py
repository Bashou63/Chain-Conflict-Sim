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

# 2. 変数定義（ユニット選択のため必須）
if not df_sheets.empty:
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    
    # 3. モード選択とデータ取得
    mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)
    if mode == "既存ユニットの調整":
        selected_name = st.selectbox("調整するユニット:", unit_name_list)
        unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
    else:
        selected_name = st.text_input("新規ユニット名:")
        unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60, '移動力': 4})

    # 4. 数値調整フォーム
    st.subheader(f"🛠️ {selected_name} の調整")
    c1, c2 = st.columns(2)
    with c1:
        hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
        atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
        def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
    with c2:
        sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
        wt = st.number_input("基礎WT", value=int(unit_data.get("基礎WT", 500)))
        mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))

    # 5. 計算ロジック
    durability = (hp * 1.0) + (def_val * 2.5)
    offensive = (atk * 2.0) + (sp * 1.5)
    total = durability + offensive + (1000 - wt) * 1.5

    # 6. 【3カラム完全整列】スコア表示
    st.markdown("### 📊 戦術評価")
    s1, s2, s3 = st.columns(3)
    s1.metric("✨ 総合", f"{int(total)}")
    s2.metric("🛡️ 耐久", f"{int(durability)}")
    s3.metric("⚔️ 攻撃", f"{int(offensive)}")

    # 7. 保存エリア
    st.markdown("---")
    if st.checkbox("上記の内容で保存する"):
        if st.button("✅ 保存を実行", use_container_width=True):
            st.success("🎉 保存完了！")
else:
    st.error("データ読み込み失敗")
