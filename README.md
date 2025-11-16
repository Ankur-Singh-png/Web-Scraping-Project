# Web-Scraping-Project
This project is a web scraping automation tool built using Selenium and Python. It showcases my ability to extract structured information from websites, integrate external APIs, and perform text processing to clean and organize the scraped data.

<h2>📌 Overview</h2>
Using Selenium, the script navigates through dynamic web pages, interacts with UI elements, and scrapes the required information. The collected data is then enhanced using API calls and processed with Python to ensure clean, usable output.

<h2>🚀 How It Works</h2>

<ol>
  <li>
    For the first step Selenium launches the mentioned website on the browser tab then maximized it for better view using <code>driver.maximize_window()</code>.
  </li>
<br>
  <li>
    For the next step, a cookie-consent pop-up appears about 10–15 seconds after the page loads. 
    The script automatically handles this by detecting the element’s ID and clicking the 
    <strong>“Accept All Cookies”</strong> button as soon as it becomes available.
  </li>
<br>
  <li>
    In the next step, I extracted the titles and links of the articles from the Opinion page (which is in Spanish). 
    All the articles were contained within <code>&lt;article&gt;</code> tags, each of which included a 
    <code>&lt;header&gt;</code> element. The titles were written in either <code>&lt;h2&gt;</code> or 
    <code>&lt;h3&gt;</code> tags. 
    I iterated through each article, checked for the presence of an <code>&lt;h2&gt;</code> or 
    <code>&lt;h3&gt;</code> tag, retrieved its text content, and stored both the title and its corresponding link 
    in a unified array of objects.
  </li>
<br>
  <li>
    Once the title is extracted, retrieving the article content becomes straightforward. However, some articles contain 
    exclusive (paywalled) content, which restricts access. To avoid losing information, the script attempts to extract 
    everything first and then processes the data afterward.
    <br>
    I loop through each link stored in the array of objects (checking for the <code>"Link"</code> key), navigate to the 
    corresponding article page, and locate the section containing the article body. The content is stored inside a 
    <code>&lt;div&gt;</code> with the class <code>.a_c.clearfix</code>. 
    After retrieving the full HTML from this container, I extract all the text from the <code>&lt;p&gt;</code> tags, 
    concatenate the paragraphs, and store the final processed content. 
    <br><br>
    Once content is fetched, I delete the link from the dictionary of its corresponding key. 
    I also created a function to download the thumbnail image for each newsletter article. It takes the image URL, 
    fetches the file, and saves the downloaded image into a designated folder for organized storage.
  </li>
<br>
  <li>
    In this step, I created a function that translates the title of each article from Spanish to English. 
    This function is called for every article and the translated title is then stored in the same object alongside the 
    original Spanish title and its content.
    <br>
    After translation, I iterated through all the English titles, removed any non-alphanumeric and non-space characters, 
    split each title into individual words, converted them to lowercase, and counted their occurrences. 
    Finally, I printed all the words that appeared more than twice.
  </li>
</ol>
