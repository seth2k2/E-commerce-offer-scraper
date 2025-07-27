import json
from bs4 import BeautifulSoup

def get_links():    

    with open("ebay_sample.json", "r") as file:
        raw_data = json.load(file)

    html_content = raw_data["results"][0]["content"]

    soup = BeautifulSoup(html_content, "html.parser")

    divs = soup.find_all("div", class_="dne-itemtile-detail")

    # Extract links
    links = []
    for div in divs:
        a_tag = div.find("a")  # Find the <a> tag inside the div
        if a_tag and a_tag.has_attr("href"):
            links.append(a_tag["href"])

    # Print extracted links
    for link in links:
        print(link)

    with open("ebay_product_links.json", "w") as outfile:
        json.dump(links, outfile, indent=4)


