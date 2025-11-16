from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os

def download_image(img_url, title):
    if not img_url:
        return None

    # Create folder if not exists
    os.makedirs("downloaded_images", exist_ok=True)

    # Use title as filename (clean unsafe characters)
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    file_path = f"downloaded_images/{safe_title}.jpg"

    try:
        r = requests.get(img_url, timeout=10)
        with open(file_path, "wb") as f:
            f.write(r.content)
        return file_path
    except:
        return None


#Function to Translate Text from Spanish to English
def translate_to_english(text):
    rapid_uri = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

    payload = {
        "from": "es",
        "to": "en",
        "q": text
    }

    # Headers contains my API Key to access Rapid Translate API
    headers = {
        "x-rapidapi-key": "9cc144cac8msh128d2a830f36251p126357jsnd746eee3944d",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(rapid_uri, json=payload, headers=headers)

    data = response.json()

    if isinstance(data, list) and data:
        return data[0]
    return ""


website = 'https://elpais.com/opinion/'
path = r'C:\Users\shris\Downloads\chromedriver-win64\chromedriver.exe'


service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

# This code automatically removes the Accept Cookies popup by clicking on the accept button in the pop-up
WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button"))
).click()

articles = driver.find_elements(By.TAG_NAME, "article")

# This loop is used to check what is being fetched inside the article variable its for my testing purpose
# for i, article in enumerate(articles, start=1):
#     html = article.get_attribute("outerHTML")
#     soup = BeautifulSoup(html, "html.parser")
#     print(f"\n--------- ARTICLE {i} ---------")
#     print(soup.prettify())


# This part fetches all the titles from the articles present on the opinions page
# All article titles and their corresponding links were located under the <article> then <header>.
# So I inspected the page and added all possible tags that could contain the titles to ensure
# I could extract them correctly by keeping the respective tags under selector array.

articles_data = []
for article in articles:
    title = None
    link = None

    # Try all possible title selectors
    selectors = ["header h2 a","header h3 a"]

    for sel in selectors:
        elements = article.find_elements(By.CSS_SELECTOR, sel)
        if elements:
            title_el = elements[0]
            title = title_el.text.strip()
            link = title_el.get_attribute("href")
            break

    articles_data.append({
        "title": title,
        "link": link
    })


# My approach for extracting content was to first navigate to each article link and retrieve the full HTML of the article
# body. Then, I used BeautifulSoup to convert it into plain text, removing unnecessary tags, spaces, and other clutter.
# After successfully extracting the content, I removed the link from the corresponding dictionary entry.
count = 0
for item in articles_data:

    # I am trying to go to each and every link and fetch there content
    url = item["link"]
    driver.get(url)
    try:

        # container variable fetches all the data present inside the div tag whose class name is .a_c.clearfix article tag
        # This is the wrapper containing all article paragraphs.
        # which can be parsed later easily
        container = driver.find_element(By.CSS_SELECTOR, "article .a_c.clearfix")

        # This extracts all HTML inside that container, as a string.
        html = container.get_attribute("innerHTML")

        # Creates a BeautifulSoup object from the extracted HTML.
        soup = BeautifulSoup(html, "html.parser")

        # Extract all <p> text
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

        item["content"] = " ".join(paragraphs)

        try:
            img_el = driver.find_element(By.CSS_SELECTOR, "article img")
            img_url = img_el.get_attribute("src")
        except:
            img_url = None

            # Download image
        item["image_path"] = download_image(img_url, item["title"])

        del item["link"]

    except Exception as e:
        count -= 1

    count += 1
    if count== 5 :
        break

# This part is used to translate and calculate the number of common words
word_count = {}
for item in articles_data:
    if "content" in item:
        item["title_en"] = translate_to_english(item["title"])

        newTitle = ""
        for s in item["title_en"]:
            if s.isalnum() or s.isspace():
                newTitle = newTitle + s

        words = newTitle.split()

        for w in words:
            w = w.lower()
            if w in word_count:
                word_count[w] += 1
            else:
                word_count[w] = 1

        print("English Title:", item["title_en"])
        print("Spanish Title:", item["title"])
        print("Content:", item["content"])

for word, count in word_count.items():
    if count > 2:
        print(word, ":", count)

# to stop automatic closure of the tab
# input("Press enter to continue...")
