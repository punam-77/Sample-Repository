# Sample-Repository
My first project 

SCRAPING:
	Scrapy is a fast, open-source web crawling framework written in Python, used to extract the data from the web page with the help of selectors based on XPath.
	Web scraping is a technique used to extract data from websites through an automated process.
SCRAPY INSTALLATION:
	Install Python version > 2.7.
	Install PIP.	
	If you have anaconda or miniconda installed on your machine, run the below command to install Scrapy using conda −
	$conda install -c scrapinghub scrapy 
CRATING A PROJECT:
	To scrap the data from web pages, first you need to create the Scrapy project where you will be storing the code. To create a new directory, run the following command −
	scrapy startproject tutorial
	The above code will create a directory with name first_scrapy and it will contain the following structure −
	tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
OUR FIRST SPIDER:
	This is the code for our first Spider. Save it in a file named quotes_spider.py under the tutorial/spiders directory in your project:

	import scrapy
	class QuotesSpider(scrapy.Spider):
		name = "quotes"

		def start_requests(self):
			urls = [
			'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

		def parse(self, response):
			page = response.url.split("/")[-2]
			filename = 'quotes-%s.html' % page
			with open(filename, 'wb') as f:
			f.write(response.body)
			self.log('Saved file %s' % filename)
	To put our spider to work, go to the project’s top level directory and run:

		scrapy crawl quotes
	This command runs the spider with name quotes that we’ve just added, that will send some requests for the quotes.toscrape.com domain. You will get an output similar to this:
	... (omitted for brevity)
	2016-12-16 21:24:05 [scrapy.core.engine] INFO: Spider opened
	2016-12-16 21:24:05 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
	2016-12-16 21:24:05 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
	2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
	2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
	2016-12-16 21:24:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/2/> (referer: None)
	2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-1.html
	2016-12-16 21:24:05 [quotes] DEBUG: Saved file quotes-2.html
	2016-12-16 21:24:05 [scrapy.core.engine] INFO: Closing spider (finished)
	...
	Now, check the files in the current directory. You should notice that two new files have been created: quotes-1.html and quotes-2.html, with the content for the respective URLs, as our parse method instructs.

EXTRACTING DATA:
	The best way to learn how to extract data with Scrapy is trying selectors using the shell Scrapy shell. Run:
	$scrapy shell 'http://quotes.toscrape.com/page/1/'
	You will see something like:
	[ ... Scrapy log here ... ]
	2016-09-19 12:09:27 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
	[s] Available Scrapy objects:
	[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
	[s]   crawler    <scrapy.crawler.Crawler object at 0x7fa91d888c90>
	[s]   item       {}
	[s]   request    <GET http://quotes.toscrape.com/page/1/>
	[s]   response   <200 http://quotes.toscrape.com/page/1/>
	[s]   settings   <scrapy.settings.Settings object at 0x7fa91d888c10>
	[s]   spider     <DefaultSpider 'default' at 0x7fa91c8af990>
	[s] Useful shortcuts:
	[s]   shelp()           Shell help (print this help)
	[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
	[s]   view(response)    View response in a browser
	>>>
	Using the shell, you can try selecting elements using CSS with the response object:
	>>> response.css('title')
	[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
	The result of running response.css('title') is a list-like object called SelectorList, which represents a list of Selector objects that wrap around XML/HTML elements and allow you to run further queries to fine-grain the selection or extract the data.
	To extract the text from the title above, you can do:
	>>> response.css('title::text').extract()
	['Quotes to Scrape']
	There are two things to note here: one is that we’ve added ::text to the CSS query, to mean we want to select only the text elements directly inside <title> element. If we don’t specify ::text, we’d get the full title element, including its tags:
	>>> response.css('title').extract()
	['<title>Quotes to Scrape</title>']
	The other thing is that the result of calling .extract() is a list, because we’re dealing with an instance of SelectorList. When you know you just want the first result, as in this case, you can do:
	>>> response.css('title::text').extract_first()
	'Quotes to Scrape'
	As an alternative, you could’ve written:
	>>> response.css('title::text')[0].extract()
	'Quotes to Scrape'
	However, using .extract_first() avoids an IndexError and returns None when it doesn’t find any element matching the selection.
	There’s a lesson here: for most scraping code, you want it to be resilient to errors due to things not being found on a page, so that even if some parts fail to be scraped, you can at least get some data.
	Besides the extract() and extract_first() methods, you can also use the re() method to extract using regular expressions:
	>>> response.css('title::text').re(r'Quotes.*')
	['Quotes to Scrape']
	>>> response.css('title::text').re(r'Q\w+')
	['Quotes']
	>>> response.css('title::text').re(r'(\w+) to (\w+)')
	['Quotes', 'Scrape']
	In order to find the proper CSS selectors to use, you might find useful opening the response page from the shell in your web browser using view(response). You can use your browser developer tools or extensions like Firebug (see sections about Using Firebug for scraping and Using Firefox for scraping).
	
EXTRACTING QUOTES AND AUTHORS:
	Now that you know a bit about selection and extraction, let’s complete our spider by writing the code to extract the quotes from the web page.
	Each quote in http://quotes.toscrape.com is represented by HTML elements that look like this:

	<div class="quote">
		<span class="text">“The world as we have created it is a process of our
		thinking. It cannot be changed without changing our thinking.”</span>
		<span>
			by <small class="author">Albert Einstein</small>
			<a href="/author/Albert-Einstein">(about)</a>
		</span>
		<div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
		</div>
	</div>
	Let’s open up scrapy shell and play a bit to find out how to extract the data we want:
	$ scrapy shell 'http://quotes.toscrape.com'
	We get a list of selectors for the quote HTML elements with:
	>>> response.css("div.quote")
	Each of the selectors returned by the query above allows us to run further queries over their sub-elements. Let’s assign the first selector to a variable, so that we can run our CSS selectors directly on a particular quote:
	>>> quote = response.css("div.quote")[0]
	Now, let’s extract title, author and the tags from that quote using the quote object we just created:
	>>> title = quote.css("span.text::text").extract_first()
	>>> title
	'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
	>>> author = quote.css("small.author::text").extract_first()
	>>> author
	'Albert Einstein'
	Given that the tags are a list of strings, we can use the .extract() method to get all of them:
	>>> tags = quote.css("div.tags a.tag::text").extract()
	>>> tags
	['change', 'deep-thoughts', 'thinking', 'world']
	Having figured out how to extract each bit, we can now iterate over all the quotes elements and put them together into a Python dictionary:
	>>> for quote in response.css("div.quote"):
	...     text = quote.css("span.text::text").extract_first()
	...     author = quote.css("small.author::text").extract_first()
	...     tags = quote.css("div.tags a.tag::text").extract(	)
	...     print(dict(text=text, author=author, tags=tags))
	{'tags': ['change', 'deep-thoughts', 'thinking', 'world'], 'author': 'Albert Einstein', 'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'}
	{'tags': ['abilities', 'choices'], 'author': 'J.K. Rowling', 'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”'}
    ... a few more of these, omitted for brevity
	>>>
EXTRACTING DATA IN OUR SPIDER:
	Let’s get back to our spider. Until now, it doesn’t extract any data in particular, just saves the whole HTML page to a local file. Let’s integrate the extraction logic above into our spider.
	A Scrapy spider typically generates many dictionaries containing the data extracted from the page. To do that, we use the yield Python keyword in the callback, as you can see below:
	import scrapy
	class QuotesSpider(scrapy.Spider):
		name = "quotes"
		start_urls = [
			'http://quotes.toscrape.com/page/1/',
			'http://quotes.toscrape.com/page/2/',
				]

		def parse(self, response):
			for quote in response.css('div.quote'):
				yield {
					'text': quote.css('span.text::text').extract_first(),
					'author': quote.css('small.author::text').extract_first(),
					'tags': quote.css('div.tags a.tag::text').extract(),
					}
	If you run this spider, it will output the extracted data with the log:
	2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/1/>
	{'tags': ['life', 'love'], 'author': 'André Gide', 'text': '“It is better to be hated for what you are than to be loved for what you are not.”'}
	2016-09-19 18:57:19 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/1/>
	{'tags': ['edison', 'failure', 'inspirational', 'paraphrased'], 'author': 'Thomas A. Edison', 'text': "“I have not failed. I've just found 10,000 ways that won't work.”"}
STORING THE SCRAPED DATA:
	The simplest way to store the scraped data is by using Feed exports, with the following command:
	$scrapy crawl quotes -o quotes.json
	That will generate an quotes.json file containing all scraped items, serialized in JSON.
	


