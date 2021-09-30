import scrapy
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
# import selenium
from bs4 import BeautifulSoup
import requests_html
import re
import time


class AppsiteSpider(scrapy.Spider):
    name = 'appsite'
    allowed_domains = ['contest-646508-5umjfyjn4a-ue.a.run.app/listing']
    start_urls = ['https://contest-646508-5umjfyjn4a-ue.a.run.app/listing']

    urlnofinal = 'https://contest-646508-5umjfyjn4a-ue.a.run.app/listing'
    urlnolisting = 'https://contest-646508-5umjfyjn4a-ue.a.run.app'

    session = requests_html.HTMLSession()

    # exitset = list()

    def parse(self, response):
        def get_site(url, render=False):
            try:
                response = self.session.get(self.urlnofinal + url, timeout=6) # no /
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as exc:
                print(f'bad response: {exc}, {self.urlnofinal + url} ') # DEBUG
                return get_site(url)

            if render:
                response.html.render()
                time.sleep(3)

            return BeautifulSoup(response.text, features='html.parser')

        def get_json(url):
            try:
                # print('urljson: ', self.urlnolisting + url) # DEBUG
                response = self.session.get(self.urlnolisting + url, timeout=6) # no /
            except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as exc:
                print(f'bad response: {exc}, {self.urlnofinal + url} ') # DEBUG
                return get_json(url)

            return response.json()


        soup = BeautifulSoup(response.text, features='html.parser')
            
        def extract(soup, page=0):

            for item in soup.find_all('div', {'class': 'item'}):
                output = dict()

                # ITEM_NAME
                try:
                    name = str(item.find('h2').text)
                    output['name'] = name

                    if re.search(
                        r'next\s*page',
                        name,
                        re.I | re.M
                    ) or re.search(
                        r'previous\s*page',
                        name,
                        re.I | re.M
                    ):
                        continue

                except:
                    output['name'] = None


                # URL ITEM
                urlsite = str(item.find('a').get('href'))


                # ITEM_ID
                try:
                    output['item_id'] = re.search(
                        r'i\/([^\"]*)$',
                        urlsite,
                        re.I | re.M
                    )[1]

                except:
                    print('ERRO!: ' + urlsite)
                    break

                # output['url'] = urlsite # DEBUG


                # ITEM SOUP
                newsoup = get_site(
                    '/i/' + output['item_id']
                )


                # FLAVOR
                try:
                    json_id = newsoup.find('span', {'class': 'flavor'}).get('data-flavor')
                    
                    output['flavor'] = get_json(
                        json_id
                    )['value']

                except:
                    flavor = None

                    for item in newsoup.findAll('p'):
                        if 'Flavor:' in str(item):
                            flavor = item.find('span').text
                            if flavor == output['item_id'] or re.search(
                                r'^\d$',
                                flavor,
                                re.I | re.M
                            ):
                            
                            # or re.search(
                            #     r'none', # não faz diferenca
                            #     flavor,
                            #     re.I | re.M
                            # ):
                            # or re.search( # ERRADO
                            #     rf'{name}',
                            #     flavor,
                            #     re.M #
                            # ):

                            # or re.search( # ERRADO!
                            #     r'^\d*$',
                            #     flavor,
                            #     re.I | re.M
                            # ): 
                                flavor = None
                            
                            break

                    output['flavor'] = flavor

                # RIGHT IMAGE
                slide2 = newsoup.find('div', {'id': '2'})
                

                # IMAGE_ID
                try:
                    imageurl = str(slide2.find('img').get('src'))
                    output['image_id'] = re.search(
                        r'gen\/([^\.]*)\.',
                        imageurl,
                        re.I | re.M
                    )[1]
                
                except:
                    output['image_id'] = None

                # if output not in self.exitset:
                #     self.exitset.append(output)
                # else:
                #     print(page)

                yield output
                
                # else: #sem dif?
                #     print(
                #         '1: ', output,
                #         '2: ', [ x for x in self.exitset if x == output ][0]
                #     )

                # Assumindo que é sempre 66 páginas

            for tag in soup.find_all('a'):
                if re.search(
                    r'next\s*page',
                    str(tag),
                    re.I | re.M):

                    try:
                        nextpage = re.search(
                            r'\?.*?\=(.*)$',
                            str(tag.get('href')),
                            re.I | re.M
                        )[1]
                    except Exception as exc:
                        # print(exc) # DEBUG
                        break
                    
                    if nextpage == page:
                        print(page) # DEBUG
                        break

                    # nota: nao fazer assim no mundo real
                    # for item in extract(
                    #     get_site(
                    #         f'?page={nextpage}'
                    #     ),
                    #     nextpage
                    # ):
                    #     yield item 
                    yield from extract(
                        get_site(
                            f'?page={nextpage}'
                        ),
                        nextpage
                    )

                
                # break

        yield from extract(soup, 0)
