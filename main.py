import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
search = input("type the product name: ").split() # write the text on the search
result = []
if len(search) > 1:
    search = "+".join(search)
for i in range(1,100):

    url = f"https://www.jumia.com.eg/ar/catalog/?q={search}&page={i}#catalog-listing"
    resp = r.get(url , headers=headers , timeout=10)
    if(resp.status_code != 200):
        break
    if resp.status_code == 200:
        soup = bs(resp.content , "html.parser")

        products = soup.find_all("a" , class_="core")
        for product in products:
            name = product.find("h3" , class_="name").text # The Name of The Product 

            price = product.find("div" , class_="prc").text.split()[0] # The price Of the product

            if product.find("div" , class_="bdg _dsct _sm"):
                discount = product.find("div" , class_="bdg _dsct _sm").text # the percentage of the discount
            else:
                discount = "NoDsiscount"
            stars_div = product.find("div", class_="stars _s")

            if stars_div:
                stars = stars_div.text.split()[0]
            else:
                stars = "No stars found"
            href = product.get('href') # get the product page
            if href:  # Check if href exists
                product_url = f'https://www.jumia.com.eg{href}'
                print(product_url)
                resp2 = r.get(product_url)
            if resp2.status_code == 200:
                soup2 = bs(resp2.content, "html.parser")
                sec = soup2.find("section", class_="col12 -df -d-co")
                mark = sec.find("a", "_more").text if sec and sec.find("a", "_more") else "Undefined" # get the trade mark of the product

                result.append({
                    "name": name,
                    "Mark": mark,
                    "price": price,
                    "Discount": discount,
                    "stars": stars,
                    "product Link": product_url
                })
df = pd.DataFrame(result)
df.to_csv("Jumia_Scrapper.csv" , index=False)