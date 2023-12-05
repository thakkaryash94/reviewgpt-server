import scrapy
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import re


def get_collection(collection_name):
    client = chromadb.HttpClient(host="127.0.0.1", port=8000)
    # embedding = embedding_functions.OpenAIEmbeddingFunction(
    #     model_name="text-embedding-ada-002"
    # )
    collection = client.get_or_create_collection(name=collection_name)
    return collection


TITLE_CLASS_ID = "review-title"
REVIEW_TEXT_CLASS_ID = "review-body"
AUTHOR_CLASS_ID = "a-profile-name"
DATE_CLASS_ID = "review-date"
VERIFIED_CLASS_ID = "avp-badge"
RATING_CLASS_ID = "review-star-rating"

REVIEWS_CLASS_ID = "review"
REVIEW_ID_CLASS_ID = "id"
NEXT_PAGE_CLASS_ID = "a-last"


class Amazon(scrapy.Spider):
    name = "amazon"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    current_page = 1

    def __init__(self, url=None, *args, **kwargs):
        super(Amazon, self).__init__(*args, **kwargs)
        self.start_urls = [f"{url}"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers=self.headers,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "errback": self.errback,
            },
        )

    async def parse(self, response):
        print(f"*************Parsing {response.url}****************************")
        page = response.meta["playwright_page"]
        average_rating_text = response.xpath(
            './/i[@data-hook="average-star-rating"]/span[1]/text()'
        ).get()
        # print(re.findall(r"[-+]?(?:\d*\.*\d+)", average_rating_text))
        print(f"============{self.current_page} started============")
        reviews = response.xpath(f'//div[@data-hook="{REVIEWS_CLASS_ID}"]')
        collection = get_collection("amz_reviews")
        for review_item in reviews:
            id = review_item.xpath(f".//@{REVIEW_ID_CLASS_ID}").get()
            created_at_string = review_item.xpath(
                f'.//span[@data-hook="{DATE_CLASS_ID}"]/text()'
            ).get()
            author = review_item.xpath(
                f'.//span[@class="{AUTHOR_CLASS_ID}"]/text()'
            ).get()
            rating_text = review_item.xpath(
                f'.//i[@data-hook="{RATING_CLASS_ID}"]/span[1]/text()'
            ).get()
            title = review_item.xpath(
                f'.//a[@data-hook="{TITLE_CLASS_ID}"]/span[2]/text()'
            ).get()
            text = "".join(
                review_item.xpath(
                    f'.//span[@data-hook="{REVIEW_TEXT_CLASS_ID}"]/span/text()'
                ).getall()
            )
            is_verified = bool(
                review_item.xpath(
                    f'.//span[@data-hook="{VERIFIED_CLASS_ID}"]/text()'
                ).get()
                is not None
            )
            ratings = re.findall(r"(?:\d*\.*\d+)", rating_text)
            rating = float(ratings[0].replace(",", "."))
            rating_limit = float(ratings[1].replace(",", "."))
            created_at = datetime.strptime(
                created_at_string.split(" on ")[1], "%d %B %Y"
            ).isoformat()
            collection.add(
                documents=text,
                metadatas={
                    "title": title,
                    "author": author,
                    "is_verified": is_verified,
                    "rating": rating,
                    "rating_limit": rating_limit,
                    "created_at": created_at,
                },
                ids=id,
            )
            print(f"{id} record inserted")
        print(f"============{self.current_page} ended============")
        next_page_url = response.xpath(
            f'.//li[@class="{NEXT_PAGE_CLASS_ID}"]/a/@href'
        ).get()
        print(f"--------next_page_url---------------{response.urljoin(next_page_url)}")
        if next_page_url is not None:
            self.current_page = self.current_page + 1
            if self.current_page <= 5:
                yield scrapy.Request(
                    url=response.urljoin(next_page_url),
                    callback=self.parse,
                    headers=self.headers,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "errback": self.errback,
                    },
                )
        else:
            print("*************No Page Left*************")

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
