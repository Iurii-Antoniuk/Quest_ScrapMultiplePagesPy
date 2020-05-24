import pandas as pd
import csv
import time
import requests as req
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Iurii Antoniuk',
    'From': 'yugonone@gmail.com'
}

baseurl = 'https://www.chucknorrisfacts.fr/facts/mtop?p='
pages = [i for i in range(1, 347)]
all_facts = []
all_notes = []

for page in pages:
    url = baseurl + str(page)
    fact_page = req.get(url, headers=headers)
    soup = BeautifulSoup(fact_page.content, 'html.parser')

    facts_markup = soup.find_all(class_="factbody")
    notes_markup = [fact.find(class_='points').extract()
                    for fact in facts_markup]
    votes_markup = [fact.find(class_='vote').extract()
                    for fact in facts_markup]

    facts = [item.get_text() for item in facts_markup]
    notes = [item.get_text() for item in notes_markup]

    all_facts.extend(facts)
    all_notes.extend(notes)
    # time.sleep(1)

csv_basis = pd.DataFrame(
    {
        'Fact': all_facts,
        'Note': all_notes,
    }
)

csv_basis.to_csv('ChuckNorris_facts')
