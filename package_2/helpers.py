# %%
import package_2.constants as c2
import package_2.classes as cl
from decimal import *
import pycurl
import certifi
from io import BytesIO

def tryconvert(value, default, *types):
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError, InvalidOperation):
            continue
    return default

def load_from_text_to_dict():
    getcontext().prec = c2.decimal_prec
    S2f = lambda X: tryconvert(X,X,Decimal)
    new_list = []
    met_file = open(c2.met_file)
    for line in met_file:
        name, CONC, SD, LB, UP, OOM  = list(map(S2f,line.split("\t")))
        
        comp_obj = cl.Compound(name,CONC*OOM,SD*OOM)
        new_list.append(comp_obj)
    return new_list

def get_url(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body.decode("utf-8").rstrip()
