import config as c
import math

conn=c.conn

song='Twenty One Pilots-Lane Boy'
song=song.lower()
cur = conn.cursor()
cur.execute("""SELECT * FROM badsong WHERE lower(artist||'-'||title)=%s;""", (song,))
row = cur.fetchall()
print(row)