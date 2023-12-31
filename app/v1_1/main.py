"""
..
  The app for our website
  03/2023
  Marine Delaborde, Mathieu Dehouck
"""
from sys import path
path.append('..')
path.append('../..')
from typing_extensions import Annotated
from typing import Union
from pydantic import BaseModel
from random import randint

from fastapi import FastAPI, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.v1_1.aligator_core import find, atrandom, lastjokes, save

app = FastAPI()

templates = Jinja2Templates(directory="../front/")


app.mount("/aligator/styles", StaticFiles(directory="../front/styles/"), name="styles")


@app.get('/Logo/Social/Favicon/FaviconLogo.png')
@app.get('/aligator/Logo/Social/Favicon/FaviconLogo.png')
@app.get('/aligator/Logo/Social/Favicon/FaviconLogo.png')
@app.get('/favicon.ico')
def fav():
    #return RedirectResponse('/styles/favicon.png')
    return RedirectResponse('/styles/Logo/Social/Favicon/FaviconLogo.png')


@app.get('/alphabet.js')
@app.get('/aligator/alphabet.js')
def fav():
    #try:
    return RedirectResponse('/aligator/styles/alphabet.js')
    #except:
    #    return RedirectResponse('/aligator/styles/alphabet.js')
    
@app.get('/integration-github.js')
@app.get('/aligator/integration-github.js')
def fav():
    #try:
    return RedirectResponse('/aligator/styles/integration-github.js')
    #except:
    #    return RedirectResponse('/aligator/styles/integration-github.js')


"""
the session id will be used to avoid showing 20 times the same joke to someone and asking them to rate them again and again, but we do not store them beyond the session
"""

@app.get('/')
@app.get('/main.html')
@app.get('/aligator')
@app.get('/aligator/main.html')
def root(req: Request, session:Union[None, int]=None):
    return templates.TemplateResponse('main.html', {'request':req})


@app.get('/top5.html')
@app.get('/aligator/top5.html')
def top(req: Request, session:Union[None, int]=None):
    return templates.TemplateResponse('top5.html', {'request':req})


@app.get('/credits.html')
@app.get('/aligator/credits.html')
def credits(req: Request, session:Union[None, int]=None):
    return templates.TemplateResponse('credits.html', {'request':req})


@app.get('/lea-toire.html')
@app.get('/aligator/lea-toire.html')
def aleatoire(req: Request, session:Union[None, int]=None):
    
    return templates.TemplateResponse('lea-toire.html', {'request':req, 'jokes':atrandom()})


#@app.get('/prenom')
@app.get('/prenom.html')
@app.get('/aligator/prenom.html')
#async def from_name(names: Annotated[str, Form()]):
def from_name(request: Request,
              name: Annotated[str, Query(max_length=50)]='',
              nameapi: Annotated[str, Query(max_length=50)]='',
              jokeid:str='-1',
              saved:str='',
              rate:int=-1,
              comp:str='',
              sensible:str='',
              remarks:str='',
              session:Union[None, int]=None):

    if jokeid != '-1':
        #print(name, nameapi, jokeid, rate, comp, sensible, remarks, sep=',\t')
        #print(lastjokes)

        save(name, nameapi, jokeid, rate, comp, sensible, remarks)

        saved = saved + str(jokeid)
        saved = ''.join(sorted(saved))
        print(saved)

        return templates.TemplateResponse('template_prenom.html', {'request':request, 'jokes':lastjokes['jokes'],
                                                                   'name':name, 'nameapi':nameapi, 'found':True, 'answer':'', 'saved':saved})
    
    if name == '' and nameapi == '':
        return templates.TemplateResponse('template_prenom.html', {'request':request, 'jokes':[], 'name':'', 'nameapi':''})

    elif nameapi != '':
        found, api, jokes = find(name, api=nameapi)
        with open('/home/mdehouck/aligator/incoming/TOADD', 'a') as f:
            print(name, nameapi, sep='\t', file=f)
    
    elif name != '':
        found, api, jokes = find(name, api='')

        
    if found:
        return templates.TemplateResponse('template_prenom.html', {'request':request, 'jokes':jokes, 'name':name, 'nameapi':api, 'found':found, 'answer':''})
    return templates.TemplateResponse('template_prenom.html', {'request':request, 'jokes':[], 'name':name, 'nameapi':api, 'found':found, 'answer':jokes})
