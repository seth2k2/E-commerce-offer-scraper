import requests
import json

# Structure payload.
def scrape():

    payload = {
    'source': 'amazon',
    'url': 'https://www.amazon.com/cybermonday?ref_=nav_cs_gb&discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522'
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('lostsoul_APCbT', 'Lost_soul1234'), #Your credentials go here
        json=payload,
    )


    json_object = json.dumps(response.json(), indent=4)
    
    with open('amazon_sample.json', "w") as outfile:
        outfile.write(json_object)





