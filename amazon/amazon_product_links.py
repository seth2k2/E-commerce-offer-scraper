import json
from bs4 import BeautifulSoup

def get_links():    

    with open("amazon_sample.json", "r") as file:
        raw_data = json.load(file)

    html_content = raw_data["results"][0]["content"]

    soup = BeautifulSoup(html_content, "html.parser")

    links = []
    for a_tag in soup.find_all("a", class_="a-link-normal dcl-product-link"):
        href = a_tag.get("href")
        if href: 
            links.append("https://www.amazon.com"+href)

    with open("product_links.json", "w") as outfile:
        json.dump(links, outfile, indent=4)

    print("Links being saved to 'product_links.json'")

