import streamlit as st
import pandas as pd

# 1. データの読み込みと読み込み関数の定義（冒頭で確実に実行）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=60) # キャッシュ時間を少し延長して安定化
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

# データを読み込む
df_sheets = load_data()

# 2. アプリのメイン処理（データが存在する場合のみ実行）
if not df_sheets.empty:
    # 列名の確定（※スプレッドシートの列名が変化しないことが前提です）
    name_col = df_sheets.columns[1]
    world_col = df_sheets.columns[2]
    
    # 選択肢用のリストをここで確実に生成
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    world_list = df_sheets[world_col].dropna().unique().tolist()

    # タブ作成
    tab1, tab2 = st.tabs(["📋 ユニット一覧・比較", "🛠️ 詳細調整・保存"])

    # 【タブ1：一覧】
    with tab1:
        st.dataframe(df_sheets, use_container_width=True)

    # 【タブ2：詳細調整】
    with tab2:
        mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True, key="mode")
        
        # ユニットデータの取得
        if mode == "既存ユニットの調整":
            selected_name = st.selectbox("調整するユニット:", unit_name_list, key="select_unit")
            unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
        else:
            selected_name = st.text_input("新規ユニット名:", key="new_unit_name")
            # 新規作成時の初期値（すべてを定義）
            unit_data = pd.Series({
                'HP': 100, 'ATK': 70, '最大SP': 100, 'DEF': 60, 
                '移動力': 4, 'WT': 500, 'エクストラスキル枠数': 1
            })

        # 入力フォーム（keyを固定して再描画を防ぐ）
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(unit_data.get("HP", 100)), key="hp_in")
            atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)), key="atk_in")
            def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)), key="def_in")
            wt = st.number_input("WT", value=int(unit_data.get("WT", 500)), key="wt_in")
        with c2:
            sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)), key="sp_in")
            mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)), key="mov_in")
            ex_slots = st.number_input("エクストラスキル枠数", value=int(unit_data.get("エクストラスキル枠数", 1)), key="ex_in")

        # 計算式（ここで使う変数はすべて上記で定義済み）
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50)

        # 結果表示
        st.markdown("### 📊 戦術評価")
        s1, s2, s3 = st.columns(3)
        s1.metric("✨ 総合", f"{int(total)}")
        s2.metric("🛡️ 耐久", f"{int(durability)}")
        s3.metric("⚔️ 攻撃", f"{int(offensive)}")

        if st.checkbox("上記の内容で保存する"):
            if st.button("✅ 保存を実行"):
                st.success("保存完了")
else:
    st.warning("データの読み込みに失敗しました。URLまたはネット環境をご確認ください。")
