from ytmusicapi import YTMusic
from pprint import pprint

ytmusic = YTMusic()

yt = YTMusic()
results = yt.search("Sex & Drugs by Temper city",  filter="songs")

pprint(results)

# for result in results:
#     if result["artists"][0].get("name") == "Temper City":
#         pprint(result)
#     else:
#         pass



    
    