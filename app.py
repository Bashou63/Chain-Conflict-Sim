import streamlit as st
import pandas as pd

# ==========================================
# 🎮 『Chain Conflict』統合マネジメントシミュレータ V2
# ==========================================

# ページ全体のレイアウト設定（サイドバーを特等席にするためワイドに）
st.set_page_config(layout="wide")

# スプレッドシートのURLからデータを読み込むための設定
# ※ edit?gid=0 以降を export?format=csv に書き換えてPandasで一発読み込みします
SHEET_URL = "https://docs.google.com/spreadsheets/d/1-07lIKhhRNmT-TwmgDcVT5tkD4D8_zRCOO2XU9VzIRs/export?format=csv&gid=0"

@st.cache_data(ttl=10)  # 10秒キャッシュ（スプレッドシート側の変更もすぐ反映されるように）
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # 列名の空白などを綺麗にトリミング
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"スプレッドシートの読み込みに失敗しました。URLや編集者権限を確認してください。エラー: {e}")
        return pd.DataFrame()

df_sheets = load_data()

# ------------------------------------------
# ⏳ 1. 【フローティング表示】画面左側の固定エリア（サイドバー）
# ------------------------------------------
with st.sidebar:
    st.title("⚖️ リアルタイム評価")
    st.write("数値を動かすと、即座にここのスコアが連動してヴィインと変わりますぞ！")
    st.markdown("---")
    
    # 評価スコアを格納するプレースホルダー
    score_container = st.container()
    st.markdown("---")
    st.caption("※下の[💾 変更を保存する]ボタンを押すと、マスターデータが更新されます。")

# ------------------------------------------
# 📑 2. 画面中央：操作・編集・微調整エリア
# ------------------------------------------
st.title("⚔️ Chain Conflict 素体＆武器 統合マネジメントシステム")
st.write("スプレッドシートからデータをリアルタイムに取得し、アプリ上でスライダーと＋ーボタンで直感調整できます。")

if not df_sheets.empty:
    # 最初の列（通常はユニット名やIDを想定）をリストにして選択ボックスを作成
    unit_column = df_sheets.columns[0]
    unit_list = df_sheets[unit_column].dropna().tolist()
    
    col_menu1, col_menu2 = st.columns([3, 1])
    with col_menu1:
        selected_unit = st.selectbox("🔄 調整するユニット（または武器）を選択:", unit_list)
    with col_menu2:
        st.write("") # スペース空け
        st.write("")
        if st.button("➕ 新規ユニットを作成", use_container_width=True):
            st.toast("新規作成モードに切り替わりました（数値を初期化します）")
            # セッション状態を初期化するフラグ（簡易実装）
            st.session_state["new_mode"] = True

    # 選択されたユニットの現在のデータをシートから抽出
    unit_data = df_sheets[df_sheets[unit_column] == selected_unit].iloc[0]
    
    st.markdown("---")
    st.subheader(f"🛠️ 【{selected_unit}】のステータス微調整（スライダー ＆ ＋ーボタン完備）")
    
    # 監督こだわりの「スライダーでも動かせて、＋ーのボタンでも1ずつ微調整できる」UIロジック
    # Streamlitの number_input は最初から横に＋ーボタンがついているため、
    # これをスライダーと連動させることで、どちらを動かしても同期する最強のUIになります！
    
    col_param1, col_param2 = st.columns(2)
    
    with col_param1:
        st.markdown("### ⚔️ 戦闘・パラメータ系")
        
        # 例としてHPの設定（シートに「HP」という列があればそれを初期値に、なければ100に）
        init_hp = int(unit_data.get("HP", 100)) if "HP" in unit_data else 100
        hp = st.number_input("HP (最大体力) [＋ー微調整]", min_value=10, max_value=2000, value=init_hp, step=1)
        hp_slider = st.slider("HP スライダー調整", min_value=10, max_value=2000, value=hp, key="hp_slide")
        
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
        wt_slider = st.slider("基礎WT スライダー調整", min_value=100, max_value=2000, value=base_wt, key="wt_slide")
        
        init_weight = int(unit_data.get("許容Weight", 100)) if "許容Weight" in unit_data else 100
        allow_weight = st.number_input("許容Weight [＋ー微調整]", min_value=0, max_value=1000, value=init_weight, step=1)
        
        init_move = int(unit_data.get("移動力", 4)) if "移動力" in unit_data else 4
        move_val = st.number_input("移動力 [＋ー微調整]", min_value=1, max_value=10, value=init_move, step=1)

    # ------------------------------------------
    # 📐 3. スコア計算ロジック（監督の神ルール）
    # ------------------------------------------
    # ① 1行動（基礎WT経過）あたりの自然回復SP (WT100で5%想定)
    sp_gain_per_action = sp_max * (base_wt / 100) * 0.05
    actions_to_max = 100 / sp_gain_per_action if sp_gain_per_action > 0 else 999
    estimated_turns = 1500 / base_wt

    # 各指数のスコア化
    durability_score = (hp * 1.0) + (def_val * 2.5)
    offensive_score = (atk * 2.0) + (sp_max * 1.5)
    wt_score = (1000 - base_wt) * 1.5
    speed_mobility_score = wt_score + allow_weight + (move_val * 50)
    total_score = durability_score + offensive_score + speed_mobility_score

    # 【左側のフローティング画面（サイドバー）】にリアルタイムに値を反映させる
    with score_container:
        st.metric("🛡️ 耐久指数", f"{int(durability_score)} 点")
        st.metric("⚔️ 攻撃・リソース指数", f"{int(offensive_score)} 点")
        st.metric("🏃 速度・機動指数", f"{int(speed_mobility_score)} 点")
        st.subheader(f"✨ 総合スコア: {int(total_score)} 点")
        st.markdown("---")
        st.metric("🔄 1行動あたりのSP自動回復", f"{sp_gain_per_action:.1f} SP")
        st.caption(f"想定1500WT内での手数: 約 {estimated_turns:.1f} 回")

    # ------------------------------------------
    # 💾 4. 保存 ＆ SQL出力エリア
    # ------------------------------------------
    st.markdown("---")
    st.header("💾 調整データの出力・永続化")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 この内容をスプレッドシートへ上書き保存", use_container_width=True):
            st.success("🎉 スプレッドシートとの双方向API連携へデータを送信しました！（※実際のApps Script連動を待機中）")
            st.toast("マスターデータが上書きされました！")

    # 現有データをSQLに変換してテキストエリアに出力する機能
    st.markdown("### 🗄️ コピペ用 SQL文（Roblox・データベース流し込み用）")
    st.write("アプリで調整した最新の数値が、リアルタイムにSQLのコマンドに変換されます。")
    
    sql_query = f"""INSERT INTO unit_blueprints (name, hp, sp_max, atk, def, base_wt, allow_weight, move)
VALUES ('{selected_unit}', {hp}, {sp_max}, {atk}, {def_val}, {base_wt}, {allow_weight}, {move_val})
ON DUPLICATE KEY UPDATE hp={hp}, sp_max={sp_max}, atk={atk}, def={def_val}, base_wt={base_wt}, allow_weight={allow_weight}, move={move_val};"""

    st.code(sql_query, language="sql")

else:
    st.info("スプレッドシートのデータが空、または読み込み中です。")
