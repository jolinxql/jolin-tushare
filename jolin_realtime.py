import tushare as ts
import time
cash = 2278.42
earn = -45.72
lines={'002555': ((16.635, 4))}
total=cash
for code in lines.keys():
    total +=lines[code][0]*lines[code][1]*100
print(total)
while True:
    current_earn=0
    for code in lines.keys():
        real_price = float(ts.get_realtime_quotes(code)['price'][0])
        diff = 100*(real_price-lines[code][0])*lines[code][1]
        curr_warning = '(%.2f :%s %d %.1f %%) ' % (float(real_price), code,
                                          diff,
                                          diff/(lines[code][0]*lines[code][1]))
        print(curr_warning, end='')
        current_earn+=diff
        time.sleep(5)
    history_earn = current_earn + earn
    total_money = current_earn + total
    print(time.ctime().split()[3][:-3],'%.2f'%history_earn, '%.2f'%total_money)