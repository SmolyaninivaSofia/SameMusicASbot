
import initSongs as init
import config as c
import math

conn = c.conn
getsongList=[]
#insert to database data from json files
def preInsert():
    songs = init.getSongs()
    for song in songs:
        cur = conn.cursor()
        cur.execute("""SELECT count(*) FROM song;""")
        track_id = cur.fetchall()[0][0] + 1
        row = (track_id, song[0], song[1], ','.join(song[2]))
        Insert(row)
        print('update ',track_id )

#insert row to database
def Insert(row):
    cur = conn.cursor()
    cur.execute("""INSERT INTO song (track_id, artist, title,tags) VALUES (%s,%s,%s,%s);""", row)
    conn.commit()
#select all songs from database
def SelectGet():
    cur = conn.cursor()
    cur.execute("""SELECT * FROM song;""")
    rows = cur.fetchall()
    for r in rows:
        tag_list=r[3].split(',')
        getsongList.append((r[0],r[1],r[2],tag_list))
    return  getsongList

#update list of similar songs
def UpdateSimilars(sim,song):
    cur = conn.cursor()
    cur.execute("""UPDATE song SET similars=%s WHERE track_id=%s;""",(sim,song) )
    conn.commit()
    print('update ',song)

#delete songs with no similar songs
def DeleteBadSongs(song):
    cur = conn.cursor()
    cur.execute("""DELETE FROM song  WHERE track_id=%s;""",(song,))
    conn.commit()
    print('delete ', song)
#insert songs with no similar songs to another table
def InsertBadSongs(song):
    cur = conn.cursor()
    cur.execute("""INSERT INTO badsong SELECT track_id,artist,title,tags FROM song WHERE track_id=%s;""",(song,))
    conn.commit()
    print('insert ', song)

#get list of similar songs
def SelectSimilars(song):
    song=song.lower()
    cur = conn.cursor()
    cur.execute("""SELECT similars FROM song WHERE lower(artist||'-'||title)=%s;""",(song,))
    row = cur.fetchall()
    if len(row) != 0:
        sim_list = row[0][0].split(',')
        same_song_list=[]
        for s in sim_list:
            cur.execute("""SELECT artist||'-'||title FROM song WHERE track_id =%s;""", (int(s),))
            same_song_list.append(cur.fetchall())
        res=''
        num=1
        for same_song in same_song_list:
            res+=str(num)+'. '+same_song[0][0]+'\n'
            num+=1
    else:
        res=''
    return res

def Add(user_id, song):
    ind = song.find('-')
    indd = song.find(':')
    if (ind < 0 or indd < 0):
        return 1
    else:
        tags = song[indd + 1:len(song)]
        if tags == '':
            return 1
        artist = song[0:ind].lower()
        title = song[ind + 1:indd].lower()
        song = song[0:indd].lower()
        taglist = tags.split(',')
        cur = conn.cursor()
        cur.execute("""SELECT * FROM badsong WHERE lower(artist||'-'||title)=%s;""", (song,))
        row = cur.fetchall()
        if (len(row) == 0):
            cur = conn.cursor()
            cur.execute("""SELECT max(track_id) FROM song;""")
            track_id = cur.fetchall()[0][0] + 1
            cur = conn.cursor()
            cur.execute("""SELECT max(track_id) FROM badsong;""")
            track_id = max(cur.fetchall()[0][0] + 1,track_id)
            list = []
            for tag in taglist:
                list.append(math.exp(1))
            cur = conn.cursor()
            cur.execute("""INSERT INTO badsong (track_id, artist, title,tags,tag_count,user_count) VALUES (%s,%s,%s,%s,%s,%s);""",(track_id, artist, title, tags, list, user_id))
            conn.commit()
            return 0
        else:
            if not (row[0][5] is None) and (row[0][5].find(','+str(user_id)) >= 0 or row[0][5]==str(user_id)):
                return(2)
            else:
                if not (row[0][5] is None):
                    user_id_list = str(row[0][5]) + ',' + str(user_id)
                else:
                    user_id_list = str(user_id)
                track_id = row[0][0]
                tab_tagss = row[0][3]
                list = row[0][4].lstrip('{').rstrip('}').split(',')
                tab_tags = tab_tagss.split(',')
                for t in taglist:
                    try:
                        t=t.strip(' ')
                        i = tab_tags.index(t)
                        list[i] = math.exp(math.log(float(list[i])) + 1)
                    except ValueError:
                        tab_tagss += ',' + t
                        list.append(math.exp(1))
                cur = conn.cursor()
                cur.execute("""UPDATE badsong SET tags=%s, tag_count=%s, user_count=%s WHERE track_id=%s;""",(tab_tagss, list, user_id_list, track_id))
                conn.commit()
                return 0






