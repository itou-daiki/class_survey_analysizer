import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Streamlitアプリの設定
st.set_page_config(page_title="授業アンケート分析")

# アプリケーションのタイトルと説明
st.title("授業アンケート分析")
st.caption("Created by Dit-Lab.(Daiki Ito)")

# ファイルアップローダー
uploaded_file = st.file_uploader('Excelファイルをアップロードしてください', type=['xlsx'])

# データフレームの作成
df = None

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # 全ての列が空の列を削除
    empty_columns = df.columns[df.isna().all()].tolist()
    df = df.dropna(axis=1, how='all')
    
    st.write(df.head())
    
    st.subheader('分析データの選択')

    # カテゴリ変数の抽出
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    # 数値変数の抽出
    numerical_cols = df.select_dtypes(exclude=['object', 'category']).columns.tolist()

    # 教科・教員データの選択
    st.subheader("教科・教員データの選択")
    
    # カテゴリデータがない場合の処理
    if len(categorical_cols) == 0:
        st.error('カテゴリ（文字列）データがありません')
        st.stop()
    
    subject = st.multiselect('教科を示す列を選択してください', categorical_cols,max_selections=1)
    teacher = st.multiselect('教員を示す列を選択してください', categorical_cols,max_selections=1)
    
    # 数値データがない場合の処理
    if len(numerical_cols) == 0:
        st.error('数値データがありません')
        st.stop()

    # 分析用データの抽出
    st.subheader("分析する数値データの選択")
    num_vars = st.multiselect('分析に使用する数値データを選択してください', numerical_cols)

    # 選択したデータのみを抽出し、表示する
    temp_df = df[[*subject, *teacher, *num_vars]]
    
    #temp_dfをセッションに保存
    st.session_state.temp_df = temp_df
    
    # 分析用データの表示
    st.subheader("分析用データ")
    st.write(temp_df)
    
    # 分析実行ボタンの表示
    if st.button('分析実行'):
        
        # ヘッダーの表示
        st.header('授業アンケート分析')

        st.subheader('全体概要')

        # 要約統計量の表示
        
        # num_varsに格納されている整数の出現割合を計算
        num_vars_ratio = df[num_vars].apply(lambda x: x.value_counts(normalize=True)).T
        
        # num_vars_ratioの行の順番を反転
        num_vars_ratio = num_vars_ratio.loc[:, ::-1]
        
        # 列の左半分の合計値を計算
        num_vars_ratio['肯定群'] = num_vars_ratio.iloc[:, :len(num_vars) // 2].sum(axis=1)
        
        # 列の右半分の合計値を計算
        num_vars_ratio['否定群'] = num_vars_ratio.iloc[:, len(num_vars) // 2:].sum(axis=1)
    
        # 平均値を追加
        num_vars_ratio['平均値'] = df[num_vars].mean()
        
        # num_vars_ratioを表示
        st.write(num_vars_ratio)        

        # 数値データの平均値の可視化（棒グラフ）
        mean_df = df[[*num_vars]]
        max_value = mean_df.max().max()
        fig = px.bar(mean_df.mean(), title='設問ごとの平均値')
        fig.update_yaxes(range=[0, max_value])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


        st.subheader('教科別分析')

        st.subheader('教師別分析')




else:
    st.error('Excelファイルをアップロードしてください')


# Copyright表示
st.markdown('© 2022-2023 Dit-Lab.(Daiki Ito). All Rights Reserved.')