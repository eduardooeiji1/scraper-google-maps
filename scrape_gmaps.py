from functions.scrape import scrape_places, scrape_places_links, replace_spaces_and_commas
import json
import os


if __name__ == "__main__":
    query = ["escolas, SP", "contabilidade em taubate, SP"]
    links = scrape_places_links(query)

    for q, link in zip(query, links):
        result = scrape_places(link)
        name_output = replace_spaces_and_commas(q)
        file_path = os.path.join('leads', name_output + '.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
            print('Resultado salvo em ' + file_path)
