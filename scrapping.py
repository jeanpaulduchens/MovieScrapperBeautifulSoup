from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Playwright
import re


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

    # sacamos el total de resultados
    def get_total_movies(pag):
        soup = BeautifulSoup(pag, "lxml")
        results = soup.find('div', class_="sc-2d056ab8-3 fhbjmI").text
        match = re.search(r"^(.+)\s+of\s+(.+)$", results)
        total_str = match.group(2)
        total_int = int(total_str.replace(",",""))
        return total_int
    
    total_movies = get_total_movies(page.content())
    total_clicks = total_movies // 50

    # si queremos scrappear mas paginas, tenemos que clickear el boton de "ver mas", pero no está a la vista hay que scrollear
    # page.locator("button.ipc-see-more__button").click(button="left")

    # generalizado para obtener todas las peliculas
    def load_all_movies_on_screen(total_clicks):
        for i in range(total_clicks):
            btn = page.locator("button.ipc-see-more__button")
            btn.scroll_into_view_if_needed()
            btn.click()

            page.wait_for_timeout(2000)
            if page.locator("li.ipc-metadata-list.summary-item").count() < 50*(i+2):
                page.wait_for_timeout(2000)
    
    load_all_movies_on_screen(total_clicks)

    html = page.content()
    browser.close()

    return html

with sync_playwright() as playwright:
    html = run(playwright)
    
soup = BeautifulSoup(html, "lxml")
movies_list = soup.find_all('li', class_='ipc-metadata-list-summary-item')
movies_titles = [movies.find('h3', class_='ipc-title__text').text for movies in movies_list]
print(movies_titles)