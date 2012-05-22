import otter

def run0():
    r = otter.Resource('top')
    pages = r(thresh='top20k',type='tweet',local='en')
    items = []
    for i,p in enumerate(pages):
        if i > 10: return
        items.extend(page.response.list)
