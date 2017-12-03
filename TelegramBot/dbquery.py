import config as c
import math

conn=c.conn

tags='indie,acoustic,experimental,beautiful,Lo-Fi,deep,weird voice,all the best,pure genius,seriously amazing,of christmas past,best songs of the 80s,friendsofthekingofrummelpop,cry'
list=[]
cur = conn.cursor()
cur.execute("""UPDATE badsong SET user_count=%s WHERE track_id=%s;""",(None,2178))
conn.commit()

song='Daniel Johnston-The Story of an Artist: cry'
ind=song.find('-')
user_id=4
indd = song.find(':')
if (ind<0 or indd<0):
    print(1)
else:
    artist=song[0:ind].lower()
    title=song[ind+1:indd].lower()
    tags = song[indd + 1:len(song)]
    if tags=='':
        print(1)
    song=song[0:indd].lower()
    taglist = tags.split(',')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM badsong WHERE lower(artist||'-'||title)=%s;""", (song,))
    row = cur.fetchall()
    print(row)
    if (len(row)==0):
        cur = conn.cursor()
        cur.execute("""SELECT max(track_id) FROM song;""")
        track_id = cur.fetchall()[0][0] + 1
        list = []
        for tag in taglist:
            list.append(math.exp(1))
        cur = conn.cursor()
        cur.execute("""INSERT INTO badsong (track_id, artist, title,tags,tag_count,user_count) VALUES (%s,%s,%s,%s,%s,%s);""", (track_id ,artist ,title,tags,list,user_id))
        conn.commit()
    else:
        if row[0][5] is None or row[0][5].find(str(user_id)+',')<0:
            if not (row[0][5] is None):
                user_id_list=str(row[0][5])+','+str(user_id)
            else:
                user_id_list = str(user_id)
            track_id = row[0][0]
            tab_tagss=row[0][3]
            list=row[0][4].lstrip('{').rstrip('}').split(',')
            tab_tags=tab_tagss.split(',')
            for t in taglist:
                try:
                    i=tab_tags.index(t)
                    list[i]=math.exp(math.log(float(list[i]))+1)
                except ValueError:
                    tab_tagss+=','+t
                    list.append(math.exp(1))
            cur = conn.cursor()
            cur.execute( """UPDATE badsong SET tags=%s, tag_count=%s, user_count=%s WHERE track_id=%s;""",(tab_tagss,list,user_id_list,track_id))
            conn.commit()
        else:
            print(2)
cur = conn.cursor()
cur.execute("""SELECT * FROM badsong WHERE lower(artist||'-'||title)=%s;""", (song,))
row = cur.fetchall()
print(row)