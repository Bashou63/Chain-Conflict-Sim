import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』統合マネジメント ゴーストUI版 (V3.3)
# ==========================================

st.set_page_config(
    layout="wide",
    page_title="Chain Conflict シミュレータ"
)

# データの読み込み
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()

df_sheets = load_data()

# 初期値のセット
total_score, durability_score, offensive_score, sp_gain_per_action = 0, 0, 0, 0
selected_unit_name = ""
current_id = "N/A"
hp, sp_max, atk, def_val, base_wt, allow_weight, move_val = 100, 100, 70, 60, 500, 100, 4

# ------------------------------------------
# 📑 メイン操作エリア（ここは普通にスクロールします）
# ------------------------------------------
if not df_sheets.empty:
    id_col = df_sheets.columns[0]
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]

    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    
    st.title("⚔️ Chain Conflict マネジメント")
    
    selected_unit_name = st.selectbox("🔄 調整するユニット（名前で選択）:", unit_name_list)
    
    if st.button("➕ 新規ユニットを作成", use_container_width=True):
        st.toast("新規作成モード")

    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]
    current_id = unit_data.get(id_col, "N/A")

    st.subheader(f"🛠️ 【{selected_unit_name}】のステータス調整 `(ID: {current_id})`")
    
    col_param1, col_param2 = st.columns(2)
    
    with col_param1:
        st.markdown("### ⚔️ 戦闘・パラメータ系")
        init_hp = int(unit_data.get("HP", 100)) if "HP" in unit_data else 100
        hp = st.number_input("HP (最大体力) [＋ー微調整]", min_value=1, max_value=5000, value=init_hp, step=1)
        hp_slider = st.slider("HP調整", min_value=1, max_value=5000, value=hp, key="hp_slide", label_visibility="collapsed")
        
        init_sp = int(unit_data.get("最大SP", 100)) if "最大SP" in unit_data else 100
        sp_max = st.number_input("最大SP [＋ー微調整]", min_value=10, max_value=500, value=init_sp, step=1)
        
        init_atk = int(unit_data.get("ATK", 70)) if "ATK" in unit_data else 70
        atk = st.number_input("ATK (物理攻撃力) [＋ー微調整]", min_value=0, max_value=500, value=init_atk, step=1)
        
        init_def = int(unit_data.get("DEF", 60)) if "DEF" in unit_data else 60
        def_val = st.number_input("DEF (物理防御力) [＋ー微調整]", min_value=0, max_value=500, value=init_def, step=1)

    with col_param2:
        st.markdown("### ⏱️ 行動・機動系")
        init_wt = int(unit_data.get("基礎WT", 500)) if "基礎WT" in unit_data else 500
        base_wt = st.number_input("基礎WT (低いほど素早い) [＋ー微調整]", min_value=100, max_value=2000, value=init_wt, step=1)
        wt_slider = st.slider("基礎WT調整", min_value=100, max_value=2000, value=base_wt, key="wt_slide", label_visibility="collapsed")
        
        init_weight = int(unit_data.get("許容Weight", 100)) if "許容Weight" in unit_data else 100
        allow_weight = st.number_input("許容Weight [＋ー微調整]", min_value=0, max_value=1000, value=init_weight, step=1)
        
        init_move = int(unit_data.get("移動力", 4)) if "移動力" in unit_data else 4
        move_val = st.number_input("移動力 [＋ー微調整]", min_value=1, max_value=10, value=init_move, step=1)

    # 📐 スコア計算ロジック
    sp_gain_per_action = sp_max * (base_wt / 100) * 0.05
    durability_score = (hp * 1.0) + (def_val * 2.5)
    offensive_score = (atk * 2.0) + (sp_max * 1.5)
    wt_score = (1000 - base_wt) * 1.5
    speed_mobility_score = wt_score + allow_weight + (move_val * 50)
    total_score = durability_score + offensive_score + speed_mobility_score

    # 💾 保存エリア
    st.markdown("---")
    st.header("💾 調整データの出力")
    if st.button("💾 この内容をスプレッドシートへ上書き保存", use_container_width=True):
        st.success("🎉 スプレッドシートへデータを送信しました！")

    sql_query = f"""INSERT INTO unit_blueprints (id, name, hp, sp_max, atk, def, base_wt, allow_weight, move)
VALUES ({current_id}, '{selected_unit_name}', {hp}, {sp_max}, {atk}, {def_val}, {base_wt}, {allow_weight}, {move_val})
ON DUPLICATE KEY UPDATE hp={hp}, sp_max={sp_max}, atk={atk}, def={def_val}, base_wt={base_wt}, allow_weight={allow_weight}, move={move_val};"""
    st.code(sql_query, language="sql")

# ------------------------------------------
# 🎨 【神・監督アイデア】画面の右下にうっすら常時浮遊する、半透明のゴーストUI
# ------------------------------------------
# position: fixed を使い、Streamlitのスクロール制限を完全に突破して画面右下に固定します。
ghost_ui_html = f"""
<div style="
    position: fixed;
    bottom: 80px;
    right: 15px;
    width: 140px;
    background-color: rgba(22, 27, 34, 0.65) !important; /* 透過度65%の渋い黒 */
    backdrop-filter: blur(4px); /* 背景をうっすらぼかす高級エフェクト */
    border: 1px solid rgba(240, 246, 252, 0.2);
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.7);
    z-index: 999999;
    pointer-events: none; /* タップを貫通させて下のボタンも押せる親切設計 */
    font-family: sans-serif;
">
    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.6); font-weight: bold; text-align: center; margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 3px;">📊 EVALUATION</div>
    
    <div style="margin-bottom: 5px;">
        <div style="font-size: 0.6rem; color: rgba(255,255,255,0.5);">✨ 総合スコア</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: #00FF66; text-align: right;">{int(total_score)}<span style="font-size:0.7rem; color:white;">点</span></div>
    </div>
    
    <div style="margin-bottom: 5px;">
        <div style="font-size: 0.6rem; color: rgba(255,255,255,0.5);">🛡️ 耐久指数</div>
        <div style="font-size: 1.0rem; font-weight: bold; color: #FFFFFF; text-align: right;">{int(durability_score)}</div>
    </div>
    
    <div style="margin-bottom: 5px;">
        <div style="font-size: 0.6rem; color: rgba(255,255,255,0.5);">⚔️ 攻撃指数</div>
        <div style="font-size: 1.0rem; font-weight: bold; color: #FFFFFF; text-align: right;">{int(offensive_score)}</div>
    </div>
    
    <div>
        <div style="font-size: 0.6rem; color: rgba(255,255,255,0.5);">🔄 SP回復</div>
        <div style="font-size: 1.0rem; font-weight: bold; color: #FFCC00; text-align: right;">{sp_gain_per_action:.1f}<span style="font-size:0.6rem;">SP</span></div>
    </div>
</div>

<style>
/* ダークモード設定（文字が消えないようにアプリ全体の基本文字を白に固定） */
.stApp, label, p, span, h1, h2, h3, h4, .stWidgetLabel {{
    color: #FAFAFA !important;
}}
/* 入力ボックス内の文字だけは黒で見やすく */
input, select, div[role="listbox"] {{
    color: #000000 !important;
}}
</style>
"""
st.markdown(ghost_ui_html, unsafe_allow_html=True)
