import sqlite3 as lite
import nba_py
import sys
import nba_py
from nba_py import player
from nba_py import game
import csv

plist = nba_py.player.PlayerList(league_id='00', season='2017-18', only_current=1)
p_df = plist.info()
p_dict = p_df.T.to_dict().values()
counter = 0
stats = ["GP","MIN","PTS","REB","AST","STL","BLK","OREB","DREB","FG3M","FG3A","FTM","FTA","FG_PCT","FG3_PCT","FT_PCT"]
advstat = ["Id","Name","GP","PER","TS","TPAr","FTr","ORBr","DRBr","TRBr","ASTr","STLr","BLKr","TOVr","USGr","OWS","DWS","WS","WSr","OBPM", "DBPM","BPM","VORP","YR"]
con = lite.connect('user.db')
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Players(Id INT, Name TEXT, GP INT,PER REAL, TS REAL, TPAr REAL, FTr REAL, ORBr REAL, DRBr REAL, TRBr REAL, ASTr REAL, STLr REAL, BLKr REAL, TOVr REAL, USGr REAL, OWS REAL, DWS REAL, WS REAL, WSr REAL, OBPM REAL, DBPM REAL, BPM REAL, VORP REAL, YR REAL)")
    for player in p_dict:
        name = player['DISPLAY_FIRST_LAST']
        id = player['PERSON_ID']
        # Getting year by year splits and condensing it into a string
        pprof = nba_py.player.PlayerYearOverYearSplits(player_id=id)
        json = pprof.json
        headers = json['resultSets'][0]['headers']
        results = json['resultSets'][1]['rowSet']
        p = ""
        for r in results:
            p = p + str(r[1]) + ","
            for s in stats:
                i = headers.index(s)
                p = p + str(r[i]) + ","
        # Getting advanced stats (2017-18)
        adv_headers = []
        adv_stats = []
        with open('adv.csv') as csvfile:
            nbalist = csv.reader(csvfile)
            i = 0
            for row in nbalist:
                if i==0:
                    for h in row:
                        adv_headers.append(h)
                else:
                    name2 = row[1]
                    name2 = name2.split("""\\""")[0]
                    if name2 == name:
                        for s in row:
                            adv_stats.append(s)
                i = i + 1
        #print adv_stats
        #print adv_headers
        print name

        #print len(adv_stats)
        #print p

        if len(adv_stats) == 0:
            #print name
            adv_stats = []
            #print "Alexis AJJ"
            for t in range(30):
                adv_stats.append(0)
        else:
            print adv_stats[5]
        #print len(adv_stats)
        cur.execute("insert into Players values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (str(counter),name,adv_stats[5],adv_stats[7],adv_stats[8],adv_stats[9],adv_stats[10],adv_stats[11],adv_stats[12],adv_stats[13],adv_stats[14],adv_stats[15],adv_stats[16],adv_stats[17],adv_stats[18],adv_stats[20],adv_stats[21],adv_stats[22],adv_stats[23],adv_stats[25],adv_stats[26],adv_stats[27],adv_stats[28],p))
        counter = counter + 1
