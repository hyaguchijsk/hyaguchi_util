#!/usr/bin/env python

import sys,os,getopt,re,time,datetime,locale

def read_history(user,shell,histfile,year=None,month=None,day=None):
    if os.path.exists(histfile):
        re_tm=re.compile(r"^#\+(\d+)")
        st_tm=None
        f=open(histfile)
        line=f.readline().strip()

        today=datetime.datetime.today()
        t_year=int(today.year)
        t_month=int(today.month)
        t_day=int(today.day)
        if year and month and day:
            t_year=year
            t_month=month
            t_day=day

        com_list={}
        while line:
            re_res = re_tm.match(line)
            if re_res:
                st_tm=time.localtime(int(re_res.group(1)))
            elif st_tm:
                com=line.split()[0]
                if com.find("/")!=-1:
                    com="exec"
                if((t_year==st_tm.tm_year) and (t_month==st_tm.tm_mon) and (t_day==st_tm.tm_mday)):
                    if com_list.get(com):
                        com_list[com]=com_list[com]+1;
                    else:
                        com_list[com]=1;
                st_tm=None
            line=f.readline().strip()
        f.close()

        print user + "'s " + shell + " command ranking" + " on " + str(t_year) + "/" + str(t_month) + "/" + str(t_day) + " :",
        sorted_com_list=sorted(com_list.items(), key=lambda x:x[1], reverse=True)
        for i in range(4):
            cc,nn=sorted_com_list[i]
            print cc + " * " + str(nn) + ",",
        cc,nn=sorted_com_list[4]
        print cc + " * " + str(nn)
    else:
        print >>sys.stderr, "file not found: " + histfile

if __name__=="__main__":
    args=sys.argv

    opts,args = getopt.getopt(args[1:],"",["shell","histfile"])

    shell_full=os.environ.get("SHELL").split("/")
    shell=shell_full[len(shell_full)-1]
    histfile=os.environ.get("HOME") + "/." + shell + "_history"
    for opt,val in opts:
        if opt == "--shell":
            shell=val
        if opt == "--histfile":
            histfile=val

    read_history(os.environ.get("USER"),shell,histfile)
            
