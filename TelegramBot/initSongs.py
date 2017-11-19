import json
import os

fileList = []
resSongs=[]

#recommended call:
#songs=getSongs() - write this songs list to database

def findFiles():
    directory =os.walk('lastfm_subset')
    for d,dir,files in directory:
        for file in files:
            path=os.path.join(d, file)
            fileList.append(path)

def fillTags(tags):
    resTags=[]
    for tag in tags:
       if (int(tag[1])) >= 50:
           resTags.append(tag[0])
    return resTags


def getSongs():
    findFiles()
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            if data['tags'] != []:
                tags=data['tags']
                tt=fillTags(tags)
                if len(tt)>2:
                    resSongs.append((data['artist'], data['title'], data['track_id'], tt))
    print("getSongs finished")
    return resSongs
