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
    def __init__(
        self,
        url: str = None,
        title_tags: Tag = None,
        article_tags: Tag = None,
        href_tag: str = None,
        response: Response = None,
        soup: BeautifulSoup = None,
        not_article_message: str = None,
    ):
        self.url = url
        self.title_tags = title_tags
        self.article_tags = article_tags
        self.href_tag = href_tag
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.not_article_message = not_article_message

    def check_if_article(self):
        not_found = self.soup.find_all(string=self.not_article_message)
        return not not_found

    def parse_article(self) -> str:
        row_article = self.soup.find_all(
            self.article_tags.tag_name, class_=self.article_tags.class_name, limit=5
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
        super().__init__(
            url=url,
            title_tags=title_tags,
            article_tags=article_tags,
            href_tag=href_tag,
            response=response,
            soup=soup,
            not_article_message=not_article_message,
        )
        if title_tags is None:
            self.title_tags = Tag("span", "PJLV")
        if article_tags is None:
            self.article_tags = Tag("div", "wpds-c-PJLV article-body")
        if not href_tag:
            self.href_tag = "hide-for-print"
        if not not_article_message:
            self.not_article_message = "You stumped us. But here are some of our most-read stories that may interest you."

    def check_if_article(self):
        not_found = self.soup.find_all("div", id="page-not-found-text")
        return not not_found


class MitScrapper(GeneralScrapper):
    def __init__(
        self,
        url: str,
        title_tags: Tag = None,
        article_tags: Tag = None,
        href_tag: str = None,
        response: Response = None,
        soup: BeautifulSoup = None,
        not_article_message: str = None,
    ) -> None:
        super().__init__(
            url=url,
            title_tags=title_tags,
            article_tags=article_tags,
            href_tag=href_tag,
            response=response,
            soup=soup,
            not_article_message=not_article_message,
        )
        if title_tags is None:
            self.title_tags = Tag("h1")
        if article_tags is None:
            self.article_tags = Tag(
                "div",
                "paragraph paragraph--type--content-block-text paragraph--view-mode--default",
            )
        if href_tag is None:
            self.href_tag = "hide-for-print"
        if not_article_message is None:
            self.not_article_message = "Page not found"


class WikipediaScrapper(GeneralScrapper):
    def __init__(
        self,
        url: str,
        title_tags: Tag = None,
        article_tags: Tag = None,
        href_tag: str = None,
        response: Response = None,
        soup: BeautifulSoup = None,
        not_article_message: str = None,
    ) -> None:
        super().__init__(
            url=url,
            title_tags=title_tags,
            article_tags=article_tags,
            href_tag=href_tag,
            response=response,
            soup=soup,
            not_article_message=not_article_message,
        )
        if not title_tags:
            self.title_tags = Tag("span", "mw-page-title-main")
        if not article_tags:
            self.article_tags = Tag("p")
        if not href_tag:
            self.href_tag = "hide-for-print"
        if not not_article_message:
            self.not_article_message = (
                "Wikipedia does not have an article with this exact name."
            )

    def parse_title(self) -> str:
        row_title = self.soup.find(
            self.title_tags.tag_name, class_=self.title_tags.class_name
        )
        return row_title.text
