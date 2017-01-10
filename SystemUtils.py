# @Author: Thierry Rangeard <Gandalf>
# @Date:   06-Jan-2017
# @Email:  trangeard@net-online.fr
# @Project: BotApi telegram
# @Last modified by:   Gandalf
# @Last modified time: 07-Jan-2017

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Alex -*-

from ServerInfo import ServerInfo
import os
import platform
import subprocess
import httplib
import requests


class SystemUtils(object):
    def get_info_from_server(self, command_info):
        if command_info == "/info":
            info = ServerInfo()
            info.local_distributive = platform.architecture()
            info.local_architecture = platform.linux_distribution()
            info.local_hostname = platform.uname()[1]
            info.local_os = platform.uname()[0]
            info.local_kernel = platform.release()
        else:
            print "Debug message: nothing to do :&("
        return info

    def get_load_from_from_server(self, command_load):
        if command_load == "/load":
            load_average = os.getloadavg()
            load_average = "Current load: " + str(load_average)
        else:
            print "Debug message: nothing to do :&("
        return load_average

    def get_memory(self, command_memory):
        if command_memory == "/memory":
            with open('/proc/meminfo', 'r') as mem:
                ret = {}
                tmp = 0
                for i in mem:
                    sline = i.split()
                    if str(sline[0]) == 'MemTotal:':
                        ret['total'] = int(sline[1])
                    elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                        tmp += int(sline[1])
                ret['free'] = tmp
                ret['used'] = int(ret['total']) - int(ret['free'])
                mem = "Memory info: " + str(ret)
        else:
            print "Debug message: nothing to do :&("
        return mem

    def restart_apache(self, restart_apache):
        restart = "/etc/init.d/httpd restart"
        if restart_apache == "/apache_restart":
            process = subprocess.Popen(restart.split(), stdout=subprocess.PIPE)
            output = "Apache restarted: \n" + process.communicate()[0]
        else:
            print "Debug message: nothing to do :&("
        return output

    def get_status_online(self, online_status):
        host = "espaceprojets.net"
        if online_status == "/check_site_status":
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", "/")
            r1 = conn.getresponse()
            status = "Vibe status: " + str(r1.status) + " " + str(r1.reason)
        else:
            print "Debug message: nothing to do :&("
        return status

    def restart_mysqld(self, restart_mysql):
        restart = "/etc/init.d/mysqld restart"
        if restart_mysql == "/mysql_restart":
            process = subprocess.Popen(restart.split(), stdout=subprocess.PIPE)
            output = "MySQL restarted: \n" + process.communicate()[0]
        else:
            print "Debug message: nothing to do :&("
        return output

    def get_automatic_site_status(self):

        host = "filr.net-online.fr"
        url = "https://api.telegram.org/bot244202552:AAF3Q_Ue4R6gI3g1wb_1AvBft9sVwVtio08/sendMessage"
        down = "Site filr is Down"

        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", "/")
        site_status = conn.getresponse().status
        status_final = str(site_status)

        if status_final != "200":
            print status_final
            requests.post(url, data={'chat_id': 317612641, 'text': str(down)})


SystemUtils("/info")
