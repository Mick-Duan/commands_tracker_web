#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################
# Contact:
#  mick.duan@chinanetcloud.com
##############################

##############################
# CHANGELOG
# Jun 10, 2013  MD: * Initial create
##############################


import os.path
import web
import commands
import view
import config
import urllib2
from view import render
from web import form
#import render

urls = (
    '/', 'index',
    '/search', 'search',
    '/nginxupstream', 'nginxupstream',
    '/monitor-check','zabbixcheck'
)

#class index:
#    def GET(self):
#        return render.base(page='', title='ChinaNetCloud Command Track')

class index:
    formdate = form.Form(form.Dropdown(name='date_name',args=[]))
    formname = form.Form(form.Dropdown(name='server_name',args=[]))
    def GET(self):
            optionsdate = config.DB.select('date',what='date_name',group='date_name',order='date_name DESC')
            optionsname = config.DB.select('name',what='server_name',group='server_name')
            idate = self.formdate()
            iname = self.formname()
            idate.date_name.args = [(o.date_name, o.date_name) for o in optionsdate]
            iname.server_name.args = [(o.server_name, o.server_name) for o in optionsname]
            return render.base(idate,iname,page='')
 #           return render.form(idate,iname)

def notfound():
    return web.notfound('''Sorry, the page you were looking for was not found.</br> You can connect Mick''')

class search:
    formdate = form.Form(form.Dropdown(name='date_name',args=[]))
    formname = form.Form(form.Dropdown(name='server_name',args=[]))
    def GET(self):
        optionsdate = config.DB.select('date',what='date_name',group='date_name',order='date_name DESC')
        optionsname = config.DB.select('name',what='server_name',group='server_name')
        idate = self.formdate()
        iname = self.formname()
        idate.date_name.args = [(o.date_name, o.date_name) for o in optionsdate]
        iname.server_name.args = [(o.server_name, o.server_name) for o in optionsname]
        cmd_search = web.input(date_name='',server_name='')
        cus_name=cmd_search.server_name.split('-')[-1]
        file = '/var/syslog-ng/cmd_hosts/' + cus_name + '/' + cmd_search.date_name + '/cmd_track.log' 
        if os.path.exists(file):
           file = open(file,'r').read()
        else:
           file  = 'None'
	a = render.cmd_track(cmd_search.date_name,cmd_search.server_name,file)
        return render.base(idate,iname,page=a)
#
class nginxupstream:
    formdate = form.Form(form.Dropdown(name='date_name',args=[]))
    formname = form.Form(form.Dropdown(name='server_name',args=[]))
    def GET(self):
            optionsdate = config.DB.select('date',what='date_name',group='date_name',order='date_name DESC')
            optionsname = config.DB.select('name',what='server_name',group='server_name')
            idate = self.formdate()
            iname = self.formname()
            idate.date_name.args = [(o.date_name, o.date_name) for o in optionsdate]
            iname.server_name.args = [(o.server_name, o.server_name) for o in optionsname]
            nginx_search = web.input(nginx_name='')
            status_page = '''http://''' + nginx_search.nginx_name + '''/status'''
            cmd = ''' wget -q -t 2 --timeout=2  ''' + status_page + ''' -O - |awk 'NR > 7 { print }'|grep -v '</body>'|grep -v '</html>' '''
            i = commands.getoutput(cmd)
            b = render.nginx_upstream(nginx_search.nginx_name,i)
            return render.base(idate,iname,page=b)

class zabbixcheck:
#    myform = form.Form(
#         form.Textbox('bosdfafdse'),
#         form.Textbox("bax", 
#             form.notnull,
#             form.regexp('\d+', 'Must be a digit'),
#             form.Validator('Must be more than 5', lambda x:int(x)>5)),
#         form.Textarea('moe'),
#         form.Checkbox('curly'), 
#         form.Dropdown('french', ['mustard', 'fries', 'wine'])
#    )
    def GET(self): 
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        pro_all_file = open('/var/www/sites/cmd-webpy/templates/all_process.list','r')
        pro_not_file = open ('/var/www/sites/cmd-webpy/templates/not_monitor_list.txt','r')
        not_monitor_server_file = open ('/var/www/sites/cmd-webpy/templates/not_monitor_server_list.txt','r')
        pro_not = pro_not_file.read()
        pro_all = pro_all_file.read()
        not_monitor_server = not_monitor_server_file.read()
        pro_all_file.close()
        pro_not_file.close()
        not_monitor_server_file.close()
        
        #pro_not = commands.getoutput(''' cat /var/www/sites/cmd-webpy/templates/all_process.list ''')
        return render.zabbixcheck(pro_not,pro_all,not_monitor_server)


if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.notfound = notfound
    app.run()
