from functions import api
from functions import excel_sheet
from functions import own_language_title
from functions import posters_html
from functions import messages

def start_engine():     # executed with the "Save & Start" button click in main
    try:
        title, year_of_release, directors, actors, genres, lengthHour, lengthMinute = api.data_collection()
    
    except:
        messages.error_pop_up('data_coll')
        return

    excel_sheet.write_sheet(title, year_of_release, directors, actors, genres, lengthHour, lengthMinute)

    own_language_title.search(title, year_of_release)

    excel_sheet.launch_sheets()

    posters_html.compose()

# start_engine()