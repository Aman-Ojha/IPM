import json
import webbrowser
import requests
from colorama import Fore

location = 0


def get_location():
    global location
    if not location:
        print("Getting Location ... ")
        send_url = 'http://api.ipstack.com/check?access_key=8f7b2ef26a8f5e88eb25ae02606284c2&output=json&legacy=1'
        r = requests.get(send_url)
        location = json.loads(r.text)
    return location


def directions(to_city, from_city=0):
    if not from_city:
        from_city = get_location()['city']
    url = "https://www.google.com/maps/dir/{0}/{1}".format(from_city, to_city)
    webbrowser.open(url)


def locate_me():
    hcity = get_location()['city']
    print(Fore.BLUE + "You are at " + hcity + Fore.RESET)


def weather(city):
    
    country = get_location()['country_name']

    # If country is US, shows weather in Fahrenheit
    if country == 'United States':
        send_url = (
            "http://api.openweathermap.org/data/2.5/weather?q={0}"
            "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units=imperial".format(
                city)
        )
        unit = ' ºF in '

    # If country is not US, shows weather in Celsius
    else:
        send_url = (
            "http://api.openweathermap.org/data/2.5/weather?q={0}"
            "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units=metric".format(
                city)
        )
        unit = ' ºC in '
    r = requests.get(send_url)
    j = json.loads(r.text)

    # check if the city entered is not found
    if 'message' in j and j['message'] == 'city not found':
        print(Fore.BLUE + "City Not Found" + Fore.RESET)
        return False

    else:
        temperature = j['main']['temp']
        description = j['weather'][0]['main']
        print("{COLOR}It's {TEMP}{UNIT}{CITY} ({DESCR}){COLOR_RESET}"
              .format(COLOR=Fore.BLUE, COLOR_RESET=Fore.RESET,
                      TEMP=temperature, UNIT=unit, CITY=city,
                      DESCR=description))

    return True





def main(data):
    to_city = data.split()
    to_city=[word for word in to_city if word not in ["direction","directions","from","here","office","college","to","there","that","the","city","nearest","closest","nearby"]]
    '''to_index = wordIndex(data, "to")
    if " from " in data:
        from_index = wordIndex(data, "from")
        if from_index > to_index:
            to_city = " ".join(word_list[to_index + 1:from_index])
        else:
            to_city = " ".join(word_list[to_index + 1:])
    else:
        to_city = " ".join(word_list[to_index + 1:])
        from_city = 0'
    directions(to_city, "SRM IST")
    '''
    directions(to_city, "SRM IST")
    
    weather(to_city)


