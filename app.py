import streamlit as st
import pandas as pd

# データの読み込み
@st.cache_data(ttl=60)
def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    df.columns = [c.strip() for c in df.columns]
    name_col = df.columns[1]
    
    # タブ設定
    tab1, tab2 = st.tabs(["📋 ユニット一覧", "🛠️ 調整"])

    with tab1:
        st.dataframe(df, use_container_width=True)

    with tab2:
        selected_name = st.selectbox("調整するユニット:", df[name_col].unique())
        unit_row = df[df[name_col] == selected_name].iloc[0]

        # フォーム内で完結させる（値を同期させるため）
        with st.form("adjustment_form"):
            st.subheader(f"🛠️ {selected_name} の調整")
            
            # 入力項目（既存データを初期値に設定）
            c1, c2 = st.columns(2)
            with c1:
                hp = st.number_input("HP", value=int(unit_row.get("HP", 100)))
                atk = st.number_input("ATK", value=int(unit_row.get("ATK", 70)))
                def_val = st.number_input("DEF", value=int(unit_row.get("DEF", 60)))
                wt = st.number_input("WT", value=int(unit_row.get("WT", 500)))
            with c2:
                sp = st.number_input("最大SP", value=int(unit_row.get("最大SP", 100)))
                mov = st.number_input("移動力", value=int(unit_row.get("移動力", 4)))
                ex_slots = st.number_input("枠数", value=int(unit_row.get("エクストラスキル枠数", 1)))

            # 計算ロジックをボタン押し下げの直後に配置
            submit = st.form_submit_button("✅ 計算・更新")
            
            if submit:
                durability = (hp * 1.0) + (def_val * 2.5)
                offensive = (atk * 2.0) + (sp * 1.5)
                total = durability + offensive + (1000 - wt) * 1.5 + (ex_slots * 50)
                
                # 結果をフォーム内に表示
                s1, s2, s3 = st.columns(3)
                s1.metric("✨ 総合", f"{int(total)}")
                s2.metric("🛡️ 耐久", f"{int(durability)}")
                s3.metric("⚔️ 攻撃", f"{int(offensive)}")
                st.success("最新のデータで計算完了！")
else:
    st.warning("データが読み込めません。")
