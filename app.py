import streamlit as st
import pandas as pd

# (データ読み込み処理は省略せず、そのままお使いください)
# ... (load_data 関数) ...

df_sheets = load_data()

if not df_sheets.empty:
    name_col = df_sheets.columns[1]
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()

    tab1, tab2 = st.tabs(["📋 ユニット一覧・比較", "🛠️ 詳細調整・保存"])

    with tab1:
        st.dataframe(df_sheets, use_container_width=True)

    with tab2:
        mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)
        
        if mode == "既存ユニットの調整":
            selected_name = st.selectbox("調整するユニット:", unit_name_list)
            unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
        else:
            selected_name = st.text_input("新規ユニット名:")
            unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, 'WT': 500, 'DEF': 60, '移動力': 4, 'エクストラスキル枠数': 1})

        # 【超重要：key引数でユニット名を指定し、切り替え時に再描画させる】
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(unit_data.get("HP", 100)), key=f"hp_{selected_name}")
            atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)), key=f"atk_{selected_name}")
            def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)), key=f"def_{selected_name}")
            wt = st.number_input("WT", value=int(unit_data.get("WT", 500)), key=f"wt_{selected_name}")
        with c2:
            sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)), key=f"sp_{selected_name}")
            mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)), key=f"mov_{selected_name}")
            ex_slots = st.number_input("エクストラスキル枠数", value=int(unit_data.get("エクストラスキル枠数", 1)), key=f"ex_{selected_name}")

        # 計算式
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50)

        # スコア表示
        s1, s2, s3 = st.columns(3)
        s1.metric("✨ 総合", f"{int(total)}")
        s2.metric("🛡️ 耐久", f"{int(durability)}")
        s3.metric("⚔️ 攻撃", f"{int(offensive)}")
else:
    st.warning("データがまだ読み込まれていません。")
