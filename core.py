import io
import re
import time
import subprocess

community = 'public'

#host = sys.argv[1]
#interfaces = sys.argv[2]
host = None
interfaces = None
index = None

iflist = []

# 查询指令
def snmpwalk(host, oid):
    cmd = 'snmpwalk -t 0.5 -v 2c -c ' + community + ' ' + host + ' ' + oid
    proc = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()

    out = io.TextIOWrapper(proc.stdout, encoding='utf-8')
    test = str(out.read())
    if test == '':
        result = ['IF-MIB::AgentAlive.1 = INTEGER: Timeout']
    else:
        result = test.split('\n')[:-1]
    return result

# 初始化接口描述表，写入存档文件
def initdescr(host):
    # 获取内容
    global iflist
    descroid = 'ifDescr'
    iflist = snmpwalk(host, descroid)
    return iflist

# 核心功能，分析接口信息
class searchinfomation(object):
    def __init__(self, host, interfaces,index):
        self.host = host
        self.interfaces = interfaces
        self.index = index

    # 获取交换机名称
    def getswitchname(self):
        sysnameoid = 'sysName'
        switchname = ':'.join(snmpwalk(self.host, sysnameoid)[0].split(':')[3:]).strip()
        return switchname

    # 获取接口真实名称、索引号与描述
    def analysisinterfaces(self,truename):
        #定义过滤正则表达式
        regexname = re.compile(r'STRING: ' + truename + '$' )
        alias_oid = 'ifAlias.'
        #
        for i in iflist:
            if re.search(regexname,i) != None:
                ifindex = re.sub('IF-MIB::ifDescr.','',i.split(' ')[0])
        ifalias_name =  ':'.join(snmpwalk(self.host, alias_oid+ifindex)[0].split(':')[3:]).strip()
        if ifalias_name == '':
            ifalias_name = 'No description'
        result = { 'ifIndex' : ifindex ,'ifDescr' : truename , 'ifAlisa' : ifalias_name}
        return result

    def watchupdown(self,ifindex):
        operstatus_oid = 'ifOperStatus.'
        ifstatus = ':'.join(snmpwalk(self.host, operstatus_oid+ifindex)[0].split(':')[3:]).strip()
        if ifstatus == 'up(1)' :
            status = 'UP'
        elif ifstatus == 'down(2)':
            status = 'Down'
        elif ifstatus == 'Timeout':
            status = 'Timeout'
        return status

class formattext(searchinfomation):
    def __init__(self,host,interfaces,index):
        searchinfomation.__init__(self,host,interfaces,index)

    def ifname(self):
        iforigin = self.interfaces
        if re.search('E', iforigin) != None:
            truename = re.sub('E', 'Ethernet', iforigin)
        elif re.search('G', iforigin) != None:
            truename = re.sub('G', 'GigabitEthernet', iforigin)
        elif re.search('T', iforigin) != None:
            truename = re.sub('T', 'Ten-GigabitEthernet', iforigin)
        elif re.search('F', iforigin) != None:
            truename = re.sub('F', 'FortyGigE', iforigin)
        return truename


if __name__ == '__main__':
    check = searchinfomation(host,interfaces,index)
    swname = check.getswitchname()
    ifName = check.analysisinterfaces()

    while True:
        ifstatus = check.watchupdown(ifName['ifIndex'])
        if ifstatus == 'Down':
            print(f'{swname} - {ifName["ifDescr"]} ({ifName["ifAlisa"]}) ----> {ifstatus}')
        time.sleep(3)
