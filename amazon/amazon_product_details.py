import requests
import json

# from amazon_scrape import *
# from amazon_product_links import *

# scrape()
# get_links()

with open('amazon_parse.json', 'r') as file:
    parse_data = json.load(file)

def get_details():
    parent_dict = {
        "products": []
    }
    payload = {
        'source': 'amazon',
        'parse': True,
        'url': None,
        'parsing_instructions': parse_data
    }

    with open('amazon_product_links.json') as f:
        data = json.load(f)
    json_data = json.dumps(data)
    json_data=json_data[1:-1].split(",")
    count=0
    for x in json_data:
        print(count)
        count+=1
        link=x.replace('"',"").strip()
        # Structure payload.
        payload['url']=link
        # Get response.
        response = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=('lostsoul_APCbT', 'Lost_soul1234'), #Your credentials go here
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
            product_description = results["description"]
        else:
            product_description="description not available"

        try:
            product_description = product_description.replace("Read Lessabout the seller notes", "").replace("“", "").replace("”", "")
        except:
            None

        if results["product_original_price"]:
            original_price = results["product_original_price"]
        else:
            original_price = "Not Available"
        
        if results["product_discounted_price"]:
            discounted_price = results["product_discounted_price"]
        else:
            continue

        if results["discount_percentage"]:
            discount = results["discount_percentage"][1:]
        else:
            continue

        product_img_url = results["product_image_url"]
        
        product_data = {
            "site":'amazon',
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

    product_json = json.dumps(parent_dict, indent=4)
    with open("amazon_products.json", "w") as outfile:
        outfile.write(product_json)

get_details()