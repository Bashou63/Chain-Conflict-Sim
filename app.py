import streamlit as st
import pandas as pd

# (中略: 読み込み処理は以前のまま)

# 1. ユニット名リストを取得
unit_name_list = df_sheets[name_col].dropna().unique().tolist()

# 2. モード選択（ここで切り替える！）
mode = st.radio("戦術モード選択:", ["既存ユニットの調整", "新規ユニット作成"], horizontal=True)

if mode == "既存ユニットの調整":
    selected_name = st.selectbox("調整するユニット:", unit_name_list)
    unit_data = df_sheets[df_sheets[name_col] == selected_name].iloc[0]
else:
    # 新規作成時は空のデータをセット
    selected_name = st.text_input("新規ユニット名を入力:")
    unit_data = pd.Series({'HP': 100, 'ATK': 70, '最大SP': 100, '基礎WT': 500, 'DEF': 60, '許容Weight': 100, '移動力': 4})

# 3. 調整エリア（共通ロジック）
st.subheader(f"🛠️ 【{selected_name}】の設定")
hp = st.number_input("HP", value=int(unit_data.get("HP", 100)))
atk = st.number_input("ATK", value=int(unit_data.get("ATK", 70)))
# ... (他の項目も同様) ...

# 4. 保存ロジック（ここでもモードを判別）
if st.checkbox("上記の内容で保存する"):
    if st.button("✅ 保存を実行"):
        if mode == "新規ユニット作成":
            st.write(f"🎉 {selected_name} を新規作成しました！")
        else:
            st.write(f"🎉 {selected_name} を更新しました！")
