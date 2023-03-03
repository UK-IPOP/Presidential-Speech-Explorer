import scrapy

class SpeechSpider(scrapy.Spider):
    name = "speeches"

    start_urls = [
        f"https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=&items_per_page=100&page={page}"
        for page in range(0, 1521)  # 1521 because exclusive
    ]

    def parse(self, response):
        speech_links = response.css(
            "td.views-field.views-field-title a::attr(href)"
        ).getall()
        yield from response.follow_all(speech_links, self.parse_speech)

    def parse_speech(self, response):
        person = response.css("h3.diet-title a::text").get()
        title = response.css("div.field-ds-doc-title h1::text").get()
        date = response.css(
            "div.field-docs-start-date-time span.date-display-single::text"
        ).get()
        content = response.css("div.field-docs-content p::text").getall()
        url = response.url

        yield {
            "person": person,
            "title": title,
            "date": date,
            "content": "\n".join(content),
            "url": url,
        }
