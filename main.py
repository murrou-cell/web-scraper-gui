from tkinter import *
from tkinter.ttk import *
class XSearch:
    def __init__(self,keyword):
        self.keyword = keyword
    def Search(self):
        cards = []
"""SCRIPT FOR SCRAPING"""
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
            res = threadp.apply_async(XSearch.Search, (XSearch(ent.get()),))
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
        window.title('TITLE')
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