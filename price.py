import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

Product_name = []
Prices = []
Description = []
Reviews = []

n = int(input("Enter the number of pages to scrape: "))
for i in range(1, n + 1):
    url = f"https://www.flipkart.com/search?q=mobiles+under+15000&page={i}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    box = soup.find("div", class_="DOjaWF gdgoEp")
    if not box:
        continue

    names = box.find_all("div", class_="yKfJKb row")
    for name in names:
        Product_name.append(name.text)

    prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)

    desc = box.find_all("ul", class_="G4BRas")
    for description in desc:
        Description.append(description.text)

    reviews = box.find_all("div", class_="XQDdHH")
    for review in reviews:
        Reviews.append(review.text)

df = pd.DataFrame({"Product name": Product_name, "Prices": Prices, "Description": Description, "Reviews": Reviews})
print(df)

# Save scraped data to CSV
df.to_csv("Flipkart_mobiles_under_15000.csv", index=False)

target_price = 12000

def check_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    price = soup.find('div', attrs={"class": "Nx9bqj _4b5DiR"})
    if price:
        price_text = price.text
        price_without_rs = price_text[1:]
        price_without_comma = price_without_rs.replace(",", "")
        int_price = int(price_without_comma)
        return int_price
    return None

def alert_system(product, link):
    email_id = 'ramolaaditi2@gmail.com'
    email_pass = 'ldrl efme jsdy seaq'

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert'
    msg['From'] = email_id
    msg['To'] = 'ramolaaditi2@gmail.com'
    msg.set_content(f'Hey, the price of {product} dropped!\n{link}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)

def generate_daily_report(df):
    today = datetime.today().strftime('%Y-%m-%d')
    daily_report_filename = f"Daily_Report_{today}.csv"
    df.to_csv(daily_report_filename, index=False)
    print(f"Daily report generated: {daily_report_filename}")
url = "https://www.flipkart.com/search?q=mobiles+under+15000"
cur_price = check_price(url)
print(f"Current price is {cur_price}")
print("We will inform you once the price of the product hits our target price.")
print("Waiting...")

while True:
    cur_price = check_price(url)
    if cur_price is not None and cur_price <= target_price:
        print(f"It's time to buy the product, its current price is {cur_price}")
        alert_system("product_name", url)
        break
    time.sleep(60)
generate_daily_report(df)
