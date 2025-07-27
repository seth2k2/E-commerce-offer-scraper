from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

driver = webdriver.Chrome()


driver.get("https://www.aliexpress.com/gcp/300000533/KDdtyft4ys?spm=a2g0o.best.testStatic.3.2076423aFZytxh&disableNav=YES&pha_manifest=ssr&_immersiveMode=true&_gl=1*1w39npn*_gcl_aw*R0NMLjE3MzM0MTY4MTkuQ2owS0NRaUF1OFc2QmhDLUFSSXNBQ0VRb0RERlF3THM1YkNuMXl1MlVmRUNNZ1dCOVptTkJsajJsNDdHeVRGLWlMZ096T2hucnA3d0h3d2FBa0c1RUFMd193Y0I.*_gcl_au*MTY3ODc3ODc4OC4xNzMxMTc3MDc1*_ga*MTU5MTEwNTMyMS4xNzMxMTc3MDc1*_ga_VED1YSGNC7*MTczMzQxNDM1MS44LjEuMTczMzQxNjgxOC42MC4wLjA.")
time.sleep(5)#to load


product_links = []


wait = WebDriverWait(driver, 10)

try:
    # look for the section buttons 
    category_buttons = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//span[@class='rax-text-v2 tab_text']")))

    # Loop through each category button and click it
    for category_button in category_buttons:
        try:
            ActionChains(driver).move_to_element(category_button).click().perform()
            time.sleep(5)  #to load

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            links = [a['href'] for a in soup.find_all('a', href=True) if 'item' in a['href']]
            for link in links:
                if link.startswith('//'):
                    product_links.append('https:' + link)
                else:
                    product_links.append(link)
            
            print(f"Scraped {len(links)} product links from the current section")
        
        except Exception as e:
            print(f"Error clicking category: {e}")

except Exception as e:
    print(f"Error finding category buttons: {e}")


driver.quit()

print(f"Total product links found: {len(product_links)}")


with open("test_links.json", "w") as outfile:
    json.dump(links, outfile, indent=4)
