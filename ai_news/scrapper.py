import re

import requests
from bs4 import BeautifulSoup


AVAILABLE_SITES = {
    'en.wikipedia.org': 5,
    'www.washingtonpost.com': 9,
    "news.mit.edu": 5
}


class Tag:
    def __init__(
            self,
            tag_name: str,
            class_name: str = None
    ) -> None:
        self.tag_name = tag_name
        self.class_name = class_name


class GeneralScrapper:
    def __init__(
            self,
            url: str = None,
            title_tags: Tag = None,
            article_tags: Tag = None,
            href_tag: str = None
    ):
        self.url = url
        self.title_tags = title_tags
        self.article_tags = article_tags
        self.href_tag = href_tag

    def parse_article(self) -> str:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        row_article = soup.find_all(
            self.article_tags.tag_name,
            class_=self.article_tags.class_name,
            limit=5
        )
        all_text = []
        for p in row_article:
            if p.find(class_=self.href_tag):
                continue
            if not p:
                continue
            string = re.sub(r'\[.*?\]', '', p.text)
            all_text.append(string)
        return "".join(all_text)


    def parse_title(self) -> str:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        row_title = soup.find_all(
            self.title_tags.tag_name,
            class_=self.title_tags.class_name
        )
        return row_title[0].text


class WashingtonPostsScrapper(GeneralScrapper):
    def __init__(self, url: str, title_tags: Tag = None, article_tags: Tag = None, href_tag: str = None):
        super().__init__(url=url, title_tags=title_tags, article_tags=article_tags, href_tag=href_tag)
        if title_tags is None:
            self.title_tags = Tag("span", "PJLV")
        if article_tags is None:
            self.article_tags = Tag("div", "wpds-c-PJLV article-body")
        if href_tag is None:
            self.href_tag = "hide-for-print"


class MitScrapper(GeneralScrapper):
    def __init__(
            self,
            url: str,
            title_tags: Tag = None,
            article_tags: Tag = None,
            href_tag: str = None
    ) -> None:
        super().__init__(
            url=url,
            title_tags=title_tags,
            article_tags=article_tags,
            href_tag=href_tag
        )
        if title_tags is None:
            self.title_tags = Tag("h1")
        if article_tags is None:
            self.article_tags = Tag(
                "div",
                "paragraph paragraph--type--content-block-text paragraph--view-mode--default"
            )
        if href_tag is None:
            self.href_tag = "hide-for-print"


class WikipediaScrapper(GeneralScrapper):
    def __init__(
            self,
            url: str,
            title_tags: Tag = None,
            article_tags: Tag = None,
            href_tag: str = None
    ) -> None:
        super().__init__(
            url=url,
            title_tags=title_tags,
            article_tags=article_tags,
            href_tag=href_tag)
        if title_tags is None:
            self.title_tags = Tag("span", "mw-page-title-main")
        if article_tags is None:
            self.article_tags = Tag("p")
        if href_tag is None:
            self.href_tag = "hide-for-print"

    def parse_title(self) -> str:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        row_title = soup.find(
            self.title_tags.tag_name,
            class_=self.title_tags.class_name
        )
        return row_title.text


if "__main__" == __name__:
    article = WikipediaScrapper("https://en.wikipedia.org/wiki/ML_(programming_language)")

    print(article.parse_title() + "\n")
    print(article.parse_article())
