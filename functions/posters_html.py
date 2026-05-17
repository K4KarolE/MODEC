import os
import json
from pathlib import Path
import webbrowser
from functions import settings
# import settings  #testing


def compose():
    settings_data = settings.open_settings()
    if settings_data['poster_open_in_new_tab'] == 1:
        # PATH
        functions_directory = os.path.dirname(__file__)     # os.path.dirname(__file__) = D:\_DEV\Python\31_I_aM_D_bee\functions   //in my case
        main_directory = functions_directory.replace("functions",'')
        path__poster_links_json = Path(main_directory, "json", "poster_links.json")
        path_posters_temp_html = Path(main_directory, "html", "posters_template.html")       # Path functions makes the path OS independent
        path_posters_html = Path(main_directory, "html", "posters.html") 

        # OPEN HTML TEMP
        poster_template = open(path_posters_temp_html)
        list_poster_template = list(poster_template)

        # TITLE
        for index, item in enumerate(list_poster_template):
            if 'TITLE_X' in item:
                list_poster_template[index] = settings_data['title']

        # OPEN POSTER LINKS.JSON
        f = open(path__poster_links_json)
        poster_links_list = json.load(f)

        ## BODY COMPILING
        # POSTER SIZE
        if settings_data['poster_size'] == "Small":
            poster_per_row = 4
        if settings_data['poster_size'] == "Medium":
            poster_per_row = 2
        if settings_data['poster_size'] == "Large":
            poster_per_row = 1

        # ELEMENT INDEX
        for index, item in enumerate(list_poster_template):
            if 'ELEMENT_X' in item:
                element_index = index
        
        # HTML COMPILING
        list_poster_template[element_index] = '<div align="center">\n'
        counter = 1
        for index, item in enumerate(poster_links_list):
            list_poster_template[element_index] += f'<img src={item} hspace="20">\n'
            if index != 0 and counter % poster_per_row == 0 and poster_per_row != 1:
                list_poster_template[element_index] += '</div><br><div align="center">\n'
            if poster_per_row == 1:
                list_poster_template[element_index] += '</div><br><div align="center">\n'
            if index+1 == len(poster_links_list):
                list_poster_template[element_index] += '</div>\n'
            counter += 1

        # HTML COMPILING RESULT - EXAMPLE
        # '<div align="center">
        # <img src="https://image.tmdb.org/t/p/w200/wAv2tBzcTlzrRIKlM7s2cjnpxwA.jpg" hspace="20">
        # <img src="https://image.tmdb.org/t/p/w200/wAv2tBzcTlzrRIKlM7s2cjnpxwA.jpg" hspace="20">
        # ..
        # </div><br><div align="center">    # EXAMPLE: one picture in the last row
        # <img src="https://image.tmdb.org/t/p/w200/wAv2tBzcTlzrRIKlM7s2cjnpxwA.jpg" hspace="20">
        # </div>'

        # SAVING HTML
        file = open(path_posters_html, 'w', encoding="utf-8")
        for i in list_poster_template:
            try:
                file.write(i)
            except:
                print(f'ERROR writing: {i}')
        file.close()

        # OPEN POSTER PAGE
        webbrowser.open(str(path_posters_html))     # LINUX: not working without str()

# compose()  #testing
