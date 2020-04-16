from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import quote as q
from tkinter import *
from tkinter.ttk import *
class OLXearch:
    def __init__(self,keyword):
        self.keyword = keyword
    def Search(self):
        cards = []
        listingsURL = []
        pagenum = '1'
        try:
            site = requests.get('https://www.olx.bg/ads/q-' + q(self.keyword))
            pagenum = bs(site.content, "lxml").find("a", {"data-cy": "page-link-last"}).find('span').find(text=True)
        except:
            pass
        counter = []
        count = 0
        while count < int(pagenum):
            count = count + 1
            counter.append(count)
        for number in counter:
            search = requests.get('https://www.olx.bg/ads/q-'+q(self.keyword)+'/?page='+str(number))
            home = bs(search.content, "lxml")
            listings = home.find_all("a", {"data-cy": "listing-ad-title"})
            for listing in listings:
                if listing['href'][-8:] != 'promoted':
                    listingsURL.append(listing['href'])
                    print(len(listingsURL))
        for listing in listingsURL:
            url=requests.get(listing)
            home = bs(url.content, "lxml")
            title=price=address=data=name=link=''
            try:
                title = home.find('h1').find(text=True).strip()
                address = home.find('address').find("p").find(text=True).strip()
                data = home.find('div',{"id":"textContent"}).find(text=True).strip()
                name = home.find('div',{"class", "offer-user__actions"}).find('h4').find('a').find(text=True).strip()
                link = listing
                price = home.find('strong', {"class": "pricelabel__value"}).find(text=True).strip()
            except:
                pass

            card = {
                "Title":title,
                "Price":price,
                "Address":address,
                "Description":data,
                "Name" :name,
                "Link" :link
            }
            cards.append(card)
        return cards

class GUI:
    def __init__(self):
        pass
    def Start():
        from multiprocessing.pool import ThreadPool
        import _thread
        import pandas as pd
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        def process():
            threadp = ThreadPool(processes=1)
            res = threadp.apply_async(OLXearch.Search, (OLXearch(ent.get()),))
            return_val = res.get()
            df = pd.DataFrame(return_val)
            global df_forexpor
            df_forexpor = df
            btn2.pack(side=TOP, fill=BOTH)
            txt.insert(INSERT, df)
            progres.stop()

        def launch():
            _thread.start_new_thread(process, ())
        def click():
            txt.delete(1.0, END)
            launch()
            progres.start()

        def export():
            df_forexpor.to_csv(ent.get()+'.csv')
        window = Tk()
        window.title('OLX')
        window.resizable(height=None, width=None)
        ent = Entry(window, width=10)
        ent.pack(side=TOP, fill=BOTH)
        ent.insert(0, "Type here")

        scrollbar = Scrollbar(window, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)

        txt = Text(window, wrap=NONE, xscrollcommand=scrollbar.set)
        txt.pack(side=TOP, fill=BOTH)
        scrollbar.config(command=txt.xview)

        btn = Button(window, text="Start", command=click)
        btn.pack(side=TOP, fill=BOTH)

        progres = Progressbar(window, orient='horizontal', length=10)
        progres.pack(side=TOP, fill=BOTH)

        btn2 = Button(window, text="Export CSV", command=export)
        window.mainloop()
GUI.Start()