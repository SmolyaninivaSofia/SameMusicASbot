import ParseJSON as p
import math

songs=p.getSongs()
sims={}

#find similiars for song
def sim(song):
    for item in songs:
        sum=0
        if item!=song:
            for stag in song[3]:
                for itag in item[3]:
                    if stag[0]==itag[0]:
                        s=0.01*int(stag[1])
                        i=0.01*int(itag[1])
                        sum+=(1-math.fabs(s-i))
                        break
            res=sum/(len(song[3]))
            if res>1:
                print('sum ',res,song)
            sims[item[0]+item[1]]=res
#run sim function for all songs and find count and song witch has no similiar
badsongs=0
for song in songs:
    sim(song)
    srates=sorted(sims.items(),key=lambda x: x[1])
    srates=srates[len(srates)-10:len(srates)]
    count75=0
    count5=0
    for item in srates:
        if item[1]>0.75:
            count75+=1
        if item[1]>0.5:
            count5 += 1
    if (count5==0):
        badsongs+=1
        print('count ',song)
print(badsongs)