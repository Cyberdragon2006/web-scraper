import requests
from bs4 import BeautifulSoup

def scrape_books():
    print("Starting Scraping...")

    #Websites we are scraping
    url = "https://books.toscrape.com"

    # Send request to website
    response = requests.get(url)
    response.encoding = "utf-8"

    # Parse the webpage
    soup = BeautifulSoup(response.text, "html.parser")

    #Find all books
    books = soup.find_all("article", class_="product_pod")

    print(f"Found {len(books)} books!\n")

    # Loop through each book
    for book in books:
        #Get title
        title = book.find("h3").find("a")["title"]

        #Get price
        price = book.find("p", class_="price_color").text

        # Print result
        print(f"Book: {title}")
        print(f"Price: {price}")
        print("-" * 40)

#Run
scrape_books()