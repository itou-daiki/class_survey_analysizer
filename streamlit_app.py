import streamlit as st
import pandas as pd

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
    cat_var = st.multiselect('教科を示す列を選択してください', categorical_cols,max_selections=1)
    cat_var = st.multiselect('教員を示す列を選択してください', categorical_cols,max_selections=1)
    
    # 数値データがない場合の処理
    if len(numerical_cols) == 0:
        st.error('数値データがありません')
        st.stop()

    # 分析用データの抽出
    st.subheader("分析する数値データの選択")
    num_vars = st.multiselect('分析に使用する数値データを選択してください', numerical_cols)

    # 選択したデータのみを抽出し、表示する
    temp_df = df[[cat_var, num_vars]]
    st.write(temp_df)

    st.header('授業アンケート分析')

    # 要約統計量の表示
    st.subheader('要約統計量')
    temp_df.describe(include='all').transpose()

    # 数値データの可視化の表示（箱ひげ図）
    for col in num_vars:
        fig = px.box(temp_df, y=col, color=cat_var)
        st.plotly_chart(fig)


    st.subheader('全体概要')

    st.subheader('教科別分析')

    st.subheader('教師別分析')




else:
    st.error('Excelファイルをアップロードしてください')


# Copyright表示
st.markdown('© 2022-2023 Dit-Lab.(Daiki Ito). All Rights Reserved.')