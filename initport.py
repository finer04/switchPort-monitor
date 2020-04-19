import core
import sys,os

def processing(host):
    global core
    portlist = []
    cr = core.searchinfomation(host,' ',' ')
    iflist = core.initdescr(host) # 发现交换机主机的所有端口

    # Linux 需要更改分隔符
    path = os.getcwd()+'\\data\\hosts\\' + host

    for i in iflist:
        #ifPortname = re.sub(r'IF-MIB::ifDescr.[0-9]* = STRING: ','',i)
        portdict = {}
        # 分析 SNMP
        splitresult = i.split(' ')
        a = splitresult[3] # 接口
        c = cr.analysisinterfaces(a) # 分析接口信息
        c['Host'] = host
        c['Hostname'] = cr.getswitchname()
        portlist.append(c)

    # 存储设备信息到文件，先判断有无目录
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass

    # 写入信息
    fileObject = open(path+'\\AllPortDict.txt','w')
    for line in portlist:
        fileObject.write(str(line).replace("\'","\""))
        fileObject.write('\n')
    fileObject.close()

def main():
    load_list_tmp = []
    path = os.getcwd()+'\\data\\'
    # 录入交换机IP
    with open(path+'jiankong_list.txt') as f:
        lines = f.read().split('\n')

        for line in lines:
            tmp = line.split(' ')[0]
            load_list_tmp.append(tmp)

    # 去重
    load_list = list(set(load_list_tmp))

    # 开始爬取
    for i in range(len(load_list)):
        print(f'walking... now {load_list[i]}')
        processing(load_list[i])

if __name__ == '__main__':
    main()