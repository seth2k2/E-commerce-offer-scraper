import requests
import json
import time

# from ali_scrape import *
# from ali_product_links import *

# scrape()
# get_links()

with open('ali_parse.json', 'r') as file:
    parse_data = json.load(file)

def get_details():
    parent_dict = {
        "products": []
    }

    payload = {
        'source': 'universal',
        'url': None,
        'geo_location': 'United States',
        'locale': 'en-us',
        'user_agent_type': 'desktop',
        'render': 'html',
        #to click the specification button to get the detailed specification in aliexpress
        'browser_instructions': [{'type': 'click','selector': {'type': 'xpath','value': '//div[@data-pl="product-specs"]//button'}}],
        'parse': True,
        'parsing_instructions': parse_data
    }

    with open('ali_product_links.json') as f:
        data = json.load(f)

    data=list(data)
    count=0
    for x in data:
        count+=1
        print(count)
        link='https://'+x[2:].split('?pvid')[0]
        payload['url']=link

        try:
            response = requests.request(
                'POST',
                'https://realtime.oxylabs.io/v1/queries',
                auth=('lostsoul_APCbT', 'Lost_soul1234'), 
                json=payload,
            )

            response_data = response.json()

            results =  response_data["results"][0]["content"]

            if results["product_title"]:
                product_name = results["product_title"]
            else:
                continue

            if results["positive_rating_percentage"]:
                product_rating = results["positive_rating_percentage"]
            else:
                product_rating="rating not available"

            if results["description"]:
                product_description=""
                for x in results["description"]:
                    product_description+=f"{x['Title']} : {x['Description']} \n"

            else:
                product_description="description not available"

            if results["product_original_price"]:
                original_price = results["product_original_price"]
            else:
                original_price = "Not Available"

            if results["product_discounted_price"]:
                discounted_price = results["product_discounted_price"]
            else:
                continue

            if results["discount_percentage"]:
                discount = results["discount_percentage"].split(' ')[0]
            else:
                continue

            product_img_url = results["product_image_url"]

            product_data = {
                "site":'aliexpress',
                "product_name": product_name,
                "product_description": product_description,
                "product_rating":product_rating,
                "original_price": original_price,
                "discounted_price": discounted_price,
                "discount": discount,
                "product_image_url":product_img_url,
                "product_url":link
            }

            parent_dict["products"].append(product_data)

        except:
            time.sleep(10)
            continue

        product_json = json.dumps(parent_dict, indent=4)
        with open("ali_products.json", "w") as outfile:
            outfile.write(product_json)

get_details()