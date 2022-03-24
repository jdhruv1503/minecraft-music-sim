import PySimpleGUI as sg
import datetime
import base64
from urllib.request import urlopen 
import json
import sys
import webbrowser


SETTINGS_PATH = '.'
MUSIC_PATH = ''  # Set using the "Settings" window and saved in your config file

sg.theme('Light Green 6')
ALPHA = 0.8
BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()

APP_DATA = {
    'Title': 'Sweden',
    'WaitTime': 0.0,
    'Icon': ''
}


with open(r"icon.png", "rb") as img_file:
    APP_DATA['Icon'] = base64.b64encode(img_file.read()).decode('utf-8')


def load_settings():
    global MUSIC_PATH
    settings = sg.UserSettings(path=SETTINGS_PATH)
    MUSIC_PATH = settings['-musicpath-']
    if not MUSIC_PATH:
        sg.popup_quick_message('No valid path found... opening setup window...', keep_on_top=True, background_color='red', text_color='white',
                               auto_close_duration=3, non_blocking=False)
        change_settings(settings)
    return settings



def change_settings(settings, window_location=(None, None)):
    global APP_DATA, API_KEY

    layout = [[sg.T('Enter Music path:')],
              [sg.I(settings.get('-musicpath-', ''), size=(15, 1), key='-MUSICPATH-')],
              [sg.B('Save', border_width=0, bind_return_key=True),  sg.B('Cancel', border_width=0)], ]

    window = sg.Window('Settings', layout, location=window_location, no_titlebar=True, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()


    if event == 'Save':
        MUSIC_PATH = settings['-musicpath-'] = values['-MUSICPATH-']
    else:
        MUSIC_PATH = settings['-musicpath-']

    return settings


def update_music_data():
    global APP_DATA

    """

    TO DO: Update all values and also grab albumart
    
    weather = json.loads(response.read())
    APP_DATA['City'] = weather['name'].title()
    APP_DATA['Description'] = weather['weather'][0]['description']
    APP_DATA['Temp'] = "{:,.0f}°F".format(weather['main']['temp'])
    APP_DATA['Humidity'] = "{:,d}%".format(weather['main']['humidity'])
    APP_DATA['Pressure'] = "{:,d} hPa".format(weather['main']['pressure'])

    icon_url = "http://openweathermap.org/img/wn/{}@2x.png".format(weather['weather'][0]['icon'])
    APP_DATA['Icon'] = base64.b64encode(request.urlopen(icon_url).read())

    """


def metric_row(metric):
    """ Return a pair of labels for each metric """
    return [sg.Text(metric, font=('Arial', 10), pad=(15, 0), size=(9, 1)),
            sg.Text(APP_DATA[metric], font=('Arial', 10, 'bold'), pad=(0, 0), size=(9, 1), key=metric)]


def create_window(win_location):
    """ Create the application window """

    """ Cross at the top """
    col2 = sg.Column(
        [[sg.Text('×', font=('Arial Black', 16), pad=(0, 0), justification='right', background_color=BG_COLOR, text_color=TXT_COLOR, enable_events=True,
                  key='-QUIT-')]],
        element_justification='right', background_color=BG_COLOR, key='COL2')

    """ This is for changing settings """
    col4 = sg.Column(
        [[sg.Text('Settings', font=('Arial', 8, 'italic'), background_color=BG_COLOR, text_color=TXT_COLOR, enable_events=True, key='-CHANGE-')]],
        pad=(10, 5), element_justification='right', background_color=BG_COLOR, key='COL4')


    top_col = sg.Column([[col2]], pad=(0, 0), background_color=BG_COLOR, key='TopCOL')

    bot_col = sg.Column([[col4]], pad=(0, 0), background_color=BG_COLOR, key='BotCOL')


    """ LfCOL is image, RtCOL is title """
    lf_col = sg.Column(
        [[sg.Image(data=APP_DATA['Icon'], pad=((5, 15), (0, 0)), size=(100, 100), background_color=BG_COLOR, key='Icon')]],
        pad=(10, 0), element_justification='center', key='LfCOL')
    rt_col = sg.Column(
        [[sg.Text(APP_DATA['Title'], font=('Haettenschweiler', 40), pad=((10, 0), (0, 0)), justification='center', key='Title')]],
        pad=(10, 0), element_justification='center', key='RtCOL')


    layout = [[top_col],
              [lf_col, rt_col],
              [bot_col]]


    window = sg.Window(layout=layout, title='Music Widget', margins=(0, 0), finalize=True, location=win_location,
                       element_justification='center', keep_on_top=True, no_titlebar=True, grab_anywhere=True, alpha_channel=ALPHA)

    for col in ['COL2', 'TopCOL', 'BotCOL']:
        window[col].expand(expand_y=True, expand_x=True)

    for col in ['COL4', 'LfCOL', 'RtCOL']:
        window[col].expand(expand_x=True)

    window['-CHANGE-'].set_cursor('hand2')
    window['-QUIT-'].set_cursor('hand2')

    return window

def update_metrics(window):

    """ Adjust the GUI to reflect the current weather metrics """
    
    metrics = ['Title', 'WaitTime', 'Icon']
    for metric in metrics:
        if metric == 'Icon':
            window[metric].update(data=APP_DATA[metric])
        else:
            window[metric].update(APP_DATA[metric])


def main(refresh_rate, win_location):
    """ The main program routine """
    
    refresh_in_milliseconds = refresh_rate * 60 * 1000

    # Load settings from config file. If none found will create one
    settings = load_settings()
    musicpath = settings['-musicpath-']
    if musicpath is not None:
        MUSIC_PATH = musicpath
        update_music_data()
    else:
        sg.popup_error('Can\'t find a path. Your music path: ', musicpath)
        exit()

    window = create_window(win_location)

    while True:  # Event Loop
        event, values = window.read(timeout=refresh_in_milliseconds)
        if event in (None, '-QUIT-'):
            break
        if event == '-CHANGE-':
            x, y = window.current_location()
            settings = change_settings(settings, (x + 405, y))
        elif event != sg.TIMEOUT_KEY:
            sg.Print('Unknown event received\nEvent & values:\n', event, values)

        update_music_data()
        update_metrics(window)
    window.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        location = sys.argv[1].split(',')
        location = (int(location[0]), int(location[1]))
    else:
        location = (None, None)
    main(refresh_rate=1, win_location=location)

