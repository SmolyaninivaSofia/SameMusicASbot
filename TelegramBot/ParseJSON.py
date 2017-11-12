import json
import os

fileList = []
needTags=[]
songs=set()
#Sofia, you need this list, it consist of coteges, it makes by getSongs() function
resSongs=[]

def findFiles():
    directory =os.walk('lastfm_subset')
    for d,dir,files in directory:
        for file in files:
            path=os.path.join(d, file)
            fileList.append(path)

def analyze_tags():
    untagged_count=0
    diff_tags=set()
    tags={}
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            if data['tags'] == []:
                untagged_count += 1
            else:
                for tag in data['tags']:
                    diff_tags.add(tag[0])
                    if tags.get(tag[0]) is None:
                        tags[tag[0]]=0
                    else:
                        tags[tag[0]]+=1
#    print(untagged_count)
#    print(len(diff_tags))
    tag_list=sorted(tags.items(),key=lambda x: x[1])
    for item in tag_list:
        if item[1]>100:
            needTags.append(item[0])

def analyze_artists():
    diff_artists=set()
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            diff_artists.add(data['artist'])
#    print(len(diff_artists))

def getTagsSongs():
    for file in fileList:
        counter=0
        with open(file) as data_file:
            data = json.load(data_file)
            for tag in data['tags']:
                for item in needTags:
                    if tag[0]==item:
                        counter+=1
                if counter>2:
                    songs.add(data['track_id'])
#    print(len(songs))

def chooseTags(tags):
    tt=[]
    for tag in tags:
        for item in needTags:
            if tag[0]==item:
                tt.append(tag)
    return tt

def getSongs():
    findFiles()
    analyze_tags()
    getTagsSongs()
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            for item in songs:
                if item==data['track_id']:
                    tt=chooseTags(data['tags'])
                    resSongs.append((data['artist'],data['title'],data['track_id'],tt))
                    break
    print("getSongs finished")
    return resSongs
