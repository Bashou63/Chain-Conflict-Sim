import streamlit as st

# ステート初期化
if 'stats' not in st.session_state:
    st.session_state.stats = {'HP': 100, 'ATK': 70, 'SP': 100, 'DEF': 60, 'WT': 500, 'MV': 4}

# HTML/CSSで強制横並びのテーブルを構築
html_content = """
<style>
    .compact-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .compact-table td { padding: 5px; text-align: center; vertical-align: middle; }
    .val-cell { font-weight: bold; font-size: 1.1em; }
</style>
<table class="compact-table">
"""
# ※注: ボタンのクリック処理は、後述のst.formで行います
