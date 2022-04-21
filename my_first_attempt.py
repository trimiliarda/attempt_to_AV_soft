from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests

int_url = set()
ext_url = set()


def is_valid(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def website_links(url: str, indent: int = 0) -> str:
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"

        if not is_valid(href):
            continue
        if domain_name not in href:
            if href not in ext_url:
                ext_url.add(href)
                print(f"{'   ' * indent}[!] External link: {href}")
            continue

        if href not in int_url:
            int_url.add(href)
            print(f"{'   ' * indent}(*) Internal link: {href}")
        if href not in urls:
            urls.add(href)
        yield href


def crawl(url: str, max_deep: int = 1, tab: int = 0) -> None:
    for link in website_links(url, indent=tab):
        if max_deep > 1:
            crawl(link, max_deep=max_deep-1, tab=tab + 1)


if __name__ == "__main__":
    crawl("https://stackoverflow.com/", max_deep=1)  # указываем сайт и желаемую глубину
    print("\t[+] Total External links:", len(ext_url))
    print("\t[+] Total Internal links:", len(int_url))
    print("\t[+] Total:", len(ext_url) + len(int_url))
