import streamlit as st
import pandas as pd

# (データ読み込み処理は省略せず、ここが起点となります)
# ... (load_data()関数は以前のまま) ...

df_sheets = load_data()
if not df_sheets.empty:
    # 列名の確定（重要！）
    name_col = df_sheets.columns[1]
    world_col = df_sheets.columns[2] # 3列目を世界とする
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    world_list = df_sheets[world_col].dropna().unique().tolist()

    # --- 1. タブで画面を分ける ---
    tab_list, tab_edit = st.tabs(["📋 ユニット一覧・比較", "🛠️ 詳細調整・保存"])

    with tab_list:
        st.subheader("全ユニットデータ")
        st.dataframe(df_sheets, use_container_width=True)

    with tab_edit:
        # ユニット調整エリア（所属世界選択付き）
        mode = st.radio("戦術モード:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)
        
        if mode == "既存ユニットの調整":
            selected_name = st.selectbox("調整するユニット:", unit_name_list)
            unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
            current_world = unit_data[world_col]
        else:
            selected_name = st.text_input("新規ユニット名:")
            current_world = st.selectbox("所属世界:", world_list)
            unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60, '移動力': 4})

        # 全数値調整
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
            atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
            def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
        with c2:
            sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
            wt = st.number_input("基礎WT", value=int(unit_data.get("基礎WT", 500)))
            mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))

        # 計算式と表示（ここも忘れず配置！）
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        total = durability + offensive + (1000 - wt) * 1.5
        
        st.markdown("### 📊 戦術評価")
        s1, s2, s3 = st.columns(3)
        s1.metric("✨ 総合", f"{int(total)}")
        s2.metric("🛡️ 耐久", f"{int(durability)}")
        s3.metric("⚔️ 攻撃", f"{int(offensive)}")
        
        # 保存ロジック
        if st.checkbox("上記の内容で保存する"):
            if st.button("✅ 保存を実行"):
                st.success("🎉 完了！")
else:
    st.error("データ読み込み失敗")
