import requests
import json

# Structure payload.
def scrape():

    payload = {
    'source': 'universal_ecommerce',
    'url': 'https://www.aliexpress.com/gcp/300000533/KDdtyft4ys?spm=a2g0o.best.testStatic.3.463d2c25Nao45Y&disableNav=YES&pha_manifest=ssr&_immersiveMode=true&_gl=1*1kt2yat*_gcl_aw*R0NMLjE3MzMyNDk2MTMuQ2p3S0NBaUE5YnE2QmhBS0Vpd0FINmJxb0ZJZk9kOEhPZGc5YTI1T3BKMVpQX3ZfZ2FJeDVOUzlDNFNSN0R0NEVnc1ZUQ0wtZWszRGJCb0NFcjhRQXZEX0J3RQ..*_gcl_au*MTY3ODc3ODc4OC4xNzMxMTc3MDc1*_ga*MTU5MTEwNTMyMS4xNzMxMTc3MDc1*_ga_VED1YSGNC7*MTczMzM5OTA2NC42LjEuMTczMzQwMDQ2OS42MC4wLjA.'
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('lostsoul_APCbT', 'Lost_soul1234'), #Your credentials go here
        json=payload,
    )


    json_object = json.dumps(response.json(), indent=4)
    
    with open('ali_sample.json', "w") as outfile:
        outfile.write(json_object)





