import BDConn as bd
import math
import initSongs as init

songs=bd.SelectGet()
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
            if sims.get(song[0]) is None:
                sims[song[0]]={item[0]:res}
            else:
                sims[song[0]].update({item[0]:res})



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
                count5 += 1
        if (count5==0):
            badsongs+=1
            badsongslist.append(item)
    for bad in badsongslist:
        bd.InsertBadSongs(bad)
        bd.DeleteBadSongs(bad)

def calcSimsAndWriteInDB():
    for song in songs:
        sim(song)
    for item in sims:
        rates=sorted(sims[item].items(),key=lambda x: x[1], reverse=True)[:10]
        s =[]
        for r in rates:
            if r[1]>0.16:
                s.append(str(r[0]))
        list_sim=(','.join(s))
        bd.UpdateSimilars(list_sim,item)

#findbadsongs()