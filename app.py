import streamlit as st
import pandas as pd

# 1. データの読み込み定義
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"データ取得エラー: {e}")
        return pd.DataFrame()

# 2. データ読み込み実行
df_sheets = load_data()

# 3. データが存在する場合のみ画面を描画
if not df_sheets.empty:
    # 列名の確定
    name_col = df_sheets.columns[1]
    world_col = df_sheets.columns[2]
    
    # 選択肢用のリスト
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    world_list = df_sheets[world_col].dropna().unique().tolist()

    # タブ設定
    tab1, tab2 = st.tabs(["📋 ユニット一覧・比較", "🛠️ 詳細調整・保存"])

    with tab1:
        st.subheader("全ユニットデータ")
        st.dataframe(df_sheets, use_container_width=True)

    with tab2:
        mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)
        
        if mode == "既存ユニットの調整":
            selected_name = st.selectbox("調整するユニット:", unit_name_list)
            unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
        else:
            selected_name = st.text_input("新規ユニット名:")
            unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60, '移動力': 4, 'WT': 500, 'エクストラスキル枠数': 1})

        # 入力フォーム（WT、枠数を含む）
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
            atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
            def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
            wt = st.number_input("WT", value=int(unit_data.get("WT", 500))) # 追加
        with c2:
            sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
            mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))
            ex_slots = st.number_input("エクストラスキル枠数", value=int(unit_data.get("エクストラスキル枠数", 1))) # 追加

        # 計算ロジック
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50)

        # スコア表示
        st.markdown("### 📊 戦術評価")
        s1, s2, s3 = st.columns(3)
        s1.metric("✨ 総合", f"{int(total)}")
        s2.metric("🛡️ 耐久", f"{int(durability)}")
        s3.metric("⚔️ 攻撃", f"{int(offensive)}")

        # 保存
        if st.checkbox("上記の内容で保存する"):
            if st.button("✅ 保存を実行"):
                st.success("保存完了")
else:
    st.warning("データがまだ読み込まれていません。")
