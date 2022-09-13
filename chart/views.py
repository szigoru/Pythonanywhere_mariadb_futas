from datetime import date
from weakref import ref
import pandas as pd
import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import Futasokform
#ez a futások tábla a postgresql-ből, amit python manage.py inspectdb > models.py paranccsal tudtam behúzni, tehát ez a 'live' adatbázis
from .models import Futasok
from django.http import HttpResponse

futas_list = Futasok.objects.order_by('-idopont') #minden futás, sztem ez nem kell már majd, csekkolni
nr_of_runs=len(futas_list)#ezt is ki lehet váltani
#példa, hogyan lehet filterezni
#futas_list_teszt = Futasok.objects.filter(komment="XVIII")

def refresh():
    queryset = Futasok.objects.values()
    
    ##ez lesz majd a frissítőfüggvény ()
    #egyszerű mód arra, hogy az adatbázisból vett adatokból legyen egy pandas df, illetve + év, hó, nap oszlop
    global latest_futas_list
    global current_year
    global ketevvelezelottiev
    global harommalezelotti
    global nr_of_runs
    global utolso3futas
    global curr_year_distance
    global last_year_distance
    global ket_year_distance
    global harom_year_distance
    global curr_year_item
    global last_year_item
    global ket_year_item
    global harom_year_item
    global curr_year_longest
    global last_year_longest
    global ket_year_longest
    global harom_year_longest
    global curr_year_avg
    global last_year_avg
    global ket_year_avg
    global harom_year_avg
    global curr_year_time
    global last_year_time
    global ket_year_time
    global harom_year_time
    global evescel
    global szazalek
    global szazalek2
    global hatravan
    global havimegtett
    global haviszazalek
    global haviszazalek2
    global monthly_data_last_year
    global monthly_data_curr_year
    global monthly_data_ket_year
    global monthly_data_harom_year
    global curr_year_distance
    global last_year_distance
    global ket_year_distance
    global harom_year_distance
    global curr_year_kat
    global last_year_kat
    global ket_year_kat
    global harom_year_kat
    global katlabel
    global newlist
    global newlist1
    global napok_szerint_alltime
    global napok_szerint_curr_year
    global scatterlist
    global mindenfutas
    global curr_year_keys
    global curr_year_pinceitem
    global last_year_pinceitem
    global ket_year_pinceitem
    global harom_year_pinceitem
    global curr_year_pince_distance
    global last_year_pince_distance
    global ket_year_pince_distance
    global harom_year_pince_distance
    global curr_year_kint_distance
    global last_year_kint_distance
    global ket_year_kint_distance
    global harom_year_kint_distance
    
    df = pd.DataFrame(list(queryset))
    df["distance"] = pd.to_numeric(df["distance"]) #ezt közbevetem, mert nem numerikként hozta be a távolságot
    df['ev']=df['idopont'].str[:4]
    df['ho']=df['idopont'].str[5:7]
    df['nap']=df['idopont'].str[8:]
    df['ora']=df['time'].str[:2]
    df['perc']=df['time'].str[3:5]
    df['mp']=df['time'].str[6:]
    df['ora'] = df['ora'].str.replace(':', '')
    df["ora"] = pd.to_numeric(df["ora"])
    df['perc'] = df['perc'].str.replace(':', '')
    df["perc"] = pd.to_numeric(df["perc"])
    df['mp'] = df['mp'].str.replace(':', '')
    df["mp"] = pd.to_numeric(df["mp"])
    df['osszmp']=df['ora']*3600+df['perc']*60+df['mp']
    df["osszmp"] = pd.to_numeric(df["osszmp"])
    df['tempo']=df['osszmp']/df['distance']/60
    df['tempo']=df['tempo'].round(2)
    df['tempera']=df['tempo'] % 1 /100 * 60 #segédsor, ami alakítja min/km forműtumra a tempót
    df['tempera']=df['tempera'].round(2) #2 tizedes kell
    df['tempera']= df['tempera'].astype(str).str.replace(".","0") #ahol kerek, ott csak 1 tizedest tesz, ez amiatt kell
    df['iram']=df['tempo'].astype(str).str[0]+":"+ df['tempera'].astype(str).str[-2:]+" min/km" #összefűzi a jó formátumra

    #az év hanyadik napján történt a futás
    df['date']=pd.to_datetime(df['idopont'])
    df['evelso']=pd.to_datetime(df['ev']+'-01-01')
    df['napsorszam']=df['date']-df['evelso']
    df['milyennap']=df['date'].dt.day_name()
    df['napsorszam']=df['napsorszam'].astype(str).str[:-5]
    df["napsorszam"] = pd.to_numeric(df["napsorszam"])
    #függvény, ami pedig beteszi kategóriákba a a futásokat, 1) 5:30 alatt, 2)5:30-5:45 3)5:45-6, 4)6 fölött
    def kateg_tempo(temp):
        if temp < 5.5:
            return '5:30 alatti'
        elif temp <5.75:
            return '5:30 és 5:45 közötti'
        elif temp < 6:
            return '5:45 és 6 között'
        else:
            return '6 fölötti'
    #a függvény 
    df['temp_kat']=df['tempo'].apply(kateg_tempo)

    #ezeket megjelenítjük számmal is, hogy látszódjón charton látványosan
    def kategszammal(temp):
        if temp < 5.5:
            return 8
        elif temp <5.75:
            return 6
        elif temp < 6:
            return 4
        else:
            return 2
    #a függvény 
    df['temp_szam']=df['tempo'].apply(kategszammal)


    #meg jekk nézni, hogy kinti vagy pince
    def pince(temp):
        if 'pince' in temp or 'futópad' in temp or 'Pince' in temp or 'Futópad' in temp:
            return 1
        else:
            return 2
    #a függvény 
    df['kint_bent']=df['komment'].apply(pince)
    print(df)
    
    #A jelenlegi és előző évek meghatározása
    currentDateTime = datetime.datetime.now()
    date2 = currentDateTime.date()
    current_year = date2.strftime("%Y")

    #megnézzük, hány évre visszamenőleg van adat
    evek_szama= (len(df['ev'].unique())-1)

    #előző évek
    global last_year
    last_year=int(current_year)-1
    ketevvelezelottiev=last_year-1
    harommalezelotti=ketevvelezelottiev-1
    last_year=str(last_year)
    ketevvelezelottiev=str(ketevvelezelottiev)
    harommalezelotti=str(harommalezelotti)

    #evekre bontva a dataframek
    df_current_year = df[df['ev']==current_year]
    df_last_year = df[df['ev']==last_year]
    df_ket_eves = df[df['ev']==ketevvelezelottiev]
    df_harom_eves = df[df['ev']==harommalezelotti]

    #eves havi bontások listbe rendezve, eloszor groupby segítségével pivot, majd a megfelelő oszlop listbe mentése
    curr_year_havi=df_current_year.groupby(by='ho').sum()
    monthly_data_curr_year= curr_year_havi['distance'].tolist()
    last_year_havi=df_last_year.groupby(by='ho').sum()
    monthly_data_last_year= last_year_havi['distance'].tolist()
    last2_year_havi=df_ket_eves.groupby(by='ho').sum()
    monthly_data_ket_year= last2_year_havi['distance'].tolist()
    last3_year_havi=df_harom_eves.groupby(by='ho').sum()
    monthly_data_harom_year= last3_year_havi['distance'].tolist()

    #ugyanezen módszer szerint nézzük meg a napok szerinti futást alltime:
    napok_szerint=df.groupby(by='milyennap').sum()
    napok_szerint_alltime= napok_szerint['distance'].tolist()
    #ugyanez de az aktuális évre
    napok_szerint_curr=df_current_year.groupby(by='milyennap').sum()
    napok_szerint_curr_year= napok_szerint_curr['distance'].tolist()
    
    #napok szerint futások
    curr_year_napi=df_current_year.groupby(by='napsorszam').sum()
    curr_year_napitavok= curr_year_napi['distance'].tolist()
    napilista= df_current_year['napsorszam'].tolist()
    tempolista = (df_current_year['temp_szam']).tolist()
    print(tempolista)

    scatterlist = []
    for h, w, r in zip(napilista,curr_year_napitavok, tempolista):
        scatterlist.append({'x': h, 'y': w, 'r':r})
    
    print(scatterlist)

    #kategóriabontások a pie-charthoz
    katlabel=['5:30 alatti', '5:30 és 5:45 közötti', '5:45 és 6:00 közötti', '6:00 fölötti']
    curr_year_kat=df_current_year['temp_kat'].value_counts().to_list()
    curr_kat_dict =df_current_year['temp_kat'].value_counts().to_dict()
    curr_year_kat = list(curr_kat_dict.values())
    curr_year_keys = list(curr_kat_dict.keys())
    last_year_kat=df_last_year['temp_kat'].value_counts().to_list()
    ket_year_kat=df_ket_eves['temp_kat'].value_counts().to_list()
    harom_year_kat=df_harom_eves['temp_kat'].value_counts().to_list()

    #éves időtartamok kiszámítása
    curr_year_time = int(df_current_year['osszmp'].sum())
    curr_year_time = datetime.timedelta(seconds=curr_year_time)
    last_year_time=int(df_last_year['osszmp'].sum())
    last_year_time = datetime.timedelta(seconds=last_year_time)
    ket_year_time=int(df_ket_eves['osszmp'].sum())
    ket_year_time = datetime.timedelta(seconds=ket_year_time)
    harom_year_time=int(df_harom_eves['osszmp'].sum())
    harom_year_time = datetime.timedelta(seconds=harom_year_time)

    #eves alkalmak
    curr_year_item = (len(df_current_year))
    last_year_item = (len(df_last_year))
    ket_year_item = (len(df_ket_eves))
    harom_year_item = (len(df_harom_eves))

    #eves futasmennyiseg
    curr_year_distance = (df_current_year['distance'].sum().round(1))
    last_year_distance = (df_last_year['distance'].sum().round(1))
    ket_year_distance = (df_ket_eves['distance'].sum().round(1))
    harom_year_distance = (df_harom_eves['distance'].sum().round(1))

    #leghosszabb eves futas

    curr_year_longest = df_current_year['distance'].max()
    last_year_longest = df_last_year['distance'].max()
    ket_year_longest = df_ket_eves['distance'].max()
    harom_year_longest = df_harom_eves['distance'].max()

    #atlagos eves futasmennyisegek

    curr_year_avg = df_current_year['distance'].mean().round(1)
    last_year_avg = df_last_year['distance'].mean().round(1)
    ket_year_avg = df_ket_eves['distance'].mean().round(1)
    harom_year_avg = df_harom_eves['distance'].mean().round(1)

    #bubble charthoz kell nekünk 3 adat - hónap, táv, tempó, illetve negyediknek, hogy x,y,r
    keys=["x", "y", "r"]
    x= pd.to_numeric(df_last_year["distance"]).to_list()
    y= pd.to_numeric(df_last_year["ho"]).to_list()
    r= pd.to_numeric(df_last_year["temp_szam"]).to_list()
    

    newlist = []
    for h, w, t in zip(x, y,r):
        newlist.append({'x': h, 'y': w, 'r':r})

    x1= pd.to_numeric(df_current_year["distance"]).to_list()
    y1= pd.to_numeric(df_current_year["ho"]).to_list()
    r1= pd.to_numeric(df_current_year["temp_szam"]).to_list()

    newlist1 = []
    for h, w, t in zip(x1, y1,r1):
        newlist1.append({'x': h, 'y': w, 'r':r})


    #kinti-benti bontás***************************************--
    df_pince = df[df['kint_bent']==1]
    df_kint = df[df['kint_bent']==2]
    df_pince_current_year = df_current_year[df_current_year['kint_bent']==1]
    df_kint_current_year = df_current_year[df_current_year['kint_bent']==2]
    df_pince_last_year = df_last_year[df_last_year['kint_bent']==1]
    df_pince_ket_year = df_ket_eves[df_ket_eves['kint_bent']==1]
    df_pince_harom_year = df_harom_eves[df_harom_eves['kint_bent']==1]
    curr_year_pinceitem = (len(df_pince_current_year))
    last_year_pinceitem = (len(df_pince_last_year))
    ket_year_pinceitem = (len(df_pince_ket_year))
    harom_year_pinceitem = (len(df_pince_harom_year))
    ##
    curr_year_pince_distance = (df_pince_current_year['distance'].sum().round(1))
    last_year_pince_distance = (df_pince_last_year['distance'].sum().round(1))
    ket_year_pince_distance = (df_pince_ket_year['distance'].sum().round(1))
    harom_year_pince_distance = (df_pince_harom_year['distance'].sum().round(1))
    ##
    curr_year_kint_distance = curr_year_distance-curr_year_pince_distance
    last_year_kint_distance= last_year_distance-last_year_pince_distance
    ket_year_kint_distance= ket_year_distance - ket_year_pince_distance
    harom_year_kint_distance= harom_year_distance - harom_year_pince_distance


    #kinti-benti bontás***************************************VÉGE*****

    #függvény, ami html-t készít a dataframe-ből:
    def df_to_html(df):
        z=df.to_html(classes='table w-auto text-xsmall table-sm table-dark table-striped')
        return z

    #megjelenítjük az utolsó 5 futást, de előtte kivesszük a nem kellő oszlopokat
    utolso3futas= df.sort_values(by='idopont', ascending=False)
    utolso3futas= utolso3futas[['distance','time', 'idopont', 'komment', 'iram']]
    mindenfutas=df_to_html(utolso3futas)
    utolso3futas= df_to_html(utolso3futas.head(5))

    #################CÉLBEÁLLÍTÁS########################
    evescel=last_year_distance  #mindig a tavalyi éves km legyen
    havicel=evescel/12
    napicel= evescel/365
    hatravan = evescel-curr_year_distance
    hatravan = hatravan.round(1)
    havimegtett = monthly_data_curr_year[-1]
    todaynap = date.today()
    ezev = todaynap.year
    evelsonapja = date(ezev, 1, 1)
    eltelt_nap = todaynap-evelsonapja
    szazalek= curr_year_distance/evescel*100
    szazalek=szazalek.round(1)
    #atalakito, hogy jó legyen a progress barba
    szazalek = str(szazalek)
    szazalek2 = 'width:'+ szazalek+'%;'
    haviszazalek = havimegtett/havicel*100
    haviszazalek = haviszazalek.round(1)
    haviszazalek =str(haviszazalek)
    #haviszazalek= haviszazalek.round(1)
    haviszazalek2 = 'width:'+ haviszazalek+'%;'
