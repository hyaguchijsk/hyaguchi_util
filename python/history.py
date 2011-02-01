#!/usr/bin/env python

import sys,os,getopt,re,time,datetime,locale
import tweet

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
                line_split=line.split()
                com=line_split[0]
                if com=="sudo" and len(line_split)>2:
                    com=line_split[1]
                if com.find("/")!=-1:
                    com="[exec]"
                if((t_year==st_tm.tm_year) and (t_month==st_tm.tm_mon) and (t_day==st_tm.tm_mday)):
                    if com_list.get(com):
                        com_list[com]=com_list[com]+1;
                    else:
                        com_list[com]=1;
                st_tm=None
            line=f.readline().strip()
        f.close()

        com_num=len(com_list)
        if com_num==0:
            print >>sys.stderr, "blank history."
            return ""
        else:
            #print user + "'s " + shell + " command ranking" + " on " + str(t_year) + "/" + str(t_month) + "/" + str(t_day) + " :",
            retstr = user + "'s " + shell + " command ranking" + " on " + str(t_year) + "/" + str(t_month) + "/" + str(t_day) + " : "
            com_num = com_num if com_num<5 else 5

            if com_num==1:
                cc,nn=sorted_com_list[0]
                #print cc + " * " + str(nn)
                retstr = retstr + cc + " * " + str(nn)
            else:
                sorted_com_list=sorted(com_list.items(), key=lambda x:x[1], reverse=True)
                for i in range(com_num-1):
                    cc,nn=sorted_com_list[i]
                    #print cc + " * " + str(nn) + ",",
                    retstr = retstr + cc + " * " + str(nn) + ", "
                cc,nn=sorted_com_list[com_num-1]
                #print cc + " * " + str(nn)
                retstr = retstr + cc + " * " + str(nn)
            return retstr
    else:
        print >>sys.stderr, "file not found: " + histfile
        return ""

if __name__=="__main__":
    args=sys.argv

    opts,args = getopt.getopt(args[1:],"",["shell","histfile","tweet"])

    shell_full=os.environ.get("SHELL").split("/")
    shell=shell_full[len(shell_full)-1]
    histfile=os.environ.get("HOME") + "/." + shell + "_history"
    istweet=False
    for opt,val in opts:
        if opt == "--shell":
            shell=val
        elif opt == "--histfile":
            histfile=val
        elif opt == "--tweet":
            istweet=True

    retstr = read_history(os.environ.get("USER"),shell,histfile)
    if retstr != "":
        print retstr
        if istweet:
            tweet.tweetstring(retstr)
