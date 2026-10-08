import sys
import pyperclip
import requests
import json
import os
from pathlib import Path

from functions import messages
from functions import settings



functions_directory = os.path.dirname(__file__)     # = D:\_DEV\Python\MODDEC\functions   //in my case
main_directory = functions_directory.replace("functions",'')

def path_json(name_json):
    path_json = Path(main_directory,  "json", name_json)
    return path_json   

def data_collection():
    settings_data = settings.open_settings()

    # API KEY
    path_api_key = Path(main_directory, 'api_key.txt')
    file = open(path_api_key)
    api_key = file.read()
    if api_key == "":
        messages.error_pop_up('api_key_missing')
        return
    file.close()

### GET LINK / IMDB ID
    link = pyperclip.paste()
    counter = 0
    while 'tt' not in link:     # IMDb id: tt7366338
        counter += 1
        messages.error_pop_up('wrong_link')
        link = pyperclip.paste()
        if counter == 2:
            messages.error_pop_up('bye_bye')
            sys.exit()

    link_split= link.split('/')
    for i in link_split:
        if i[0:2] == 'tt':
            imdb_id = i

### FIND
    link_find = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=en-US&external_source=imdb_id'
    response = requests.get(link_find)

    # SAVE, LOAD 'FIND TITLE' RESPONSE
    with open(path_json('find.json'), 'w') as f:
        json.dump(response.json(), f, indent=2)

    f = open(path_json('find.json'))
    find_dic = json.load(f)

    # MOVIE VS. TV - MEDIA DECIDER
    if find_dic['movie_results']:
        find_dic_active = 'movie_results'
        title_name = 'title'
        title_name_original = 'original_title'

    elif find_dic['tv_results']:
        find_dic_active = 'tv_results'
        title_name = 'name'
        title_name_original = 'original_name'

    elif find_dic['tv_episode_results']:
        find_dic_active = 'tv_episode_results'
        title_name = 'name'
        title_name_original = 'name'


    title = find_dic[find_dic_active][0][title_name]
    original_title = find_dic[find_dic_active][0][title_name_original]
    id = find_dic[find_dic_active][0]["id"]
    media_type = find_dic[find_dic_active][0]["media_type"] # movie / tv

    if title != original_title:
        title = f'{title}\n({original_title})'

    # SAVING TITLE
    settings_data['title'] = title
    settings.save_settings(settings_data)

### DETAILS
    link_details = f'https://api.themoviedb.org/3/{media_type}/{id}?api_key={api_key}&language=en-US'
    response = requests.get(link_details)


    # SAVE, LOAD 'DETAILS' RESPONSE
    with open(path_json('details.json'), 'w') as f:
        json.dump(response.json(), f, indent=2)

    f = open(path_json('details.json'))
    details_dic = json.load(f)

    # VERIFY RESPONSE
    if details_dic.get('success') == False:
        messages.error_pop_up_straight(details_dic['status_message'])
        return

    # GENRES
    genres = []
    for item in details_dic['genres']:
        genres.append(item['name'])

    # RELEASE YEAR
    if media_type == 'movie':
        year_of_release = details_dic['release_date'] and details_dic['release_date'][0:4]
    else:
        first_air_date = details_dic['first_air_date'] and details_dic['first_air_date'][0:4]
        last_air_date = details_dic['last_air_date'] and details_dic['last_air_date'][0:4]
        if last_air_date == [] or first_air_date == last_air_date:
            year_of_release = first_air_date
        else:
            year_of_release = f'{first_air_date}-{last_air_date}'
    # RUNTIME
    if media_type == 'movie':
        runtime = details_dic['runtime']
    else:
        if details_dic['episode_run_time']:
            runtime = details_dic['episode_run_time'][0]
        elif details_dic['last_episode_to_air']:
            runtime = details_dic['last_episode_to_air'].get('runtime')
        elif details_dic['next_episode_to_air']:
            runtime = details_dic['next_episode_to_air'].get('runtime')
        else:
            runtime = 0
            messages.error_pop_up('runtime')

    if runtime == None: runtime = 0
    lengthHour = int(runtime/60)    # if runtime < 60 -> lengthHour = 0 addressed in excel_sheet.py, will leave it None
    lengthMinute = runtime%60


    ### CREDITS
    link_credits = f'https://api.themoviedb.org/3/{media_type}/{id}/credits?api_key={api_key}&language=en-US'
    response = requests.get(link_credits)

    # SAVE, LOAD 'CREDITS' RESPONSE
    with open(path_json('credits.json'), 'w') as f:
        json.dump(response.json(), f, indent=2)

    f = open(path_json('credits.json'))
    credits_dic = json.load(f)

    # VERIFY RESPONSE
    if credits_dic.get('success') == False:
        messages.error_pop_up_straight(credits_dic['status_message'])
        return

    # ACTORS
    try:
        actors = []
        i = 0
        while i < 3:
            actors.append(credits_dic['cast'][i]["name"])
            i += 1
    except:
        pass

    # DIRECTORS
    try:
        directors = []
        if media_type == 'movie':
            for item in credits_dic['crew']:
                if item["job"] == "Director":
                    directors.append(item["name"])
    except:
        pass


    ### IMAGES
    if settings_data['poster_open_in_new_tab'] == 1:
        link_images = f'https://api.themoviedb.org/3/{media_type}/{id}/images?api_key={api_key}'
        response = requests.get(link_images)

        # SAVE, LOAD 'IMAGES' RESPONSE
        with open(path_json('images.json'), 'w') as f:
            json.dump(response.json(), f, indent=2)

        f = open(path_json('images.json'))
        images_dic = json.load(f)

        # VERIFY RESPONSE
        if images_dic.get('success') == False:
            messages.error_pop_up_straight(images_dic['status_message'])
            return

        # POSTERS
        posters = []
        for item in images_dic["posters"]:
            if item["iso_639_1"] == "en":
                posters.append(item["file_path"])

        poster_links = []
        selected_poster_size = settings_data['poster_size']     # Small, Medium...
        selected_poster_size_value = settings_data["poster_size_options"][selected_poster_size]     # w200 - Small, w500 - Medium, original - Large
        for item in posters:
            try:
                poster_links.append(f'https://image.tmdb.org/t/p/{selected_poster_size_value}{item}')
            except:
                print(f'FAILED popster link to add: https://image.tmdb.org/t/p/{selected_poster_size_value}{item}')

        with open(path_json('poster_links.json'), 'w') as f:
            json.dump(poster_links, f, indent=2)

    return title, year_of_release, directors, actors, genres, lengthHour, lengthMinute