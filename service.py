from ytmusicapi import YTMusic

from pprint import pprint

ytmusic = YTMusic()

yt = YTMusic()


def search_song(song):
    request = yt.search(song,  filter="songs")

    results = []

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


# query = "Way less sad"

# print(f"Searching for {query} ....")
# pprint(search_song(query))

# for result in results:
#     if result["artists"][0].get("name") == "Temper City":
#         pprint(result)
#     else:
#         pass



    
    