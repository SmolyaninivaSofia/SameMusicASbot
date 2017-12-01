
import initSongs as init
import config as c

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
        res='List of songs simmilar to '+song.upper()+'\n'+res
    else:
        res="Sorry...This song have no simmilars :( \nOr you can make a mistake"
    return res








