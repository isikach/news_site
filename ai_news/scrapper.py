import re

import requests
from bs4 import BeautifulSoup
from requests import Response

AVAILABLE_SITES = {
    "en.wikipedia.org": 5,
    "www.washingtonpost.com": 9,
    "news.mit.edu": 5,
}


class Tag:
    def __init__(self, tag_name: str, class_name: str = None) -> None:
        self.tag_name = tag_name
        self.class_name = class_name


class GeneralScrapper:

    TITLE_TAG = "TAG"
    ARTICLE_TAG = "ARTICLE"
    HREF_TAG = "hide-for-print"
    NOT_ARTICLE = "Not found"

    def __init__(
        self,
        url: str,
        title_tags: Tag = None,
        article_tags: Tag = None,
        href_tag: str = None,
        response: Response = None,
        soup: BeautifulSoup = None,
        not_article_message: str = None,
    ):
        self.url = url
        if title_tags is None:
            self.title_tags = self.TITLE_TAG
        if article_tags is None:
            self.article_tags = self.ARTICLE_TAG
        if not href_tag:
            self.href_tag = self.HREF_TAG
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        if not not_article_message:
            self.not_article_message = self.NOT_ARTICLE

    def check_if_article(self):
        not_found = self.soup.find_all(string=self.not_article_message)
        return not not_found

    def parse_article(self) -> str:
        row_article = self.soup.find_all(
            self.article_tags.tag_name,
            class_=self.article_tags.class_name
        )
        all_text = []
        for p in row_article:
            if p.find(class_=self.href_tag):
                continue
            if not p:
                continue
            string = re.sub(r"\[.*?\]", "", p.text)
            all_text.append(string)
        return "\n".join(all_text)

    def parse_title(self) -> str:
        row_title = self.soup.find_all(
            self.title_tags.tag_name, class_=self.title_tags.class_name
        )
        return row_title[0].text


class WashingtonPostsScrapper(GeneralScrapper):

    TITLE_TAG = Tag("span", "PJLV")
    ARTICLE_TAG = Tag("div", "wpds-c-PJLV article-body")
    HREF_TAG = "hide-for-print"
    NOT_ARTICLE = "You stumped us. But here are some of our most-read stories that may interest you."

    def check_if_article(self):
        not_found = self.soup.find_all("div", id="page-not-found-text")
        return not not_found


class MitScrapper(GeneralScrapper):

    TITLE_TAG = Tag("h1")
    NOT_ARTICLE = "Page not found"
    HREF_TAG = "hide-for-print"
    ARTICLE_TAG = Tag(
                "div",
                "paragraph paragraph--type--content-block-text paragraph--view-mode--default",
            )


class WikipediaScrapper(GeneralScrapper):

    TITLE_TAG = Tag("span", "mw-page-title-main")
    ARTICLE_TAG = Tag("p")
    HREF_TAG = "hide-for-print"
    NOT_ARTICLE = (
                "Wikipedia does not have an article with this exact name."
            )

    def parse_title(self) -> str:
        row_title = self.soup.find(
            self.title_tags.tag_name, class_=self.title_tags.class_name
        )
        return row_title.text
