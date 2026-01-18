from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Playwright

url_base = "https://www.imdb.com/search/title/"
release_date = "2018-01-01,2018-12-31"
title_type = "feature"
url_scrapp = f"{url_base}?release_date={release_date}&title_type={title_type}"

# Tenemos que esperar a que cargue el js, no estan las cosas en el source
def run(playwright: Playwright):
    chromium = playwright.chromium 
    browser = chromium.launch(headless=True)
    """
    <noscript>
        <h1>JavaScript is disabled</h1>
        In order to continue, we need to verify that you're not a robot.
        This requires JavaScript. Enable JavaScript and then reload the page.
    </noscript>
    """
    # Debemos agregar context y el agent o sino sale el error de arriba
    context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36")

    # page = browser.new_page()
    page = context.new_page()
    page.goto(url_scrapp)
    
    page.locator("button.ipc-see-more__button").click(button="left")

    html = page.content()
    browser.close()

    return html

with sync_playwright() as playwright:
    html = run(playwright)

soup = BeautifulSoup(html, "lxml")
movies_list = soup.find_all('li', class_='ipc-metadata-list-summary-item')
movies_titles = [movies.find('h3', class_='ipc-title__text').text for movies in movies_list]
print(movies_titles)