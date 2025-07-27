import json
from bs4 import BeautifulSoup

def get_links():    

    with open("ali_sample.json", "r") as file:
        raw_data = json.load(file)

    html_content = raw_data["results"][0]["content"]

    soup = BeautifulSoup(html_content, "html.parser")
    count=0
    links = []
    for a_tag in soup.find_all("a", class_="productContainer"):
        href = a_tag.get("href")
        if href: 
            links.append(href)
            count+=1

    with open("ali_product_links.json", "w") as outfile:
        json.dump(links, outfile, indent=4)

    print("Links being saved to 'product_links.json'")
    print(count)

