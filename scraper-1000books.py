import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import openpyxl


def scrape_all_books():
    print("SCRAPER ACTIVATED  ...\n")

    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    # Scrape all 50 pages
    for page_num in tqdm(range(1, 51), desc="Scraping", ncols=60, colour="green"):
        url = base_url.format(page_num)
        response = requests.get(url)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.find("h3").find("a")["title"]
            price = book.find("p", class_="price_color").text
            rating = book.find("p")["class"][1]

            all_books.append({
                "title": title,
                "price": price,
                "rating": rating
            })

    # Create Excel file
    print("\n📊 Saving to Excel...")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Books"

    # Header row
    sheet["A1"] = "Title"
    sheet["B1"] = "Price"
    sheet["C1"] = "Rating"

    # Make headers bold
    from openpyxl.styles import Font
    sheet["A1"].font = Font(bold=True)
    sheet["B1"].font = Font(bold=True)
    sheet["C1"].font = Font(bold=True)

    # Add all books
    for i, book in enumerate(all_books, start=2):
        sheet[f"A{i}"] = book["title"]
        sheet[f"B{i}"] = book["price"]
        sheet[f"C{i}"] = book["rating"]

    # Auto adjust column widths
    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        sheet.column_dimensions[column_letter].width = max_length + 5

    # Save file
    workbook.save("books_data.xlsx")
    print(f"✅ Done! {len(all_books)} books saved to books_data.xlsx")
    print("📁 Check your project folder for the Excel file!")


scrape_all_books()