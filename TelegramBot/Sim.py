import initSongs as s
import math

songs=s.getSongs()
sims={}
badsongslist=[]

#recommended call:
#findbadsongs()
#do something with song in badsongslist - list of keys in sims (I recommend track_id)
#calcSimsAndWriteInDB()

#find similiars for song
def sim(song):
    for item in songs:
        sum=0
        if item!=song:
            #intersection
            mpsitag=0
            for stag in song[3]:
                for itag in item[3]:
                   if stag==itag:
                        mpsitag+=1
                        break
            #coefficient Jakkara
            res=mpsitag/(len(song[3])+len(item[3])-mpsitag)
            #song[0]+" "+song[1] need to change for song_id
            #item[0]+" "+item[1] need to change for item_id
            if sims.get(song[0]+" "+song[1]) is None:
                sims[song[0]+" "+song[1]]={item[0]+" "+item[1]:res}
            else:
                sims[song[0]+" "+song[1]].update({item[0]+" "+item[1]:res})



#run sim function for all songs and find count and song witch has no similiar
# we need get the id and delete these song from database (they hav not got similliars in our dataset)
# or we can put them in buffer (we will keep useradd songs)
def findbadsongs():
    badsongs=0
    print(len(songs))
    for song in songs:
        sim(song)
    for item in sims:
        rates=sorted(sims[item].items(),key=lambda x: x[1])
        rates=rates[len(rates)-10:len(rates)]
        count5=0
        for r in rates:
            if r[1]>0.16:
                #0.5 17..
                #0.1 106
                #0.15 271
                #0.16 292
                #0.17 412
                #0.175 414
                #0.2 664
                count5 += 1
        if (count5==0):
            badsongs+=1
            badsongslist.append(item)
    print(badsongs)

def calcSimsAndWriteInDB():
    for song in songs:
        sim(song)
    for item in sims:
        rates=sorted(sims[item].items(),key=lambda x: x[1])
        rates=rates[len(rates)-10:len(rates)]
        for r in rates:
            if r[1]>0.16:
                #change for write in db, where item - first song id, r[0] second song id, r[1] coefficient of sim
                print(item,r[0],r[1])
