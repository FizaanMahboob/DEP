import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the website to scrape
url = "http://books.toscrape.com/"

# Define the CSS selectors for the data you want to extract
title_selector = ".product_pod h3 a"  # Selector for book titles
price_selector = ".product_pod .price_color"  # Selector for book prices

# Create an empty list to store the extracted data
data = []

# Send a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful. Parsing content...")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the title and price elements
    titles = soup.select(title_selector)
    prices = soup.select(price_selector)

    # Check how many elements are found
    print(f"Found {len(titles)} titles and {len(prices)} prices.")

    # Iterate through each title and price element and extract the desired data
    for title, price in zip(titles, prices):
        # Extract the book title
        book_title = title['title']  # Title is stored in the 'title' attribute

        # Extract the price
        book_price = price.text.strip()

        # Add the extracted data to the list
        data.append({"Title": book_title, "Price": book_price})

    # Write the data to a CSV file
    with open("books.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Title", "Price"])
        writer.writeheader()
        writer.writerows(data)

    print("Data extracted successfully and saved to books.csv")

else:
    print(f"Error: Unable to access the website. Status code: {response.status_code}")
