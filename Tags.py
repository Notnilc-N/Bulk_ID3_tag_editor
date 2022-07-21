from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
from mutagen.easyid3 import EasyID3FileType
import os
from os import listdir

fileextension = "m4a"

def set_artist(filename, description):
    if fileextension == "m4a":
        tags = MP4(filename).tags
    elif fileextension == "mp3":
        tags = EasyID3FileType(filename)
    # tags["aART"] = description
    # tags.save(filename)
    try: # this is to check whether filename's tag is equal to description
        tag1 = tags["aART"][0]
        tag2 = tags["©ART"][0]
    except:
        tag1 = ":" #: is an invalid character, so the tag1 != description will always be wrong.
        tag2 = ":"
    
    if tag1 != description or tag2 != description:
        # print("artist: " + description)
        if fileextension == "m4a":
            tags["aART"] = description
            tags["©ART"] = description
        else:
            tags["artist"] = description
            tags["albumartist"] = description
        tags.save(filename)
    else:
        raise Exception

def set_title(filename, description):
    if fileextension == "m4a":
        tags = MP4(filename).tags
    elif fileextension == "mp3":
        tags = EasyID3FileType(filename)
    # tags["©nam"] = description
    # tags.save(filename)
    try:
        tag = tags["©nam"][0]
    except:
        tag = ":"
    if tag != description:
        # print("title: " + description)
        if fileextension == "m4a":
            tags["©nam"] = description
        else:
            tags["title"] = description
        tags.save(filename)
    else:
        raise Exception

def list_files(directory, extension):
    return (f for f in listdir(directory) if f.endswith('.' + extension))

dir = os.getcwd()
songs = list(list_files(dir, fileextension))

failslist = ["------------------------------------------------------------------","SET FAILS:"]

for song in songs:
    #song = songs[0]
    # try:
    #     tags = EasyID3FileType(song)
    #     artist = tags["artist"][0]
    #     title = tags["title"][0]
    #     # tags["tracknumber"] = ""    #delete tracknumber
    #     # tags["discnumber"] = ""     #delete discnumber
    #     # tags["album"] = ""          #delete album
    #     # tags.save(song)
    #     try:
    #         os.rename(dir + "\\" + song, artist + ' - ' + title + '.' + fileextension)
    #     except:
    #         print("rename fail:___________" + artist + "|" + title)
    # except:
    #     print("big fail:___________" + artist + "|" + title)
    check = True
    if "- " in song:
        ssplit = song.split('- ')
        artist = ssplit[0]
        title = ssplit[1]
    elif "– " in song:
        ssplit = song.split('– ')
        artist = ssplit[0]
        title = ssplit[1]
    elif "-" not in song:
        check = False
    artist = artist[:len(artist)-1]
    title = title[:-4]
    if artist[:20] == "David Dean Burkhart ":
        artist = artist[20:]
    if artist[:10] == "jock barr ":
        artist = artist[10:]
    if artist[:10] == "Polipoli8 ":
        artist = artist[10:]
        bracketindex = title.index('(') - 1
        title = title[:bracketindex]
    if artist[:20] == "Adventures In Sound ":
        artist = artist[20:]
        title = title[:-7]
    if artist[:16] == "WorthikidsMusic ":
        artist = "Worthikids"
    if artist[:15] == "alona chemerys ":
        artist = artist[15:]
    if artist[:16] == "Bill McClintock ":
        artist = "Bill McClintock"
        title = title[1:-1]
    if title[:6] == "Topic ":
        title = title[6:]
    bracketsplit = len(title.split('('))
    if bracketsplit == 2:
        remaster_index = title.find('Remaster')
        if remaster_index != -1:
            bracket_index = title.find('(') - 1
            title = title[:bracket_index]
    if bracketsplit == 3:
        remaster_index = title.find('Remaster')
        if remaster_index != -1:
            bracket_index = title.find(')') + 1
            title = title[:bracket_index]
    print(artist + "|" + title)

    renamecheck = 0
    if check:
        try :
            set_artist(song, artist)
        except :
            failslist.append("set_artist repeat:___________" + artist + "|" + title)
            renamecheck += 1
        try :
            set_title(song, title)
        except :
            failslist.append("set_title repeat:_______________" + artist + "|" + title)
            renamecheck += 1
        if renamecheck > 0:
            try :
                os.rename(dir + "\\" + song, artist + ' - ' + title + '.' + fileextension)
            except :
                print("renamefail_______________________________________" + artist + "|" + title)

for fails in failslist:
    print(fails)