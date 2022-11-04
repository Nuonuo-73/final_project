from urllib.request import urlopen, quote
from pyecharts.charts import Pie
from pyecharts import options as opts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import streamlit_echarts
import requests
import json
import cufflinks as cf
cf.set_config_file(offline=True)

st.title('Best Cities & Countries for Startups')

plt.style.use('seaborn')

df = pd.read_csv('best cities for startups in 2022 - in 2022.csv', encoding='gbk')
df_2 = df['city'].str.split(',', expand = True)
df_3 = df.drop('city', axis = 1).join(df_2)
df_3.rename(columns={0:'city', 1:'country'}, inplace=True)
df_3.index = np.arange(1, len(df)+1)
st.dataframe(df_3)

df_country = df_3.groupby(['country']).mean()
df_country.sort_values(['total score'], axis=0, ascending=False, inplace=True)
df_country = df_country.reset_index()

#图1柱状图
df_4 = df_country.head(10)
df_5 = df_4[['country','total score']].set_index('country')
fig_1 = df_5.iplot(asFigure=True, kind='bar',title='Top 10 Countries for Startups\n(Total Score)')
st.plotly_chart(fig_1)

#add a new column to the existing interactive table
city_count_list = []

for country in df_country.country:
    city_count_list.append(df_3[df_3['country'] == country].groupby('country')['country'].value_counts()[0])

#make a sort according to the number of the best cities in the country
df_city_count = df_3.country
result_city_count = df_city_count.value_counts()

#图2柱状图
fig_2 = result_city_count[::-1][-10:].iplot(asFigure=True, kind='barh',title='Top 10 Countries for Startups\n(Best City Total)')
st.plotly_chart(fig_2)

#show new interactive table(score_top_10)
df_country.index = np.arange(1, len(df_country)+1)
df_country = df_country.drop('position', axis = 1)
df_country['best cities'] = city_count_list
st.dataframe(df_country[:10])

#为饼图添加标题
st.subheader('   Proportion of the Best Cities in the Top 10 Countries')
#制作饼图
score_top_countries = df_country[:10].country.tolist()#[' United Arab Emirates', ' Singapore', ' China', ' United States', ' South Korea', ' Israel', ' Estonia', ' Indonesia', ' Japan', ' India']#
value = df_country[:10]['best cities'].tolist()#[3, 1, 44, 257, 5, 13, 2, 5, 11, 37]#

streamlit_echarts.st_pyecharts(
        Pie()
        .add(
            '',
            list(zip(score_top_countries, value)),
            center=["45%", "50%"],
            label_opts=opts.LabelOpts(
                is_show=True,
                position='outside',
                font_size=15,
                #b c d
                #country；count；position
                formatter='{b|{b}: }{c}  {per|{d}%}  ',
                background_color='#d6fffa',
                border_color='#aaa',
                border_width=1,
                border_radius=4,
                #Unable to find how to directly set lineheight, so try to call rich text
                rich={
                    "b": {"lineHeight": 29},  
                },
            ),
        )
        .set_global_opts(
            #title_opts=opts.TitleOpts(title='Proportion of the Best Cities in the Top 10 Countries'),
            legend_opts=opts.LegendOpts(type_='scroll', pos_left='80%', item_gap = 20, item_width = 20, orient='vertical'),# orient='vertical'
        )
    )


#制作堆叠图
top_cities = df.head(20)
top_cities_info = top_cities[['city', 'quantity score', 'quality score', 'business score']].set_index('city')

fig_3 = top_cities_info.iplot(asFigure=True, kind='bar',barmode='stack',title='Inpact of different scores')
st.plotly_chart(fig_3)

#制作折线图
fig, ax4 = plt.subplots(1, 3, figsize=(15,5))
ax4[0].plot(top_cities[['total score','quality score']], marker='o')
ax4[1].plot(top_cities[['total score','quantity score']], marker='o')
ax4[2].plot(top_cities[['total score','business score']], marker='o')
st.pyplot(fig, ax4[0])
st.pyplot(fig, ax4[1])
st.pyplot(fig, ax4[2])


##获取城市的地理信息
#for i in df_3[df_3['country'] == ' China']['city'].index:
#    if df_3[df_3['country'] == ' China']['city'][i].find("'") != -1:
#        df_3.loc[i, 'city']= df_3.loc[i, 'city'].replace("'",'')

#addr_city = df_3[df_3['country'] == ' China']['city'].tolist()
 
