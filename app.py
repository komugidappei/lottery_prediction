import streamlit as st
import pandas as pd
import os
from lottery_analyzer import LotteryAnalyzer
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="宝くじ予想AI",
    page_icon="🎰",
    layout="wide"
)

st.title("🎰 宝くじ予想AI")
st.markdown("過去データを分析して次回の当選番号を予想します")

@st.cache_data
def load_analyzer():
    return LotteryAnalyzer()

analyzer = load_analyzer()

def upload_and_process_csv(lottery_type, expected_columns):
    st.subheader(f"{lottery_type} データアップロード")
    uploaded_file = st.file_uploader(
        f"{lottery_type}のCSVファイルをアップロード",
        type=['csv'],
        key=f"{lottery_type}_upload"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                st.error(f"必要な列が見つかりません: {missing_columns}")
                return False
            
            csv_path = f"data/{lottery_type}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            count = analyzer.load_data(lottery_type, csv_path)
            st.success(f"{lottery_type}データを読み込みました ({count}回分)")
            
            st.dataframe(df.head(), use_container_width=True)
            return True
            
        except Exception as e:
            st.error(f"データ読み込みエラー: {str(e)}")
            return False
    
    return False

def show_frequency_chart(lottery_type, numbers_prefix, max_number):
    if lottery_type in analyzer.data:
        frequency = analyzer.analyze_frequency(lottery_type, numbers_prefix, max_number)
        
        fig = px.bar(
            x=list(frequency.keys()),
            y=list(frequency.values()),
            title=f"{lottery_type} 数字別出現頻度 (過去30回)",
            labels={'x': '数字', 'y': '出現回数'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    tab1, tab2, tab3, tab4 = st.tabs(["ロト6", "ロト7", "ナンバーズ3", "ナンバーズ4"])
    
    with tab1:
        st.header("🎯 ロト6予想")
        
        loto6_columns = ['date', 'day', 'loto6_1', 'loto6_2', 'loto6_3', 'loto6_4', 'loto6_5', 'loto6_6', 'bonus']
        data_loaded = upload_and_process_csv('loto6', loto6_columns)
        
        if data_loaded or 'loto6' in analyzer.data:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 分析結果")
                recent_count = st.slider("分析対象回数", 10, 100, 30, key="loto6_recent")
                
                if st.button("予想実行", key="loto6_predict"):
                    with st.spinner("分析中..."):
                        result, explanation = analyzer.predict_loto6(recent_count)
                        
                        if result:
                            prediction, bonus = result
                            st.success("✨ 予想完了!")
                            
                            st.markdown("### 🎯 予想番号")
                            prediction_str = " - ".join([f"**{num}**" for num in sorted(prediction)])
                            st.markdown(f"本数字: {prediction_str}")
                            st.markdown(f"ボーナス: **{bonus}**")
                            
                            st.markdown("### 📝 予想根拠")
                            st.text(explanation)
                        else:
                            st.error(explanation)
            
            with col2:
                st.subheader("📈 出現頻度グラフ")
                show_frequency_chart('loto6', 'loto6_', 43)
    
    with tab2:
        st.header("🎯 ロト7予想")
        
        loto7_columns = ['date', 'day', 'loto7_1', 'loto7_2', 'loto7_3', 'loto7_4', 'loto7_5', 'loto7_6', 'loto7_7', 'bonus1', 'bonus2']
        data_loaded = upload_and_process_csv('loto7', loto7_columns)
        
        if data_loaded or 'loto7' in analyzer.data:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 分析結果")
                recent_count = st.slider("分析対象回数", 10, 100, 30, key="loto7_recent")
                
                if st.button("予想実行", key="loto7_predict"):
                    with st.spinner("分析中..."):
                        result, explanation = analyzer.predict_loto7(recent_count)
                        
                        if result:
                            prediction, bonus_list = result
                            st.success("✨ 予想完了!")
                            
                            st.markdown("### 🎯 予想番号")
                            prediction_str = " - ".join([f"**{num}**" for num in sorted(prediction)])
                            st.markdown(f"本数字: {prediction_str}")
                            st.markdown(f"ボーナス1: **{bonus_list[0]}**")
                            st.markdown(f"ボーナス2: **{bonus_list[1]}**")
                            
                            st.markdown("### 📝 予想根拠")
                            st.text(explanation)
                        else:
                            st.error(explanation)
            
            with col2:
                st.subheader("📈 出現頻度グラフ")
                show_frequency_chart('loto7', 'loto7_', 37)
    
    with tab3:
        st.header("🎯 ナンバーズ3予想")
        
        numbers3_columns = ['date', 'day', 'number']
        data_loaded = upload_and_process_csv('numbers3', numbers3_columns)
        
        if data_loaded or 'numbers3' in analyzer.data:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 分析結果")
                recent_count = st.slider("分析対象回数", 10, 100, 30, key="numbers3_recent")
                
                if st.button("予想実行", key="numbers3_predict"):
                    with st.spinner("分析中..."):
                        prediction, explanation = analyzer.predict_numbers3(recent_count)
                        
                        if prediction:
                            st.success("✨ 予想完了!")
                            
                            st.markdown("### 🎯 予想番号")
                            st.markdown(f"**{prediction}**")
                            
                            st.markdown("### 📝 予想根拠")
                            st.text(explanation)
                        else:
                            st.error(explanation)
            
            with col2:
                st.subheader("📊 データ情報")
                if 'numbers3' in analyzer.data:
                    data_info = analyzer.data['numbers3']
                    st.metric("総データ数", len(data_info))
                    st.metric("最新抽選日", str(data_info['date'].max())[:10])
    
    with tab4:
        st.header("🎯 ナンバーズ4予想")
        
        numbers4_columns = ['date', 'day', 'number']
        data_loaded = upload_and_process_csv('numbers4', numbers4_columns)
        
        if data_loaded or 'numbers4' in analyzer.data:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 分析結果")
                recent_count = st.slider("分析対象回数", 10, 100, 30, key="numbers4_recent")
                
                if st.button("予想実行", key="numbers4_predict"):
                    with st.spinner("分析中..."):
                        prediction, explanation = analyzer.predict_numbers4(recent_count)
                        
                        if prediction:
                            st.success("✨ 予想完了!")
                            
                            st.markdown("### 🎯 予想番号")
                            st.markdown(f"**{prediction}**")
                            
                            st.markdown("### 📝 予想根拠")
                            st.text(explanation)
                        else:
                            st.error(explanation)
            
            with col2:
                st.subheader("📊 データ情報")
                if 'numbers4' in analyzer.data:
                    data_info = analyzer.data['numbers4']
                    st.metric("総データ数", len(data_info))
                    st.metric("最新抽選日", str(data_info['date'].max())[:10])

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 使用方法")
    st.sidebar.markdown("""
    1. 各タブで対応するCSVファイルをアップロード
    2. 分析対象回数を調整
    3. 「予想実行」ボタンをクリック
    4. 予想結果と根拠を確認
    """)
    
    st.sidebar.markdown("### ⚠️ 注意事項")
    st.sidebar.markdown("""
    - この予想は過去データの統計分析に基づく参考情報です
    - 実際の当選を保証するものではありません
    - 宝くじは計画的に楽しみましょう
    """)

if __name__ == "__main__":
    main()