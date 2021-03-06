# -*- coding: utf-8 -*-

from databaseHandler import DB_Handler,DataBaseHandler
import time

CMD_UPDATE_DEV_USER     = 'DATA UPDATE USERINFO'
CMD_DEL_DEV_USER        = 'DATA DELETE USERINFO'
CMD_QUERY_DEV_USER      = "DATA QUERY USERINFO"
CMD_QUERY_DEV_ATTLOG    = 'DATA QUERY ATTLOG'
CMD_DEV_INFO            = 'INFO'
CMD_DEV_CHECK           = 'CHECK'
CMD_CLEAR_DEV_ATTLOG    = 'CLEAR LOG'
CMD_CLEAR_DEV_ALL       = 'CLEAR DATA'
CMD_SET_DEV_OPTION      = 'SET OPTION'
CMD_GET_NEW_LOG         = 'LOG'


CMD_NOT_SEND    = 1
CMD_IN_SENDING  = 2
CMD_HAS_SEND    = 3
CMD_EXC_FAIL    = 4

class CMD_Engine() :
    cmd_line_buf = {}
    cmdIds = 0

    def __init__(self,sn):
        self.db_handler = DB_Handler
        self.sn = sn

    def genCmd_update_user(self,infor):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s PIN=%s\tName=%s\tPri=%s\tCard=%s\n" %
                          (self.cmdIds,CMD_UPDATE_DEV_USER,infor['PIN'],infor['Name'],infor['Pri'],
                           infor['Card']))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND}
        print(cmd_line)
        print("Name def:", infor['Name'].encode())
        print("Name gbk:", infor['Name'].encode('gbk'))
        print("Name utf-8:", infor['Name'].encode('utf-8'))

    def genCmd_delet_user(self,infor):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s PIN=%s\n" % (self.cmdIds,CMD_DEL_DEV_USER,infor['PIN']))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_query_user(self,pin):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s PIN=%s\n" % (self.cmdIds,CMD_QUERY_DEV_USER,pin))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_query_log(self,startTime,endTime):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s StartTime=%s\tEndTime=%s\n" % (self.cmdIds,CMD_QUERY_DEV_ATTLOG,startTime,endTime))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)
        return self.cmdIds

    def genCmd_dev_info(self):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s\n" % (self.cmdIds, CMD_DEV_INFO))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_check(self):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s\n" % (self.cmdIds, CMD_DEV_CHECK))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_clear_attLog(self):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s\n" % (self.cmdIds, CMD_CLEAR_DEV_ATTLOG))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_clear_dataAll(self):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s\n" % (self.cmdIds, CMD_CLEAR_DEV_ALL))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def genCmd_get_new_log(self):
        self.cmdIds += 1
        cmd_line = format("C:%03d:%s\n" % (self.cmdIds, CMD_GET_NEW_LOG))
        self.cmd_line_buf[self.cmdIds] = {'cmd':cmd_line,'state':CMD_NOT_SEND,'timestamp':time.time()}
        print(cmd_line)

    def get_genCmd_lines(self):
        count = 0;
        cmds = []
        for (k,v) in self.cmd_line_buf.items():
            if v['state'] == CMD_NOT_SEND :
                cmds.append(v['cmd'])
                v['state'] = CMD_IN_SENDING
                count += 1
            if count > 99 :
                break
        return cmds

    def response_cmd_line(self,response):
        print(response)
        if  response['cmdIds'] in self.cmd_line_buf :
            if(response['state'] == 0 ) :
                self.cmd_line_buf[response['cmdIds']]['state'] = CMD_HAS_SEND
            else :
                self.cmd_line_buf[response['cmdIds']]['state'] = CMD_EXC_FAIL
                date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(cmd,response['timestamp']))
                record = {
                        'SN'  : self.sn,
                        'type': 'CMD_FAILED',
                        'content': format("%s ;return %d . %s" % (self.cmd_line_buf[response['cmdIds']].cmd,response['state'],date_time)),
                        'wTime': time.time()
                    }
                self.db_handler.add_error_log(record)

    def recycle_cmd_line(self):
        for (k,v) in self.cmd_line_buf.items() :
            if (v['state'] == CMD_HAS_SEND) or (v['state'] == CMD_EXC_FAIL):
                self.cmd_line_buf.pop(k)

        if len(self.cmd_line_buf) == 0:
            self.cmdIds = 0
            pass
