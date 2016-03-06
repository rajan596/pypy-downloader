'''
PYTHON 3.4
Content Downloader

Issues to be solved : URLParsering

'''

import urllib.request, urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
import os
import re
import json

repeated_search=False

'''
Get current time in Year-Month-Day-Hour-Month-Second format
'''
def get_current_time():
    d=datetime.now()
    times=[d.year,d.month,d.day,d.hour,d.minute,d.second]
    ctime=""
    for t in times:
        ctime+='-'+str(t)
    return ctime[1:]

'''
Download content specified by URL
'''
def download(url):
    page=get_content(url)
    name=url.split('/')[-1]
    print(url)
    success=False
    try:
        file=open(name,'wb')
        file.write(page)
        success=True
    except FileExistsError as f:
        name=name.split('.')[0] + get_current_time() + name.split('.')[1]  ## file.jpg
        file=open(name,'wb')
        file.write(page)
        success=True
    except Exception as e:
        print(str(e))
    finally:
        file.close()

    return success

'''
fetched Response by Requesting URL 
'''

def get_content(url):
    header={'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    req=urllib.request.Request(url,headers=header)
    page=urllib.request.urlopen(req).read()
    return page

'''
make new directory and save downloads there
'''
def change_directory():
    path=os.getcwd()
    new_dir=get_current_time()
    os.mkdir(new_dir)
    path=path+'/'+new_dir
    os.chdir(path)
    print(path)

'''
Downloads Images specified by Google search Images 
'''
def download_images_from_url(links):
    downloaded_files=0
    failure=0
    for link in links:
        try:
            if link.get('class')[0]=='rg_l':
                flink=str(link.get('href'))
                flink=flink.split('&')[0]
                flink=flink.split('?')[1][7:]
                if download(flink)==True:
                    print(downloaded_files+1,' downloaded...' + flink.split('/')[-1])
                    downloaded_files+=1
                else:
                    failure+=1
                
        except Exception as e:
            print(str(e))
            failure+=1
    

def download_content_from_url(url):
    try:
        data=get_content(url).decode("utf-8")
        data=json.loads(data)
        data=data['responseData']['results']

        success=0;
        failure=0
        for link in data:
            try:
                if download(link['url'])==True:
                    success+=1
                else:
                    failure+=1
            except Exception as e:
                failure+=1
    except Exception as e:
        pass

    
'''
Download all files specified by Web page URL
'''
def download_all_files_from_url(url):
        
    page=get_content(url)
    soup=BeautifulSoup(page)
    #print(soup.prettify())
    links=soup.find_all("a")

    # content link pdf, ppt, docs will be downloaded
    download_content_from_url(url)
    
    # download images from google search image url
    download_images_from_url(links)

'''
Downloads documents by query 
'''
def download_by_query():
    qq=input("Search for : ")
    no_of_files=int(input("No. of files : "))

    query=urllib.parse.urlencode({'q':qq})
    repeated_search=True
    url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&start=%s"

    for i in range(1,no_of_files,4):
        furl=url%(query,str(i))
        download_all_files_from_url(furl)

def get_url():
    url=input("Enter URL : ")
    return url

def menu():
    print("1. Download by Search [ pdf-ppt- doc ] :")
    print('2. Download by Google Image search URL [full-url]:')

    opt=input("Your choice : ")

    change_directory()

    if opt=="1":
        download_by_query()
    else :
        download_all_files_from_url(get_url())

    print('Download completed...')

if __name__=='__main__':
    menu()
    
''' 
url='http://orig02.deviantart.net/d778/f/2012/147/5/e/the_dark_knight_rises___batman_by_dskorn-d51ahxm.jpg'
download(url)

url='http://cslibrary.stanford.edu/103/LinkedListBasics.pdf'
download(url)

url="https://www.google.co.in/search?q=ram&hl=en&biw=1366&bih=673&site=webhp&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjb__3VvarLAhWDVo4KHaDgAAoQ_AUIBigB"
url="https://www.google.co.in/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=linked%20list%20pdf"
url='https://www.google.co.in/search?q=shraddha+kapoor+hd+wallpapers&hl=en&biw=1356&bih=638&site=webhp&source=lnms&tbm=isch&sa=X&ved=0ahUKEwipmK-O16rLAhVHBY4KHd1AAZ4Q_AUIBigB'
url="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % ('LinkedListPdf')

'''
