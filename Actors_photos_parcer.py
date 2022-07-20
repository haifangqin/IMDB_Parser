from unicodedata import name
import requests
import json
from bs4 import BeautifulSoup
import lxml
import os
import pandas as pd

domen = "https://www.imdb.com"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344"
}

try:
    name_list = []
    found_photos = []
    save_photos = []
    with open('JSON/hotstar_actors.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        actors_count = len(text)
        print(f"Number of actors in JSON = {actors_count}")
        for i in text:
            actor_name = i.get("name")
            actor_ID = i.get("ID")
            actor_href = domen+"/name/"+actor_ID
            actor_name = actor_name.replace(" ", "_")
            name_list.append(actor_ID)
            print(f"Let's start parsing the actor's photos: {actor_name}")

            # actor photo parsing
            req = requests.get(url=actor_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")


            # create a folder for storing photos with this actor
            folder_name = f"data/actors/{actor_name}_{actor_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            else:
                continue

            # create folder to store html with this actor
            folder_name = f"temp/actors/{actor_name}_{actor_ID}"
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Save the html page of this actor
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_page.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            # pass saved html file to BeautifulSoup
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_page.html", "r", encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")
            # we get a link to the album with all the photos
            try:
                all_photos_href = domen+soup.find("div", class_="mediastrip_container").find("div", class_="see-more").find("a").get("href")
            except:
                found_photos.append(0)
                save_photos.append(0)
                print('no photos for {}\n'.format(actor_ID))
                continue
            print(all_photos_href)

            # follow the new link to the album
            req = requests.get(url=all_photos_href, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            # save the html file with the actor's photo album
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_album.html", "w", encoding="utf-8") as file:
                file.write(req.text)

            # pass saved html file to BeautifulSoup
            with open(f"temp/actors/{actor_name}_{actor_ID}/{actor_name}_{actor_ID}_album.html", "r", encoding="utf-8") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")

            # сwe collect all links to photos in high resolution
            try:
                soup_photos_hrefs = soup.find("div", class_="media_index_thumb_list").find_all("a")
            except:
                found_photos.append(0)
                save_photos.append(0)
                print('no photos for {}\n'.format(actor_ID))
                continue
            # print(soup_photos_hrefs)
            list_photos_hrefs = []
            for href in soup_photos_hrefs:
                try:
                    big_photo_href = domen+href.get("href")
                    # populate the list with links
                    list_photos_hrefs.append(big_photo_href)
                except:
                    continue

            count = 0
            found_photos.append(len(list_photos_hrefs))
            print("Total photos found:" + str(len(list_photos_hrefs)))
            print(list_photos_hrefs)

            # follow each link in a loop while saving the photo
            for item in list_photos_hrefs:
                req = requests.get(url=item, headers=headers)
                soup = BeautifulSoup(req.text, "lxml")
                # sc-7c0a9e7c-1 kJatiV
                # sc-7c0a9e7c-0 hXPlvk
                try:
                    # picture_href = soup.find("img", class_="MediaViewerImagestyles__LandscapeImage-sc-1qk433p-1 jcxEsx").get("src")
                    picture_href = soup.find("img", class_="sc-7c0a9e7c-1 kJatiV").get("src")
                except Exception:
                    # picture_href = soup.find("img", class_="MediaViewerImagestyles__LandscapeImage-sc-1qk433p-1 jcxEsx").get("src")
                    picture_href = soup.find("img", class_="sc-7c0a9e7c-0 hXPlvk").get("src")

                print(picture_href)
                req = requests.get(url=picture_href, headers=headers)
                out = open(f"data/actors/{actor_name}_{actor_ID}/photo_{count}.jpg", "wb")
                out.write(req.content)
                out.close()
                print(f"Photo {count} successfully saved!")
                count += 1
            save_photos.append(count)
    data = {
        'index':name_list,
        'found_photos':found_photos,
        'saved_photos':save_photos
    }
    df = pd.DataFrame(data)
    df.to_excel('download_sheet.xlsx', index=False)
    print("Job completed, all photos downloaded successfully.")

except Exception as ex:
    print(ex)