#def gaode(addr_city):
#    para = {
#        "address": quote(addr_city), #传入地址参数
#        "key": "6c4d227098e7cda4345c79be1778faa6" #高德地图开放平台申请ak
#    }
#    url = "https://restapi.amap.com/v3/geocode/geo?"
#    req = requests.get(url,para)
#    req = req.json()
#    m = req
#    return m

#lat_list = []
#lon_list = []
#for city in addr_city:
#    lon_list.append(gaode(city)['geocodes'][0]['location'].split(',')[0])
#    lat_list.append(gaode(city)['geocodes'][0]['location'].split(',')[1])

##更新出一个新的表格
#df_china=df_3[df_3['country'] == ' China']
#df_china.index = np.arange(1, len(df_china)+1)
#df_china['lat'] = lat_list
#df_china['lon'] = lon_list
#df_china = df_china.drop('country', axis=1)
#df_china['lon'] = df_china['lon'].astype(float)
#df_china['lat'] = df_china['lat'].astype(float)
#侧边栏筛选项
#创建新列
#position_change = []

#for i in df_china.index:
#    if df_china['change in position from 2021'][i] != 'new':
#        if (df_china['sign of change in position'][i] == '+') & (int(df_china['change in position from 2021'][i]) > 100) :
#            position_change.append('substantial increase')
#        elif (df_china['sign of change in position'][i] == '+') & (int(df_china['change in position from 2021'][i]) > 10) :
#            position_change.append('obvious increase')
#        elif (df_china['sign of change in position'][i] == '+') & (int(df_china['change in position from 2021'][i]) <= 10):
#            position_change.append('small increase')
#        elif (df_china['sign of change in position'][i] == '-') & (int(df_china['change in position from 2021'][i]) > 100) :
#            position_change.append('substantial decrease')
#        elif (df_china['sign of change in position'][i] == '-') & (int(df_china['change in position from 2021'][i]) > 10) :
#            position_change.append('obvious decrease')
#        elif (df_china['sign of change in position'][i] == '-') & (int(df_china['change in position from 2021'][i]) <= 10):
#            position_change.append('small decrease')
#        else :
#            position_change.append('remain unchanged')
#    else:
#        position_change.append('new best city')

#删除原有列并加入新列
#df_china = df_china.drop('sign of change in position', axis=1).drop('change in position from 2021', axis=1)
#df_china['position change'] = position_change

#保存为新文件(让后续筛选更迅速)
#df_china.to_csv('df_map_china.csv', index=False)
#读取新文件
df_map = pd.read_csv('df_map_china.csv')
st.subheader('   Distribution of the best cities in China')
st.dataframe(df_map)

##设立侧边栏筛选项
###输入值作为筛选
form = st.sidebar.form('total_score_form')
total_score_filter = form.text_input('The total score is above?(please enter a integer number)', '0')
form.form_submit_button('Apply')

###变动作为筛选
position_change_filter = st.sidebar.multiselect(
    'World ranking compared with 2021',
        df_map['position change'].unique(),
        df_map['position change'].unique())

###选择作为筛选
business_score_filter = st.sidebar.radio(
    "Choose business score level",
    ('higher than 2', 'higher than 1', 'all')
)
quality_score_filter = st.sidebar.radio(
    "Choose quality level",
    ('higher than 50', 'higher than 10', 'all')
)
quantity_score_filter = st.sidebar.radio(
    "Choose quantity level",
    ('higher than 5', 'higher than 1', 'all')
)

###filter by these filter
if total_score_filter!= '0':
    df_map = df_map[df_map['total score'].astype(float) >= int(total_score_filter)]
#这次应该正确
df_map = df_map[df_map['position change'].isin(position_change_filter)]


if business_score_filter == 'all':
    df_map = df_map[df_map['business score'].astype(float) > 0]
elif business_score_filter == 'higher than 1':
    df_map = df_map[df_map['business score'].astype(float) > 1]
elif business_score_filter == 'higher than 2':
    df_map = df_map[df_map['business score'].astype(float) > 2]

if quality_score_filter == 'all':
    df_map = df_map[df_map['quality score'].astype(float) > 0]
elif business_score_filter == 'higher than 10':
    df_map = df_map[df_map['quality score'].astype(float) > 10]
elif business_score_filter == 'higher than 50':
    df_map = df_map[df_map['quality score'].astype(float) > 50]

if quantity_score_filter == 'all':
    df_map = df_map[df_map['quantity score'].astype(float) > 0]
elif business_score_filter == 'higher than 1':
    df_map = df_map[df_map['quantity score'].astype(float) > 1]
elif business_score_filter == 'higher than 5':
    df_map = df_map[df_map['quantity score'].astype(float) > 5]

##绘制地图


st.map(df_map)