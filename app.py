import streamlit as st

# ==========================================
# 🎮 『Chain Conflict』素体バランス調整シミュレータ
# ==========================================

st.title("⚔️ Chain Conflict 素体調整シミュレータ")
st.write("9大ステータスと、WT・SPの回復効率をリアルタイムに評価するシミュレータです。")

st.markdown("---")

# 📋 2カラムでステータス入力フォームを作成
col1, col2 = st.columns(2)

with col1:
    st.header("⚔️ 戦闘・パラメータ系")
    hp = st.number_input("HP (最大体力)", min_value=10, max_value=2000, value=100, step=10)
    sp_max = st.number_input("最大SP (スキルタンク上限)", min_value=10, max_value=500, value=100, step=10)
    atk = st.number_input("ATK (物理攻撃力)", min_value=0, max_value=500, value=70, step=5)
    def_val = st.number_input("DEF (物理防御力)", min_value=0, max_value=500, value=60, step=5)
    int_val = st.number_input("INT (知力)", min_value=0, max_value=500, value=30, step=5)
    mnd = st.number_input("MND (精神力・回復・耐性)", min_value=0, max_value=500, value=50, step=5)

with col2:
    st.header("⏱️ 行動・機動系")
    base_wt = st.number_input("基礎WT (低いほど素早い)", min_value=100, max_value=2000, value=500, step=10)
    allow_weight = st.number_input("許容Weight", min_value=0, max_value=1000, value=100, step=10)
    move_val = st.number_input("移動力", min_value=1, max_value=10, value=4, step=1)
    move_type = st.selectbox("移動タイプ", ["徒歩", "忍者", "飛行", "浮遊"])

st.markdown("---")

# ==========================================
# 📐 監督の神ルールに基づいた【SP回復効率】の計算
# ==========================================
st.header("📊 バトルタイムライン・SP回復効率の評価")

# ① 1行動（基礎WT経過）あたりの自然回復SP
# ルール: WT100経過時に最大SPの5%を回復
sp_gain_per_action = sp_max * (base_wt / 100) * 0.05

# ② 大技（消費SP100想定）を発動するまでに必要な行動回数の目安
actions_to_max = 100 / sp_gain_per_action if sp_gain_per_action > 0 else 999

# ③ 1試合全体（想定1500WT）の中での手数と、攻撃・被弾ボーナスの期待値
# WTが短い（数値が小さい）ほど行動回数が増える
estimated_turns = 1500 / base_wt

# 画面表示
st.subheader(f"🔄 1行動（{base_wt} WT経過）あたりの自動回復量")
st.metric(label="SP自動チャージ量", value=f"{sp_gain_per_action:.1f} SP", delta=f"最大SPの {(base_wt/100)*5:.1f}%")

st.markdown(f"""
* **大技（SP100）発動までの目安:** 自然回復だけで約 **{actions_to_max:.1f} 回行動** で到達します。
* **重いユニットのメリット:** 基礎WTが重いほど、ターンが回ってきた時の自動チャージ量は大きくなります！
* **軽いユニットの手数ボーナス:** 基礎WTが短いユニットは、想定1500WTのバトル中に約 **{estimated_turns:.1f} 回** の行動順が巡るため、近接攻撃（+3%）や被弾（+1%）のトリガー回数が激増し、見た目以上の速度でSPが溜まります！
""")

st.markdown("---")

# ==========================================
# 📊 簡易ステータス・スコア化（評価モノサシ）
# ==========================================
st.header("⚖️ 総合素体評価（モノサシ値）")

# 各ステータスの重み付け計算
durability_score = (hp * 1.0) + (def_val * 2.5) + (mnd * 3.0)  # MNDは多機能なのでDEFより高評価
offensive_score = (atk * 2.0) + (int_val * 2.0) + (sp_max * 1.5)

# WTは低いほど高評価（反転計算）
wt_score = (1000 - base_wt) * 1.5
move_bonus = move_val * 50
if move_type == "忍者": move_bonus += 100
elif move_type in ["飛行", "浮遊"]: move_bonus += 150

speed_mobility_score = wt_score + allow_weight + move_bonus

total_score = durability_score + offensive_score + speed_mobility_score

# 評価のビジュアル表示
c1, c2, c3 = st.columns(3)
c1.metric("🛡️ 耐久指数", f"{int(durability_score)} 点")
c2.metric("⚔️ 攻撃・リソース指数", f"{int(offensive_score)} 点")
c3.metric("🏃 速度・機動指数", f"{int(speed_mobility_score)} 点")

st.subheader(f"✨ 総合素体スコア: **{int(total_score)} 点**")
