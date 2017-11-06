import json
import os

fileList = []

def analyze_tags():
    untagged_count=0
    diff_tags=set()
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            if data['tags'] == []:
                untagged_count += 1
            else:
                for tag in data['tags']:
                    diff_tags.add(tag[0])
    print(untagged_count)
    print(len(diff_tags))

def analyze_artists():
    diff_artists=set()
    for file in fileList:
        with open(file) as data_file:
            data = json.load(data_file)
            diff_artists.add(data['artist'])
    print(len(diff_artists))


directory =os.walk('lastfm_subset')
for d,dir,files in directory:
    for file in files:
        path=os.path.join(d, file)
        fileList.append(path)


for file in fileList[0:5]:
    with open(file) as data_file:
        data = json.load(data_file)
    print(data['artist'])
    print(data['title'])
    print(data['track_id'])
    for tag in data['tags']:
       print(tag[0])
       print(tag[1])
    print('-----------------------------------------------------------------')