import tushare as ts
import itchat
import time


itchat.auto_login(hotReload=True)
me = 'filehelper'#, itchat.search_friends()['UserName']]
switcher = 0
enable_autore=True
lines={'002603': (17.23, 18.00, 17.23, 1)}
last_warning = {}
while True:
    for code in lines.keys():
        real_price = float(ts.get_realtime_quotes(code)['price'][0])
        if real_price<=lines[code][0] or real_price>=lines[code][1]:
            curr_warning = '%.2f (%s %d) ' % (float(real_price), code, 100*(real_price-lines[code][2])*lines[code][3])
            if curr_warning != last_warning:
                itchat.send(curr_warning+time.ctime().split()[3][:-3], me)  # switcher = int(switcher==0)
                print(curr_warning+ 'send.')
                last_warning = curr_warning
        time.sleep(5)
        itchat.auto_login(hotReload=True)
        me = ['filehelper', itchat.search_friends()['UserName']]