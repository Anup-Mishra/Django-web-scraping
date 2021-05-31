from asyncio.windows_events import NULL
from django.contrib.auth.hashers import check_password,make_password
import re
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
# Create your views here.
from bs4 import BeautifulSoup
import requests
import time, asyncio
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def convert(a):
    b=a.replace(" ",'')
    c=b.replace("INR",'')
    d=c.replace(",",'')
    f=d.replace("₹",'')
    g=int(float(f))
    return g
@sync_to_async
def flipkart(name):
    try:
        global flipkart2
        name1 = name.replace(" ","+")   #iphone x  -> iphone+x
        flipkart2=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',headers=headers)
        print("\nSearching in flipkart....")
        soup = BeautifulSoup(res.text,'html.parser')
        flipkart_name = soup.select('._4rR01T')[0].getText().strip() ### New Class For Product Name
        flipkart_name = flipkart_name.upper()
        if name.upper() in flipkart_name:
            flipkart_img = soup.select('._396cs4')[0]['src']
            flipkart_price = soup.select('._1_WHN1')[0].getText().strip()  ### New Class For Product Price
            flipkart_price=convert(flipkart_price)
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()
            flipKart_info = [flipkart_img,flipkart_name,flipkart_price,flipkart2]
        else:
            flipKart_info = ['No Product Found']
    except Exception as e:
        print('flipkart',e)
        flipKart_info = ['No Product Found']
    return flipKart_info
@sync_to_async
def amazon(name):
    try:
        global amazon2
        name1 = name.replace(" ","-")
        name2 = name.replace(" ","+")
        amazon2=f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(f'https://www.amazon.in/{name1}/s?k={name2}',headers=headers)
        print("\nSearching in amazon:")
        soup = BeautifulSoup(res.text,'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = int(len(amazon_page))
        for i in range(0,amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
            if name in amazon_name[0:20]:
                amazon_img = soup.select('.s-image')[i]['src']
                amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip().upper()
                amazon_price = soup.select('.a-price-whole')[i].getText().strip().upper()
                amazon_price=convert(amazon_price)
                print("Amazon:")
                amazon_info = [amazon_img,amazon_name,amazon_price,amazon2]
                break
            else:
                i+=1
                i=int(i)
                if i==amazon_page_length:
                    amazon_info = ["No Product Found"]
                    break
    except Exception as e:
        print('amazon',e)
        amazon_info = ["No Product Found"]
    return amazon_info
@sync_to_async
def olx(name):
    try:
        global olx2
        name1 = name.replace(" ","-")
        olx2=f'https://www.olx.in/items/q-{name1}?isSearchCall=true'
        res = requests.get(f'https://www.olx.in/items/q-{name1}?isSearchCall=true',headers=headers)
        print("\nSearching in OLX......")
        soup = BeautifulSoup(res.text,'html.parser')
        olx_name = soup.select('._2tW1I')
        olx_page_length = len(olx_name)
        for i in range(0,olx_page_length):
            olx_name = soup.select('._2tW1I')[i].getText().strip()
            name = name.upper()
            olx_name = olx_name.upper()
            if name in olx_name:
                olx_img = soup.select('._3Kg_w')[i]['src']
                olx_price = soup.select('._89yzn')[i].getText().strip()
                olx_price=convert(olx_price)
                olx_name = soup.select('._2tW1I')[i].getText().strip()
                olx_loc = soup.select('.tjgMj')[i].getText().strip()
                try:
                    label = soup.select('._2Vp0i span')[i].getText().strip()
                except:
                    label = "OLD"
                
                print("Olx:")
                olx_info = [olx_img,olx_name,olx_price,olx2,olx_loc,label]
                break
            else:
                i+=1
                i=int(i)
                if i==olx_page_length:
                    olx_info = ["No Product Found"]
                    break
    except Exception as e:
        print('olx',e)
        olx_info = ["No Product Found"]
    return olx_info
@sync_to_async
def paytm(name):
    try:
        name1 = name.replace(" ","+")
        global paytm2
        paytm2=f'https://paytmmall.com/shop/search?q={name1}&from=organic&child_site_id=6&site_id=2&category=66781&brand=509904'
        res = requests.get(f'https://paytmmall.com/shop/search?q={name1}&from=organic&child_site_id=6&site_id=2&category=66781&brand=509904',headers=headers)
        print("\nSearching in paytm-mall:")
        soup = BeautifulSoup(res.text,'html.parser')
        paytm_page = soup.select('.UGUy')
        paytm_page_length = int(len(paytm_page))
        for i in range(0,paytm_page_length):
            name = name.upper()
            paytm_name = soup.select('.UGUy')[i].getText().strip().upper()
            if name in paytm_name[0:20]:
                paytm_img = soup.select('div._3nWP > img')[i]['src']
                paytm_name = soup.select('.UGUy')[i].getText().strip().upper()
                paytm_price = soup.select('._1kMS')[i].getText().strip().upper()
                paytm_price=convert(paytm_price)
                print("Paytm:")
                paytm_info = [paytm_img,paytm_name,paytm_price,paytm2]
                break
            else:
                i+=1
                i=int(i)
                if i==paytm_page_length:
                    paytm_info = ["No Product Found"]
                    break
    except Exception as e:
        print('EPaytm',e)
        paytm_info = ["No Product Found"]
    return paytm_info
async def comparison(request):
    result=[]
    if(request.method=='POST'):
        tstart_time = time.time()
        name= request.POST["productname"]
        try:
            flipkart1,amazon1,olx1,paytm1 = await asyncio.gather(flipkart(name),amazon(name),olx(name),paytm(name))
            result = {'amazon':amazon1,'paytm': paytm1,'flipkart':flipkart1,'olx':olx1}
            to_compare = []
            for key,t in result.items():
                if len(t)>1:
                    to_compare.append(t[2])
            min_price = min(to_compare)
            for key,t in result.items():
                if len(t)>1 and t[2]==min_price:
                    min_price_holder = [key,t]
                    break
            print([flipkart1,amazon1,olx1,paytm1])
            print(time.time()-tstart_time)
            return render(request,'index.html',{ 'context': result, 'min_price_holder': min_price_holder, 'authenticated': True} )
        except Exception as e:
            print(e)
            return render(request,'err.html')
    return render(request,'index.html',{ 'context': result, 'authenticated': False })

def signup(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        if len(username) < 5:
            messages.info(request,'Enter a valid username')
            return redirect('/')
        elif password!=password1:
            messages.info(request,'Both Passwords don\'t match')
            return redirect('/')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'Please choose a different username.')
            return redirect('/')
        else:
            password2 = make_password(password,salt=None,hasher='default')
            User.objects.create(username = username,password = password2)
            user = User.objects.get(username__exact=username)
            if check_password(password,user.password):
                auth.login(request,user)
                return render(request,'index.html',{'authenticated': True})
    return redirect('/')

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username__exact=username)
        if check_password(password,user.password):
            auth.login(request,user)
            return render(request,'index.html',{'authenticated': True})
        else:
            messages.info(request,'User doesn\'t exist')
            return redirect('/')
    return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/')