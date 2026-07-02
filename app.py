import streamlit as st
import pandas as pd

# データ読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df_sheets = load_data()

if not df_sheets.empty:
    name_col = df_sheets.columns[1]
    
    tab1, tab2 = st.tabs(["📋 ユニット一覧・比較", "🛠️ 詳細調整・保存"])

    with tab1:
        st.dataframe(df_sheets, use_container_width=True)

    with tab2:
        # 1. ユニット選択を『先に』行う
        mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True, key="mode")
        
        if mode == "既存ユニットの調整":
            selected_name = st.selectbox("調整するユニット:", df_sheets[name_col].unique(), key="unit_select")
            unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
        else:
            selected_name = st.text_input("新規ユニット名:", key="new_unit_name")
            unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, 'DEF': 60, '移動力': 4, 'WT': 500, 'エクストラスキル枠数': 1})

        # 2. 【重要】ユニットデータに基づいて『セッション状態』を更新
        # これにより、ユニット変更時に数値が強制的に書き換わります
        def get_val(key, default):
            return unit_data.get(key, default)

        # 3. 入力フォーム（keyを『ユニット名』に紐付けることで、ユニットごとに別物として扱います）
        # これでユニット切り替え時に必ず新しい値が読み込まれます
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(get_val("HP", 100)), key=f"{selected_name}_hp")
            atk = st.number_input("ATK", value=int(get_val("ATK", 70)), key=f"{selected_name}_atk")
            def_val = st.number_input("DEF", value=int(get_val("DEF", 60)), key=f"{selected_name}_def")
            wt = st.number_input("WT", value=int(get_val("WT", 500)), key=f"{selected_name}_wt")
        with c2:
            sp = st.number_input("最大SP", value=int(get_val("最大SP", 100)), key=f"{selected_name}_sp")
            mov = st.number_input("移動力", value=int(get_val("移動力", 4)), key=f"{selected_name}_mov")
            ex_slots = st.number_input("エクストラスキル枠数", value=int(get_val("エクストラスキル枠数", 1)), key=f"{selected_name}_ex")

        # 計算ロジック
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50)

        # 結果表示
        st.markdown("### 📊 戦術評価")
        s1, s2, s3 = st.columns(3)
        s1.metric("✨ 総合", f"{int(total)}")
        s2.metric("🛡️ 耐久", f"{int(durability)}")
        s3.metric("⚔️ 攻撃", f"{int(offensive)}")
else:
    st.warning("データの読み込みに失敗しました。")
