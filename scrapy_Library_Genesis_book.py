import scrapy

class LibSpider(scrapy.Spider):
    name = "book"
    start_urls = [
        'http://gen.lib.rus.ec/',
    ]

    def parse(self, response):
        return (scrapy.FormRequest.from_response(response,
                                                 formdata={'req': 'wiley', 'res': '100'},
                                                 callback = self.get_book_list))
    def get_book_list(self, response):
        book_num = response.xpath('//tr/td/font[@size="2"]/text()').extract_first()
        book_num = int(book_num.split()[0])
        print(book_num)
        for i in range(1, book_num // 100):
            yield (scrapy.FormRequest.from_response(response,
                                                    formdata={'page': str(i)},
                                                    callback = self.show_search))

    def show_search(self, response):
        book_list = response.xpath("//tr/td[@width=500]/a[@title='']/text()").extract()
        for book_name in set(book_list):
            yield {'title': book_name}
