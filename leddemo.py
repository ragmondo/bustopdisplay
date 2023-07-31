
from mock import MagicMock
import requests
from datetime import datetime
import pprint

try:
    import ledshim
except ImportError:
    print("Import error with ledshim .. mocking")
    mm = MagicMock()
    mm.DISPLAY_WIDTH = 20
    ledshim = mm

def led():
    for col in ((255, 0, 0), (0, 255, 0), (0, 0, 255)):
        r, g, b = col
        for x in range(ledshim.DISPLAY_WIDTH):
            ledshim.clear()
            ledshim.set_pixel(x, r, g, b)
            ledshim.show()

def get_time_difference(target_time_str):
    # Convert the target time string to a datetime object
    target_time = datetime.strptime(target_time_str, "%Y-%m-%dT%H:%M:%SZ")

    # Get the current time as a datetime object
    current_time = datetime.utcnow()

    # Calculate the time difference
    time_difference = target_time - current_time

    return time_difference


def gettimes():
    try:
        url = "https://api.tfl.gov.uk/Line/20/Arrivals"

        hdr = {
            # Request headers
            'Cache-Control': 'no-cache',
        }

        response = requests.get(url, params = hdr)

        data = response.json()

        results = [(x['timeToLive'],x['timeToStation']) for x in data if x['stationName']=='Leyton Green Road']

        results = sorted(results, key=lambda x: x[1])

        displays = [get_time_difference(x[0]) for x in results]

        pprint.pprint(results)
        pprint.pprint(displays)

        minutes = [int(x.seconds/60) for x in displays]

        for d in minutes:
            print(d)

        ledshim.clear()
        for x in range(ledshim.DISPLAY_WIDTH):
            if x in minutes:
                print(f"switching on for {x}")
                r = 255
                g = 0
                b = 0
                ledshim.set_pixel(x, r, g, b)
        ledshim.show()

    except Exception as e:
        print("Error:", e)

def run():
    gettimes()

if __name__ == '__main__':
    run()