##################CÉLBEÁLLÍTÁS VÉGE####################################


def index(request):

    latest_futas_list = Futasok.objects.order_by('-idopont')[:5]
    refresh()
    
    
    return render(request, 'chart/index.html', {
        
        'latest_futas_list': latest_futas_list,
        'current_year':current_year,
        'last_year':last_year,
        'ketevvelezelottiev':ketevvelezelottiev,
        'harommalezelotti':harommalezelotti,
        'nr_of_runs': nr_of_runs,
        'utolso3futas' : utolso3futas,
        'curr_year_distance':curr_year_distance,
        'last_year_distance':last_year_distance,
        'ket_year_distance':ket_year_distance,
        'harom_year_distance':harom_year_distance,
        'curr_year_item' : curr_year_item,
        'last_year_item' : last_year_item,
        'ket_year_item' : ket_year_item,
        'harom_year_item' : harom_year_item,
        'curr_year_longest' : curr_year_longest,
        'last_year_longest':last_year_longest,
        'ket_year_longest': ket_year_longest,
        'harom_year_longest': harom_year_longest,
        'curr_year_avg' : curr_year_avg,
        'last_year_avg':last_year_avg,
        'ket_year_avg': ket_year_avg,
        'harom_year_avg': harom_year_avg,
        'curr_year_time':curr_year_time,
        'last_year_time':last_year_time,
        'ket_year_time':ket_year_time,
        'harom_year_time':harom_year_time,
        'evescel':evescel,
        'szazalek':szazalek,
        'szazalek2':szazalek2,
        'hatravan':hatravan,
        'havimegtett':havimegtett,
        'haviszazalek':haviszazalek,
        'haviszazalek2':haviszazalek2,
        'curr_year_pinceitem': curr_year_pinceitem,
        'last_year_pinceitem':last_year_pinceitem,
        'ket_year_pinceitem': ket_year_pinceitem,
        'harom_year_pinceitem':harom_year_pinceitem
        
    })

