# Ejecutar en TERMINAL py:

# python -m scrapy.cmdline runspider Scrapper\items.py


import scrapy
from scrapy.loader import ItemLoader
import csv

class spider1(scrapy.Spider):
    name = "Spider"
    #Formato de la data exportada
    custom_settings = {
         'FEED_FORMAT': 'json',
         'FEED_URI': 'scrappedData.json'
    }

    #Array que utiliza la clase Spider para guardar los links a los que ingresara
    start_urls = []

    #Archivo de donde se extraen los links iniciales que usa el Scrapper
    f = open('C:\\Users\\DELL\\new_scrapy\\majestic_million.csv', 'r')

    #Este loop inserta en el array los links dentro del CSV
    for i in f:
        u = i.split('\n')
        start_urls.append(u[0])
    
    #Funcion que retorna los HTML scrapeados
    # response contiene el HTML
    def parse(self, response):

        titles = response.xpath("///a/text()").extract()
        urls= (response.xpath("////@href").extract())
        meta = response.xpath('/html/head/meta[@name="description"]/@content').extract()
        url= (response.url)
        titlee = response.xpath('/html/head/title/text()').extract()

        num=0
        #En este array se guardaran todos los nuevos enlaces que el crawler
        #encuentre en las paginas que registre y luego se convertira en 
        #la variable start_urls
        newurls=[]
        i=40  #Esta variable se utiliza para indicar en que parte de la lista de links
        #queremos que el scraper inicie

        while i < (len(self.start_urls)):
            for title, url in zip(titles, urls):
                if title.strip() != '':
                    num=num+1
                    if len(url.split('http'))>1:
                        url= url
                    else:
                        url= self.start_urls[i] + url
                    yield {'path': url, 'title': titlee,'description': [meta,titles]}
                    newurls.append(url)
            if i == 60:
                self.start_urls = newurls
            i=i+1


#python -m scrapy.cmdline runspider Scrapper\items.py