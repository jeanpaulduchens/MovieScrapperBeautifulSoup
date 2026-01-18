import requests, json

"""
Nos dimos cuenta que se pueden hacer peticiones a la api de graphql de imdb para obtener las peliculas directamente, sin necesidad de usar playwright para cargar la pagina y hacer click en el boton de "ver 50 mas".
Se revisa el payload de la peticion en la pestaña de network de las herramientas de desarrollo del navegador.
Decodeamos en URI el valor de "variables" y "extensions" para entender mejor su estructura.

"""

URL = "https://caching.graphql.imdb.com/"
OP = "AdvancedTitleSearch"
HASH = "9fc7c8867ff66c1e1aa0f39d0fd4869c64db97cddda14fea1c048ca4b568f06a"

HEADERS = {
    "Accept": "application/graphql+json, application/json",
    "Content-Type": "application/json",
    "Origin": "https://www.imdb.com",
    "Referer": "https://www.imdb.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36",
}

variables = {
    "first": 50,
    "after": None,
    "locale": "en-US",
    "releaseDateConstraint": {"releaseDateRange": {"start": "2018-01-01", "end": "2018-12-31"}},
    "sortBy": "POPULARITY",
    "sortOrder": "ASC",
    "titleTypeConstraint": {"anyTitleTypeIds": ["movie"], "excludeTitleTypeIds": []},
}

def call_api(vars_):
    params = {
        "operationName": OP,
        "variables": json.dumps(vars_, separators=(",", ":")),
        "extensions": json.dumps({"persistedQuery": {"sha256Hash": HASH, "version": 1}}, separators=(",", ":")),
    }
    r = requests.get(URL, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

all_titles = []
cursor = None
while True:
    variables["after"] = cursor
    data = call_api(variables)
    ats = data["data"]["advancedTitleSearch"]

    for edge in ats["edges"]:
        all_titles.append(edge["node"]["title"]['titleText']["text"])

    if not ats["pageInfo"]["hasNextPage"]:
        break

    cursor = ats["pageInfo"]["endCursor"]

