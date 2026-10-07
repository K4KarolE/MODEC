import webbrowser
from functions import settings      # when you call it outside functions folder
# import settings                   # learning Python - when you run/test it from inside functions folder

def search(title, year_of_release):
    settings_data = settings.open_settings()
    if settings_data['title_search'] == 1:
        selected_default_link = settings_data['title_search_links'][settings_data['title_search_link_selected']]    # settings_db.json / 'title_search_links' dictionary looking for the 
        link = selected_default_link + ' '.join([title, ''])    # [title, ''] - year_of_release removed, better fot new movies (HUN)
        webbrowser.open(link)

## TEST
# use /import settings/ instead of /from functions import settings/
# search("My Cousin Vinny","1992")
