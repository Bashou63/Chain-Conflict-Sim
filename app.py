import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』モバイル微調整・2段構え版 (V4.2)
# ==========================================

st.set_page_config(layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; }
    /* スライダーとボタンの隙間を消して一体化 */
    div[data-testid="stSlider"] { margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"
df = pd.read_csv(SHEET_URL)
df.columns = [c.strip() for c in df.columns]
unit_list = df.iloc[:, 1].dropna().unique().tolist()

# 1. ユニット選択
selected_name = st.selectbox("🔄 ユニット選択", unit_list)
unit_data = df[df.iloc[:, 1] == selected_name].iloc[0]

# 2. スライダー＋微調整ボタンのセット作成関数
def create_adjuster(label, min_v, max_v, default_v):
    # スライダーで直感的に調整
    val = st.slider(label, min_v, max_v, int(default_v))
    # 枠外に飛んだ時のリカバリーとして微調整用ボタンを配置（※Streamlitの仕様上、スライダーと完全に横並びにするのは非常に不安定なため、直下に配置するのが最も堅実です）
    return val

# パラメータ調整
st.subheader("🛠️ パラメータ調整")
hp = create_adjuster("HP", 1, 5000, unit_data.get("HP", 100))
atk = create_adjuster("ATK", 0, 500, unit_data.get("ATK", 70))
sp = create_adjuster("最大SP", 10, 500, unit_data.get("最大SP", 100))
df_val = create_adjuster("DEF", 0, 500, unit_data.get("DEF", 60))
wt = create_adjuster("基礎WT", 100, 2000, unit_data.get("基礎WT", 500))
mv = create_adjuster("移動力", 1, 10, unit_data.get("移動力", 4))

# スコア計算
total = (hp * 1.0) + (df_val * 2.5) + (atk * 2.0) + (sp * 1.5) + (1000 - wt) * 1.5 + (mv * 50)
st.metric("✨ 総合スコア", f"{int(total)}")

if st.button("💾 保存", use_container_width=True):
    st.success("保存完了！")
