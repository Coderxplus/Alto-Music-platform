from ytmusicapi import YTMusic

from pprint import pprint





def get_home():
    results = []
    with  YTMusic() as ytmusic:
        request = ytmusic.search("Popular songs",  filter="songs")
        

        for data in request:
                response = {
                    "video_id": data.get("videoId"),
                    "title": data.get("title"),
                    "artists": data.get("artists"),
                    "album": data.get("album"),
                    "duration": data.get("duration"),
                    "thumbnail": data.get("thumbnails"),
                    "category": data.get("category")

                }

                results.append(response)
    return results

def search_song(song):
    results = []
    with  YTMusic() as ytmusic:
        request = ytmusic.search(song,  filter="songs")

        

        for data in request:
            response = {
                "video_id": data.get("videoId"),
                "title": data.get("title"),
                "artists": data.get("artists"),
                "album": data.get("album"),
                "duration": data.get("duration"),
                "thumbnail": data.get("thumbnails"),
                "category": data.get("category")

            }

            results.append(response)

    return results



    
home = get_home()
print()