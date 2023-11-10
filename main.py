import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('美容院の売上試算（新規顧客とリピーターの分析）')
st.write('（新規顧客数のリピート率は既存顧客のリピート率の-30%と仮定）')

# ユーザー入力
with st.expander("オプション"):
    col1, col2 = st.columns(2)
    new_customers_per_month = col1.number_input('月間新規顧客数', min_value=0, value=60)
    customer_unit_price = col2.number_input('平均サービス単価', min_value=0, value=5000)

def calculate_customers_sales(new_customers_per_month, new_customer_repeat_rate, existing_customer_repeat_rate, customer_unit_price, months):
    total_new_customers = 0
    monthly_results = []

    for month in range(1, months+1):
        total_new_customers += new_customers_per_month

        if month == 1:
            existing_repeater_sales = 0
        else:
            existing_customers = total_new_customers - new_customers_per_month
            existing_repeater_sales = existing_customers * existing_customer_repeat_rate * customer_unit_price

        new_customer_repeats = new_customers_per_month * new_customer_repeat_rate
        new_repeater_sales = new_customer_repeats * customer_unit_price

        monthly_results.append({
            'new_sales': new_customers_per_month * customer_unit_price,
            'existing_repeater_sales': existing_repeater_sales,
            'new_repeater_sales': new_repeater_sales,
        })
    return monthly_results

def plot_customer_sales(new_customers_per_month, customer_unit_price, months, year):
    existing_customer_repeater_rates = np.arange(0, 1.1, 0.1)
    new_sales = []
    existing_repeater_sales = []
    new_repeater_sales = []

    for existing_customer_rate in existing_customer_repeater_rates:
        new_customer_repeat_rate = max(existing_customer_rate - 0.4, 0)
        monthly_results = calculate_customers_sales(new_customers_per_month, new_customer_repeat_rate, existing_customer_rate, customer_unit_price, months)

        total_new_sales = sum([month['new_sales'] for month in monthly_results])/year
        total_existing_repeater_sales = sum([month['existing_repeater_sales'] for month in monthly_results])/year
        total_new_repeater_sales = sum([month['new_repeater_sales'] for month in monthly_results])/year

        new_sales.append(total_new_sales)
        existing_repeater_sales.append(total_existing_repeater_sales)
        new_repeater_sales.append(total_new_repeater_sales)

    bar_width = 0.35
    index = np.arange(len(existing_customer_repeater_rates))

    fig, ax = plt.subplots()
    bar1 = ax.bar(index, new_sales, bar_width, label='Newcomer')
    bar2 = ax.bar(index, existing_repeater_sales, bar_width, bottom=new_sales, label='Existing Repeater')
    bar3 = ax.bar(index, new_repeater_sales, bar_width, bottom=[i+j for i, j in zip(new_sales, existing_repeater_sales)], label='New Repeater')

    ax.set_ylim(0, 100000000)
    ax.set_xlabel('Existing Customer Repeater(%)')
    ax.set_ylabel('1oku yen')
    ax.set_title(f'Sales Breakdown for {months//12}th Year(s)')
    ax.set_xticks(index)
    ax.set_xticklabels([f'{int(rate*100)}%' for rate in existing_customer_repeater_rates])
    ax.legend()

    return fig

st.subheader('8割の売上は2割のロイヤル顧客から得られる')

st.write('青色：新規顧客の売上')
st.write('オレンジ色：3回以上リピートした顧客の売上')
st.write('緑色：2回リピートした顧客の売上')

if st.button('売上を表示'):
    years = [12, 24, 36, 48, 60]
    for year in years:
        fig = plot_customer_sales(new_customers_per_month, customer_unit_price, year, year/12)
        st.pyplot(fig)

