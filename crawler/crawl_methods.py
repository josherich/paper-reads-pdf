from bs4 import BeautifulSoup
# from selenium import webdriver
from urllib.parse import urlparse, urljoin
# from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import InvalidSessionIdException, ElementClickInterceptedException
import time


def get_hrefs_html(response, follow_foreign_hosts=False):
    urls = set()
    output = []
    soup = BeautifulSoup(response.text, "lxml")
    parsed_response_url = urlparse(response.url)
    urls_on_page = [link.attrs.get("href") for link in soup.find_all('a')]

    for url in urls_on_page:

        if url not in urls:

            follow = True
            parsed_url = urlparse(url)

            if not parsed_url.path:
                continue

            if not parsed_url.netloc:
                url = urljoin(response.url, parsed_url.path)
                parsed_url = urlparse(url)

            if parsed_response_url.netloc != parsed_url.netloc and not follow_foreign_hosts:
                follow = False

            urls.add(url)
            output.append({"url": url, "follow": follow})

    return output


def handle_url_list_js(output_list, new_urls, parsed_response_url, follow_foreign_hosts):
    urls_present = [x['url'] for x in output_list]
    new_output = []

    for url in new_urls:

        if url not in urls_present:

            follow = True
            parsed_url = urlparse(url)

            if parsed_response_url.netloc != parsed_url.netloc and not follow_foreign_hosts:
                follow = False

            urls_present.append(url)
            new_output.append({"url": url, "follow": follow})

    return new_output


def get_hrefs_js_simple(response, follow_foreign_hosts=False):
    parsed_response_url = urlparse(response.url)
    try:
        response.html.render(reload=False)
        urls_on_page = response.html.absolute_links
    except Exception:
        return get_hrefs_html(response, follow_foreign_hosts)

    return handle_url_list_js([], urls_on_page, parsed_response_url, follow_foreign_hosts)


def is_valid_link(link):
    if not link or link == "#" or link == "":
        return False
    return True


def make_element_id(element):
    id_str = ""

    css_properties = ["font-size", "font-weight", "margin", "padding", "color", "position", "display"]

    try:
        id_str += "text=" + str(element.text) + ";"

        for k, s in element.size.items():
            id_str += str(k) + "=" + str(s) + ";"

        for k, s in element.location_once_scrolled_into_view.items():
            id_str += str(k) + "=" + str(s) + ";"

        for k in css_properties:
            id_str += str(k) + "=" + str(element.value_of_css_property(k)) + ";"

    except Exception:
        return None

    return id_str

