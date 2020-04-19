import core
import os,re,time
import json
import threadpool

path = os.getcwd() + '\\data\\'
monitor_list = []

# 加载需要监控的接口到监控列表
def load_list():
    txt = open(path+'jiankong_list.txt','r')
    lines = txt.read().split('\n')

    for line in lines:
        monitor_dict = {}
        tmp = line.split(' ')
        monitor_dict['host'] = tmp[0]
        monitor_dict['interface'] = core.formattext('',tmp[1],'').ifname()
        monitor_list.append(monitor_dict)

# 匹配已经缓存的交换机条目
def preload():
    preload_list = []
    for i in range(len(monitor_list)):
        with open(path+'\\hosts\\'+monitor_list[i]['host']+'\\AllPortDict.txt','r') as f:
            tmp = f.read().split('\n')
            for o in tmp:
                regexname = re.compile(r'' + monitor_list[i]['interface'])
                if re.search(regexname,o) != None:
                    # 由于读取到是字符串，需要转换成字典
                    temp = json.loads(o)
                    preload_list.append(json.dumps(temp))
                    break

    return preload_list

def monitor(op1):
    # 我还不是很会数据处理，本来预加载的是字符串转成字典，字典列入到预处理的列表后，又要拆出来转换成字典，啊还是好好看书吧。
    op = json.loads(op1)
    q = core.searchinfomation(op['Host'], '', op['ifIndex'])
    status = q.watchupdown(op['ifIndex'])

    if status != 'Timeout':
        if status == 'Down':
            print(f'{op["Hostname"]} {op["Host"]} - {op["ifDescr"]} ({op["ifAlisa"]}) ----> {status}')
    else:
        print(f'{op["Hostname"]} {op["Host"]} ----> {status}')


def main():
    print('loading list..',end='')
    load_list()
    print(' ok')
    print('pulling into monitor-list...',end='')
    preload_list = preload()
    print(' ok')
    print('now monitoring..\n')
    while True:
        # 加载线程池
        pool = threadpool.ThreadPool(50)
        requests = threadpool.makeRequests(monitor,preload_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()

        time.sleep(5)

if __name__ == '__main__':
    main()