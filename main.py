import google.generativeai as genai
import streamlit as st
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the JSON file
with open('amazon/amazon_products.json') as f:
    amazon = json.load(f)

with open('ebay/ebay_products.json') as f:
    ebay = json.load(f)

with open('aliexpress/ali_products.json') as f:
    ali = json.load(f)

# Configure the Generative AI model
api_key = os.getenv('gemini_key')
if not api_key:
    st.error("Gemini API key not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Template for summarization
template = """
You are an intelligent assistant that helps users find the best deals on Amazon. 
Given a description of the user's desired product, search through the following json file data and find all products that match the given name or closely related terms. 
Compare products description and name and provide the matching product names and product sites as it is.

User input: {product_name}
Take keywords from {product_name} and search with available products and retrieve those


You are provided with {ali_data},{amazon_data} ,{ebay_data} data to search products,make sure to go through all the files:

Don't mention about unmatching content in the json file, If couldn't find any matching content do nothing
Provide the results in the following format for each matching product:

site of product 1 -|- product name 1\n
site of product 2 -|- product name 2\n
"""
def get_details(site, name):
    if site == "ebay":
        products_list = ebay['products']
    elif site == "amazon":
        products_list = amazon['products']
    elif site == "aliexpress":
        products_list = ali['products']
    
    for item in products_list:
        if str(item.get("product_name")) == name:
            return item
    
    return None
# Custom CSS for divs
st.markdown(
    """
<style>
.out-div {
    background-color: #2E2E2E; /* Dark ash color */
    color: white; /* Text color */
    padding: 20px;
    margin: 10px 0;
    border-radius: 8px;
    border: 1px solid #444; /* Optional border for separation */
    font-family: Arial, sans-serif;
    position: relative; /* Set position to relative for absolute positioning inside */
}

.product-description {
    max-width: 60%; 
    padding-right: 15px;
}

.product-image {
    max-width: 35%;
    height: auto;
}

.custom-div {
    display: flex;
    align-items: center;
    justify-content: space-between; /* Distribute space between content */
}

#site {
    font-size: 30px;
    color:#51db44;
    position: absolute;
    top: 20px;
    right: 6%;
    font-weight: bold;
}

.view-product-button button {
    background-color: #4CAF50; /* Green background */
    border: none;
    color: white;
    padding: 5px 8px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
}

#title {
    font-size: 20px;
}

#early_price {
    font-size: 21px;
}

#discount_price {
    font-size: 25px;
    color: red;
}
</style>

    """,
    unsafe_allow_html=True
)

st.title("E-Commerce Offer Scraper")


product_details = st.text_input("Enter product details")


if st.button("Search for offers"):
        try:
            if product_details:
                with st.spinner("Searching for offers..."):
                    prompt = template.format(product_name=product_details, amazon_data=amazon,ebay_data=ebay,ali_data=ali)
                    response = model.generate_content(prompt)
                    response=response.text

                    for result in response.split("\n"):
                        if '-|-' in result:
                            site = result.split("-|-")[0].strip()
                            title = result.split("-|-")[1].strip()
                            details=get_details(site, title)
                            if details != None:
                                description = details["product_description"]
                                if len(description) > 300:
                                    prompt = f"Just summarize the following paragraph without saying anything else:\n\n{description}"
                                    response = model.generate_content(prompt)
                                    description = response.text if response else description

                                rating = str(details.get("product_rating"))
                                original_price=str(details.get("original_price"))
                                discounted_price=str(details.get("discounted_price"))
                                discount=str(details.get("discount"))
                                
                                image_url = details.get("product_image_url")
                                if image_url==None or "null" in image_url or "No" in image_url:
                                    image_url = "https://cdn.iconscout.com/icon/free/png-256/free-image-icon-download-in-svg-png-gif-file-formats--picture-photo-gallery-sharing-site-pack-user-interface-icons-1505123.png"
                                
                                product_url = details.get("product_url")
                                
                                st.markdown(
                                    f"""
                                    <div class="out-div">
                                        <div class="custom-div">
                                            <div class="product-description">
                                                <p id='title'><b>{title}</b></p>
                                                <p>{description}</p>
                                                <p>Rating <b>{rating}</b></p>
                                                <p><span id="early_price"><s>{discounted_price}</s></span>&emsp;<span id='discount_price'>{original_price}</span></p>
                                                <p>Disocunt <b>{discount}</b></p>
                                            </div>
                                            <div>
                                                <p id="site">{site}</p>
                                                <img class="product-image" src="{image_url}" alt="Product Image" width=200>
                                            </div>
                                        </div>
                                        <a href="{product_url}" class="view-product-button"><button>View product</button></a>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                        

        except Exception as e:
            st.write("Search limit reached")
            print(e)