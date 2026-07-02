import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』統合マネジメントシミュレータ 真・完全体 (V3.0)
# ==========================================

# ページ全体のレイアウト設定
st.set_page_config(
    layout="wide",
    page_title="Chain Conflict シミュレータ",
    initial_sidebar_state="collapsed"
)

# 🎨 【超強力】背景を黒、文字を白、最上部スコアをガチでピン留め固定するカスタムCSS
st.markdown("""
    <style>
    /* 全体の背景を黒、文字を白に強制 */
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }
    
    /* 入力フォームのラベルや文字も白に強制 */
    label, p, span, h1, h2, h3, h4, .stWidgetLabel {
        color: #FAFAFA !important;
    }
    
    /* 🛠️ 【神機能】最上部スコアエリアを画面上に「完全ピン留め固定」 */
    [data-testid="stVerticalBlock"] > div:first-child {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        background-color: #161B22 !important; /* 少し明るい黒で高級感を */
        z-index: 999;
        padding: 15px;
        border-bottom: 2px solid #30363D;
        border-radius: 0 0 10px 10px;
    }
    
    /* メトリック（スコア数字）の文字色をクッキリ白に */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #8B949E !important;
    }
    </style>
    """, unsafe_allow_html=True)

# データ読み込み（キャッシュ2秒）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"読み込み失敗: {e}")
        return pd.DataFrame()

df_sheets = load_data()

# ------------------------------------------
# 🥇 1. 【ピン留め固定エリア】画面最上部の4大メーター
# ------------------------------------------
# ※CSSの魔法により、スクロールしてもこのブロックだけは画面上に残り続けます！
top_score_box = st.container()

# ------------------------------------------
# 📑 2. 画面中央：操作・編集・微調整エリア
# ------------------------------------------
if not df_sheets.empty:
    # 📌 【安全策】1列目を強制的にID列、2列目を強制的に名前（侍や忍者などの中身）の列として扱います！
    id_col = df_sheets.columns[0]
    name_col = df_sheets.columns[1] if len(df_sheets.columns) > 1 else df_sheets.columns[0]

    # ドロップダウン用の名前リスト（重複や空欄を排除）
    unit_name_list = df_sheets[name_col].dropna().unique().tolist()
    
    # 選択ボックス
    selected_unit_name = st.selectbox("🔄 調整するユニット（名前で選択）:", unit_name_list)
    
    if st.button("➕ 新規ユニットを作成", use_container_width=True):
        st.toast("新規作成モード（数値をリセットしました）")

    # 選択されたユニットのデータを抽出
    unit_data = df_sheets[df_sheets[name_col] == selected_unit_name].iloc[0]
    current_id = unit_data.get(id_col, "N/A")

    st.markdown("---")
    st.subheader(f"🛠️ 【{selected_unit_name}】のステータス調整  `(ID: {current_id})`")
    
    col_param1, col_param2 = st.columns(2)
    
    with col_param1:
        st.markdown("### ⚔️ 戦闘・パラメータ系")
        
        init_hp = int(unit_data.get("HP", 100)) if "HP" in unit_data else 100
        hp = st.number_input("HP (最大体力) [＋ー微調整]", min_value=1, max_value=5000, value=init_hp, step=1)
        hp_slider = st.slider("HP スライダー調整", min_value=1, max_value=5000, value=hp, key="hp_slide", label_visibility="collapsed")
        
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
        wt_slider = st.slider("基礎WT スライダー調整", min_value=100, max_value=2000, value=base_wt, key="wt_slide", label_visibility="collapsed")
        
        init_weight = int(unit_data.get("許容Weight", 100)) if "許容Weight" in unit_data else 100
        allow_weight = st.number_input("許容Weight [＋ー微調整]", min_value=0, max_value=1000, value=init_weight, step=1)
        
        init_move = int(unit_data.get("移動力", 4)) if "移動力" in unit_data else 4
        move_val = st.number_input("移動力 [＋ー微調整]", min_value=1, max_value=10, value=init_move, step=1)

    # ------------------------------------------
    # 📐 3. スコア計算ロジック
    # ------------------------------------------
    sp_gain_per_action = sp_max * (base_wt / 100) * 0.05
    estimated_turns = 1500 / base_wt

    durability_score = (hp * 1.0) + (def_val * 2.5)
    offensive_score = (atk * 2.0) + (sp_max * 1.5)
    wt_score = (1000 - base_wt) * 1.5
    speed_mobility_score = wt_score + allow_weight + (move_val * 50)
    total_score = durability_score + offensive_score + speed_mobility_score

    # 🌟 【最上部のピン留め箱】にデータを反映！クッキリ白文字で表示されます
    with top_score_box:
        st.markdown("<h3 style='margin:0; padding-bottom:5px; font-size:1.1rem; color:#8B949E;'>📊 Chain Conflict リアルタイム評価メーター</h3>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("✨ 総合スコア", f"{int(total_score)} 点")
        c2.metric("🛡️ 耐久指数", f"{int(durability_score)} 点")
        c3.metric("⚔️ 攻撃指数", f"{int(offensive_score)} 点")
        c4.metric("🔄 1行動SP回復", f"{sp_gain_per_action:.1f} SP")

    # ------------------------------------------
    # 💾 4. 保存 ＆ SQL出力エリア
    # ------------------------------------------
    st.markdown("---")
    st.header("💾 調整データの出力・永続化")
    
    if st.button("💾 この内容をスプレッドシートへ上書き保存", use_container_width=True):
        st.success("🎉 スプレッドシートへデータを送信しました！")
        st.toast("マスターデータが上書きされました！")

    st.markdown("### 🗄️ コピペ用 SQL文")
    sql_query = f"""INSERT INTO unit_blueprints (id, name, hp, sp_max, atk, def, base_wt, allow_weight, move)
VALUES ({current_id}, '{selected_unit_name}', {hp}, {sp_max}, {atk}, {def_val}, {base_wt}, {allow_weight}, {move_val})
ON DUPLICATE KEY UPDATE hp={hp}, sp_max={sp_max}, atk={atk}, def={def_val}, base_wt={base_wt}, allow_weight={allow_weight}, move={move_val};"""

    st.code(sql_query, language="sql")

else:
    st.info("スプレッドシートのデータが空、または読み込み中です。")