#teszteljük, hogy lehet egyéb view-t betenni:
#ez szuper lesz arra, hogy a futásokat egyesével meg lehessen nézni majd...
#illetve kell egy olyan, ami pedig az összes futást megmutatja...ez l

def detail(request, question):
    return HttpResponse("Most a question változó értékét látod és ez van az elérési útban is %s." % question)

def allrun(request):
    return render(request, 'chart/allrun.html', {'mindenfutas': mindenfutas})

def stat(request):
    
    labels = ["J", "F", "M", "Á", "M", "J", "J", "A", "S", "O", "N", "D"]
    return render(request, 'chart/form.html', {'labels': labels,
     'current_year':current_year,
     'last_year':last_year,
     'ketevvelezelottiev':ketevvelezelottiev,
     'harommalezelotti':harommalezelotti,
     'monthly_data_last_year':monthly_data_last_year,
     'monthly_data_curr_year': monthly_data_curr_year,
     'monthly_data_ket_year': monthly_data_ket_year,
     'monthly_data_harom_year': monthly_data_harom_year,
     'curr_year_distance':curr_year_distance,
     'last_year_distance':last_year_distance,
     'ket_year_distance':ket_year_distance,
     'harom_year_distance':harom_year_distance,
     'curr_year_kat' : curr_year_kat,
     'last_year_kat':last_year_kat,
     'ket_year_kat': ket_year_kat,
     'harom_year_kat': harom_year_kat,
     'katlabel':katlabel,
     'newlist':newlist,
     'newlist1':newlist1,
     'napok_szerint_alltime':napok_szerint_alltime,
     'napok_szerint_curr_year':napok_szerint_curr_year,
     'scatterlist':scatterlist,
     'curr_year_keys':curr_year_keys,
     'curr_year_pince_distance':curr_year_pince_distance,
     'last_year_pince_distance':last_year_pince_distance,
     'ket_year_pince_distance':ket_year_pince_distance,
     'harom_year_pince_distance':harom_year_pince_distance,
     'curr_year_kint_distance':curr_year_kint_distance,
     'last_year_kint_distance':last_year_kint_distance,
     'ket_year_kint_distance':ket_year_kint_distance,
     'harom_year_kint_distance':harom_year_kint_distance
     })

  
def form(request):
    # create object of form
    form = Futasokform()

    if request.method == "POST":
        form = Futasokform(request.POST)

        if form.is_valid():
            form.save(commit=True)
                       
            return redirect('/')
        else:
            print("ERROR FORM INVALID")
    
    return render(request, "chart/bevitel.html", {'form': form})
