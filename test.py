from googlesearch import search
from mechanize import Browser

br = Browser()


for result in search('discord', tld='com', num=10, stop=10, pause=2):
    print(result)
    br.open(result)
    print(br.title())