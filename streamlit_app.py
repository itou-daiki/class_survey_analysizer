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
    # subjectが選択されている場合のみ、教科の選択肢を表示
    if len(subject) == 0:
        st.stop()
    selected_subject = st.multiselect('教科を選択してください', df[subject].iloc[:,0].unique().tolist())
    teacher = st.multiselect('教員を示す列を選択してください', categorical_cols,max_selections=1)
    if len(teacher) == 0 or len(subject) == 0:
        st.stop()
    selected_teacher = st.multiselect('教員を選択してください', df[teacher].iloc[:,0].unique().tolist())
    
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
        
        # num_varsに格納されている整数の出現割合を計算
        num_vars_ratio = df[num_vars].apply(lambda x: x.value_counts(normalize=True)).T
        
        # num_vars_ratioの行の順番を反転
        num_vars_ratio = num_vars_ratio.loc[:, ::-1]
               
        # 各行ごとに肯定群（４・３）と否定群（２・１）の割合を計算
        num_vars_ratio['肯定群'] = num_vars_ratio.get(4, 0) + num_vars_ratio.get(3, 0)
        num_vars_ratio['否定群'] = num_vars_ratio.get(2, 0) + num_vars_ratio.get(1, 0)
    
        # 平均値を追加
        num_vars_ratio['平均値'] = df[num_vars].mean()
        
        # num_vars_ratioを表示（小数点第２位まで）
        st.write(num_vars_ratio.style.format('{:.2%}'))

        # 数値データの平均値の可視化（棒グラフ）
        mean_df = df[[*num_vars]]
        max_value = mean_df.max().max()
        fig = px.bar(mean_df.mean(), title='設問ごとの平均値')
        fig.update_yaxes(range=[0, max_value])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


        st.subheader('教科別分析')
        # temp_dfから選択した教科のデータのみを抽出し、新しいデータフレームに格納
        subject_df = temp_df[temp_df[subject].iloc[:,0].isin(selected_subject)]
        st.write(subject_df)
        
        # num_varsに格納されている整数の出現割合を計算
        subject_ratio_df = subject_df[num_vars].apply(lambda x: x.value_counts(normalize=True)).T
        
        # num_vars_ratioの行の順番を反転
        subject_ratio_df = subject_ratio_df.loc[:, ::-1]
        
        # 各行ごとに肯定群（４・３）と否定群（２・１）の割合を計算
        subject_ratio_df['肯定群'] = subject_ratio_df.get(4, 0) + subject_ratio_df.get(3, 0)
        subject_ratio_df['否定群'] = subject_ratio_df.get(2, 0) + subject_ratio_df.get(1, 0)

        # num_varsの各要素がsubject_ratio_dfに存在するか確認
        subject_valid_vars = [var for var in num_vars if var in subject_ratio_df.columns]

        # 平均値を追加,平均が計算できない場合はNoneを追加
        subject_ratio_df['平均値'] = subject_df[subject_valid_vars].mean(skipna=True)
        
        # num_vars_ratioを表示（小数点第２位まで）
        st.write(subject_ratio_df.style.format('{:.2%}'))

        # 数値データの平均値の可視化（棒グラフ）
        subject_ratio_mean_df = subject_ratio_df[[*num_vars]]
        max_value = subject_ratio_mean_df.max().max()
        fig = px.bar(subject_ratio_mean_df.mean(), title='設問ごとの平均値')
        fig.update_yaxes(range=[0, max_value])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('教師別分析')




else:
    st.error('Excelファイルをアップロードしてください')


# Copyright表示
st.markdown('© 2022-2023 Dit-Lab.(Daiki Ito). All Rights Reserved.')