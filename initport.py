import core
import sys,os

def processing(host):
    global core
    portlist = []
    cr = core.searchinfomation(host,' ',' ')
    iflist = core.initdescr(host)


    path = os.getcwd()+'\\data\\hosts\\' + host

    for i in iflist:
        #ifPortname = re.sub(r'IF-MIB::ifDescr.[0-9]* = STRING: ','',i)
        portdict = {}
        splitresult = i.split(' ')
        a = splitresult[3]
        c = cr.analysisinterfaces(a)
        c['Host'] = host
        c['Hostname'] = cr.getswitchname()
        portlist.append(c)

    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass

    fileObject = open(path+'\\AllPortDict.txt','w')
    for line in portlist:
        fileObject.write(str(line).replace("\'","\""))
        fileObject.write('\n')
    fileObject.close()

def main():
    load_list_tmp = []
    path = os.getcwd()+'\\data\\'
    with open(path+'jiankong_list.txt') as f:
        lines = f.read().split('\n')

        for line in lines:
            tmp = line.split(' ')[0]
            load_list_tmp.append(tmp)

    load_list = list(set(load_list_tmp))

    for i in range(len(load_list)):
        print(f'walking... now {load_list[i]}')
        processing(load_list[i])

if __name__ == '__main__':
    main()