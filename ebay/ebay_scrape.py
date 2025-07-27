import requests
import json

# Structure payload.
def scrape():
    url='https://www.ebay.com/globaldeals'
    payload = {
    'source': 'universal_ecommerce',
    'url': url
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('lostsoul_APCbT', 'Lost_soul1234'), #Your credentials go here
        json=payload,
    )


    json_object = json.dumps(response.json(), indent=4)
    
    with open('ebay_sample.json', "w") as outfile:
        outfile.write(json_object)

