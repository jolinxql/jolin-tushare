import tushare as ts
import pandas
import os
ts.get_today_all().to_csv('data/today.csv')
today = pandas.read_csv('data/today.csv')
today.index = today['code']
print('... loading done.')
"""code：代码
name:名称
changepercent:涨跌幅
trade:现价
open:开盘价
high:最高价
low:最低价
settlement:昨日收盘价
volume:成交量
turnoverratio:换手率"""
ts.get_stock_basics().to_csv('data/basic.csv')  #'Please wait.'
basic = pandas.read_csv('data/basic.csv')
basic.index = basic['code']
print('... loading done.')
"""code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本
totals,总股本(万)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
eps,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期"""
hists = []
for year,season in [(2013, 4), (2014, 4), (2015,4), (2016,3)]:  # 1:4/1-4/30,2:7/1-8/30,3:10/1-10/31,4:1/1-4/30
    if not os.path.exists('data/hist%d_%d.csv'%(year,season)):
        ts.get_growth_data(year,season).to_csv('data/hist%d_%d.csv'%(year,season))
    hist = pandas.read_csv('data/hist%d_%d.csv'%(year,season))
    hist.index=hist['code']
    hists.append(hist)
"""code,代码
name,名称
mbrg,主营业务收入增长率(%)
nprg,净利润增长率(%)
nav,净资产增长率
targ,总资产增长率
epsg,每股收益增长率
seg,股东权益增长率"""
print('... loading done.')
jiejins = []  #解禁
for year in range(2010, 2018):
    for month in range(1, 13):  #1:4/1-4/30,2:7/1-8/30,3:10/1-10/31,4:1/1-4/30
        if year==2017 and month==3: break
        try:
            if not os.path.exists('data/jiejin%d_%d.csv'%(year, month)):
                ts.xsg_data(year=str(year), month=str(month), retry_count=1).to_csv('data/jiejin%d_%d.csv'%(year, month))
            jiejin = pandas.read_csv('data/jiejin%d_%d.csv'%(year, month))
            jiejins.append(jiejin)
        except: continue
datas={}
head=['code','PE/sum(nprg)','PE','timeToMarket']
head_added=False
my_selected=[2555]
for code in today['code']:
    try:
        pe = float(basic.ix[code]['pe'])
    except:
        continue
    if code not in my_selected and\
            (int((str(basic.ix[code]['timeToMarket']))[:4])<=2009 or
                 (len(str(code))==6 and str(code)[:3]=='300')):
        continue
    datas[code] = []
    for hist in hists:
        try:
            nprg = float(hist.ix[code]['nprg'])
        except:
            nprg = -100.0
        if str(nprg) == 'nan': nprg = -100.0
        datas[code].append(nprg)
        if not head_added:
            head.insert(1, 'nprg')
    head_added=True
    datas[code].append(pe / sum(datas[code]) / len(datas[code]) * 100)
    datas[code].append(pe)
    datas[code].append('%s:%d (%s)' % (today.ix[code]['name'], basic.ix[code]['timeToMarket'], basic.ix[code]['industry']))
sorted_nprgs = sorted([item for item in datas.items()],
                      key = lambda item: 0 if item[0] in my_selected
                      else (item[1][-3] if item[1][-3]>0 else float('inf')))
print('... processing done.')
selected = sorted_nprgs[:200]
for code, vs in selected:
    time_to_mkt = basic.ix[code]['timeToMarket']
    total_ratio = 0.0
    last_date = '----------'
    for jiejin in jiejins:
        for index, row in jiejin.loc[jiejin.code == code].iterrows():
            total_ratio+=row['ratio']
            last_date = row['date']
    vs[-1]+=', ('+last_date+', '+str(total_ratio)[:5]+')'
print(head)
print('\n'.join([str(1000000+code)[1:]+' '+'\t'.join(['%5.2f'%v if isinstance(v, float) else v for v in vs])
                 for code, vs in selected]))
print('done')