import streamlit as st
import pandas as pd

# (中略: load_data()等はそのまま使用)
df_sheets = load_data()

if not df_sheets.empty:
    # (中略: 列名定義)
    
    # 🛠️ 詳細調整タブ内
    with tab_edit:
        # (中略: 既存項目)
        c1, c2 = st.columns(2)
        with c1:
            hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
            atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
            def_val = st.number_input("DEF", value=int(unit_data.get("DEF", 60)))
            # 【追加】WTと枠数
            wt = st.number_input("WT", value=int(unit_data.get("WT", 500)))
        with c2:
            sp = st.number_input("最大SP", value=int(unit_data.get("最大SP", 100)))
            mov = st.number_input("移動力", value=int(unit_data.get("移動力", 4)))
            # 【追加】エクストラスキル枠数
            ex_slots = st.number_input("エクストラスキル枠数", value=int(unit_data.get("エクストラスキル枠数", 1)))

        # 計算ロジック（WTが反映されるよう調整）
        durability = (hp * 1.0) + (def_val * 2.5)
        offensive = (atk * 2.0) + (sp * 1.5)
        # WTが低いほどスコアが高くなる計算式を維持
        total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50) 
        
        # (中略: 表示・保存ロジック)
