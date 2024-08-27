from botasaurus import *
import urllib.parse
from .constants import BLOQUEAR_IMAGENS, IS_HEADLESS



@browser(
    block_images=BLOQUEAR_IMAGENS,
    parallel=1,
    reuse_driver=True,
    cache=True,
    output=None,
    headless=IS_HEADLESS
)
def scrape_places(driver: AntiDetectDriver, link):

    def scrape_place_data():
        driver.get(link)

        if driver.is_in_page("https://consent.google.com/"):
            agree_button_selector = 'form:nth-child(2) > div > div > button'
            driver.click(agree_button_selector)
            driver.get(link)

        title_selector = 'h1'
        title = driver.text(title_selector)

        rating_selector = "div.F7nice > span"
        rating = driver.text(rating_selector)

        reviews_selector = "div.F7nice > span:last-child"
        reviews_text = driver.text(reviews_selector)
        reviews = int(''.join(filter(str.isdigit, reviews_text))
                      ) if reviews_text else None

        website_selector = "a[data-item-id='authority']"
        website = driver.link(website_selector)

        phone_xpath = "//button[starts-with(@data-item-id,'phone')]"
        phone_element = driver.get_element_or_none(phone_xpath)
        phone = phone_element.get_attribute(
            "data-item-id").replace("phone:tel:", "") if phone_element else None
        
        category_selector = '[jsaction*=".category"]'
        category_text = driver.text(category_selector)

        address_xpath = "//button[starts-with(@data-item-id,'address')]"
        address_element = driver.get_element_or_none(address_xpath)
        address = address_element.get_attribute(
            "aria-label").replace("Endereço:", "") if address_element else None

        if title is not None:
            print("raspagem " + title)
        else:
            print("raspagem ")

        return {
            "title": title,
            "phone": phone,
            "category":category_text,
            "address": address,
            "website": website,
            "reviews": reviews,
            "rating": rating,
            "link": link,
        }
    return scrape_place_data()


@browser(
    block_images=BLOQUEAR_IMAGENS,
    parallel=1,
    reuse_driver=True,
    cache=True,
    output=None,
    headless=IS_HEADLESS
)
def scrape_places_links(driver: AntiDetectDriver, query):
    def visit_google_maps():
        encoded_query = urllib.parse.quote_plus(query)
        url = f'https://www.google.com/maps/search/{encoded_query}'
        driver.get(url)

        if driver.is_in_page("https://consent.google.com/"):
            agree_button_selector = 'form:nth-child(2) > div > div > button'
            driver.click(agree_button_selector)
            driver.get(url)

    def scroll_to_end_of_places_list():
        end_of_list_detected = False

        while not end_of_list_detected:
            places_list_element_selector = '[role="feed"]'
            driver.scroll(places_list_element_selector)
            print('Scroll estabelecimentos...' + query)

            end_of_list_indicator_selector = "p.fontBodyMedium > span > span"
            if driver.exists(end_of_list_indicator_selector):
                end_of_list_detected = True

        print('Estabelecimentos scrolados até o fim da lista...' + query)

    def extract_place_links():
        places_links_selector = '[role="feed"] > div > div > a'
        return driver.links(places_links_selector)

    visit_google_maps()
    scroll_to_end_of_places_list()

    places_links = extract_place_links()

    return places_links

def replace_spaces_and_commas(input_string):
    return input_string.replace(' ', '_').replace(',', '_').lower()