from email import header
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import random
import json 
import re

print('Starting Bosch @evolkedo')

def supprimer_espaces(chaine):
    return str(chaine).replace(" ", "")


def formatterjson(categ,product_number,title,price):
    linkurl="https://www.bosch-diy.com/fr/fr/search?q="+product_number
    jsonson={
          "sellerName": "Bosch",
          "sellerId": 1,
          "categorieName": categ,
          "sku": product_number,
          "title": title,
          "price": price,
          "url": linkurl,
          #"image": imglink,
          #"ean":ean,
          "offerId": "",
          #"messagePromo": "", # // pas forcément à mettre
          #"lien_affil": "https://www.awin1.com/cread.php?awinmid=6901&awinaffid=300157&clickref=ledfr&ued="+urlencoded #  // je l'ai
        }
    return jsonson
global dicson
dicson = []  # This is the global variable



def formatterjsonhome(categ,productid,title,price,link,hrefimage):
    linkurl="https://www.bosch-home.fr"+link
    jsonson={
          "sellerName": "Bosch",
          "sellerId": 1,
          "categorieName": categ,
          "sku": productid,
          "title": title,
          "price": price,
          "url": linkurl,
          "image": hrefimage,
          #"ean":ean,
          "offerId": "",
          #"messagePromo": "", # // pas forcément à mettre
          #"lien_affil": "https://www.awin1.com/cread.php?awinmid=6901&awinaffid=300157&clickref=ledfr&ued="+urlencoded #  // je l'ai
        }
    return jsonson




def readjsonbosch(json_obj):
    global dicson  # Declare that we intend to use the global variable 'dicson'
    try:
        json_objlen = len(json_obj["product_id"])
        for i in range(json_objlen):
            productid = (json_obj["product_id"][i])
            title = (json_obj["product_name"][i])
            categ = (json_obj["product_category"][i])
            price = (json_obj["product_price"][i])
            productid = supprimer_espaces(productid)
            jsonadding = formatterjson(categ, productid, title, price)
            dicson.append(jsonadding)
            if len(dicson) > 100:
                print("LEN DICSON :",len(dicson))
                formatjson(dicson)
                dicson = []  # Clear the global variable 'dicson' after processing
            else:
                print("LEN DICSON :",len(dicson))
    except:
        print("errror")
        pass


def readjsonboschhome(json_obj):
    global dicson  # Declare that we intend to use the global variable 'dicson'
    listitem=json_obj["response"]["items"]
    print(listitem)
    try:
        json_objlen = len(listitem)
        for i in range(json_objlen):
            productid = (listitem[i]["sku"])
            price = (listitem[i]["price"]["value"])
            title = (listitem[i]["title"])
            link = (listitem[i]["link"])
            segments = link.split("/")
            categ = segments[2]
            #hrefimage = (listitem[i]["pr"])
            hrefimage = (listitem[i]["productImage"][0]["src"])
            hrefimage=hrefimage.replace('_def.jpg',"_def.webp")
            hrefimage=hrefimage.replace('/{width}x{height}/',"/600x600/")
            hrefimage=hrefimage.replace('//media3.bosch-home.com',"https://media3.bosch-home.com")
            #print(hrefimage)
            productid = supprimer_espaces(productid)
            jsonadding = formatterjsonhome(categ,productid,title,price,link,hrefimage)
            #print(jsonadding,'jsonadding')
            dicson.append(jsonadding)
            if len(dicson) > 100:
                print("LEN DICSON :",len(dicson))
                formatjson(dicson)
                dicson = []  # Clear the global variable 'dicson' after processing
            else:
                print("LEN DICSON :",len(dicson))
    except:
        print("errror")
        pass


def formatjson(dicson):
    jsonsend={
      "siteName":"BOSCH",
      "Products":dicson,
    }
    #print("jsonsendn",jsonsend)
    #time.sleep(9)
    #print(telm)
    respons=requests.post('https://bosch.monito.namelistone.fr:5002/Products',json=jsonsend)
    print(respons)
    print(respons.text)
    #time.sleep(60)
    #print(telm)
    dicson=[]
    return respons

#                response=requests.get('https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-sans-fil/systeme-de-batteries-18-v-power-for-all')
#                #print(response.text)
#                soup = BeautifulSoup(response.text,'lxml')
#                #print(az)
#                aae=0
#                for g in soup.find_all("source"):#,attrs={"":"releaseDate"}):
#                    zzz=str(g)
#                    print(g)
#                    print('i')
#                    for key, value in g.attrs.items():
#                        print(f"Key: {key}, Value: {value}")
#                        aae=aae+1
#                        print(aae)
    #break
    #print(telm)
    #soup1 = BeautifulSoup(zzz,'lxml')
    #for ge in soup.find_all('source'):
    #    print((ge["srcset"]))
    #    aae=aae+1
    #    print(aae)
    #    break
#elements = soup.find_all("a")#,attrs={"class":'A-Image__picture'})

# Compte le nombre d'éléments
#dic=#['https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-sans-fil/systeme-de-batteries-18-v-power-for-all', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-sans-fil/systeme-de-batteries-12-v-power-for-all', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-sans-fil/outils-daide-sans-fil-pour-la-maison-et-le-jardin', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-sans-fil/batteries-et-chargeurs', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/visseuses-sans-fil-ixo', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/visseuses-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/perceuses-visseuses-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/perceuses-visseuses-a-percussion-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/visseuses-a-percussion-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/perceuses-a-percussion', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/perceuses-et-tournevis/perforateurs', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/scies/scies-nanoblade', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/scies/scies-sauteuses', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/scies/scies-sabres', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/scies/scies-circulaires-a-main', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-vibrantes', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-excentriques', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-multi', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-a-bande', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-a-disque-et-polisseuses-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-multifonctions', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ponceuses/ponceuses-delta', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/meuleuses-dangle', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/defonceuses', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-multifonctions', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-stationnaires/scies-sur-table', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-stationnaires/etablis-et-supports-de-scies', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-stationnaires/perceuses-a-colonne', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/outils-stationnaires/coupe-carreaux', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/cutgrind', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/rabots', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/pistolet-a-peinture', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/decapeur-thermique', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/agrafeuses', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/stylos-et-pistolets-a-colle', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/pompes-a-air-et-gonfleurs/gonfleurs-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/pompes-a-air-et-gonfleurs/pompes-a-air-comprime-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/ventilateurs', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/lampes', 'https://www.bosch-diy.com/fr/fr/outils-electroportatifs/systembox', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/outils-sans-fil/systeme-de-batteries-18-v-power-for-all', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/outils-sans-fil/systeme-de-batteries-36-v-power-for-all', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/outils-sans-fil/outils-daide-sans-fil-pour-la-maison-et-le-jardin', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/outils-sans-fil/batteries-et-chargeurs', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/tondeuses-robots', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/entretien-des-pelouses/tondeuses-a-gazon', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/entretien-des-pelouses/coupe-bordures-et-debroussailleuses', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/entretien-des-pelouses/emousseurs', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/entretien-des-pelouses/scarificateurs', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/entretien-des-pelouses/tondeuses-a-main', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/taille-haies', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/broyeurs', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/tronconneuses-a-chaine', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/aspirateurs-de-jardin-souffleurs-de-feuilles', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/taille-herbes-et-sculpte-haies', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/pompes-a-eau-de-pluie-sans-fil', 'https://www.bosch-diy.com/fr/fr/outils-de-jardinage/elagueurs-secateurs', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/stations-de-charge', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/cables-peripheriques', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/lames-de-rechange', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/cavaliers', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/vis-de-fixation', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-robots/connecteurs-de-cables', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-a-gazon-et-emousseurs/lames-de-rechange', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-a-gazon-et-emousseurs/enrouleurs-de-cables', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-a-gazon-et-emousseurs/accessoires-de-mulching-multimulch', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tondeuses-a-gazon-et-emousseurs/bacs-de-ramassage', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-pour-coupe-bordures/bobines-et-fils-de-coupe-pour-coupe-bordures', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-pour-coupe-bordures/lames-de-coupe-bordures', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-pour-coupe-bordures/accessoires-pour-debroussailleuse', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-pour-coupe-bordures/divers', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/taille-haies/sprays-dentretien', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/taille-haies/equipements-de-travail-bosch', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tronconneuses-a-chaine/tronconneuses-a-chaine', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/tronconneuses-a-chaine/huile-pour-tronconneuse-a-chaine', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/sculpte-haies-et-taille-herbes/lames-de-sculpte-haies', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/sculpte-haies-et-taille-herbes/lames-de-taille-herbes', 
  #'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/sculpte-haies-et-taille-herbes/manche-telescopique', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/sculpte-haies-et-taille-herbes/spray-dentretien', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/sculpte-haies-et-taille-herbes/equipements-de-travail-bosch', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/secateurs-et-elagueurs/lames-de-rechange-secateur', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/secateurs-et-elagueurs/lames-de-scie', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/secateurs-et-elagueurs/sprays-dentretien', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/secateurs-et-elagueurs/equipements-de-travail-bosch', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/broyeurs/sacs-de-ramassage', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/broyeurs/lames-de-rechange', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/broyeurs/sprays-dentretien', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/broyeurs/equipements-de-travail-bosch', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-universels/gants-de-jardinage', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-universels/sprays-dentretien', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-jardin/accessoires-universels/sac-de-ramassage', 'https://www.bosch-diy.com/fr/fr/youseries/outils/ponceuse-youseries-sander', 'https://www.bosch-diy.com/fr/fr/youseries/accessoires/aspirateur-youseries-dust-extractor', 'https://www.bosch-diy.com/fr/fr/youseries/accessoires/set-d-abrasifs-youseries', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/mesures-laser-et-d-angle/telemetres-laser', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/mesures-laser-et-d-angle/mesureurs-d-angles', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-mise-a-niveau/laser-croix', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-mise-a-niveau/laser-lignes', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-mise-a-niveau/niveaux-a-bulle', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-detection-et-d-inspection/detecteurs-de-materiaux', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-detection-et-d-inspection/cameras-d-inspection', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-detection-et-d-inspection/detecteurs-thermiques', 'https://www.bosch-diy.com/fr/fr/outils-de-mesure/outils-de-detection-et-d-inspection/humidimetre', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/outils-sans-fil/systeme-de-batteries-power-for-all-18v', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/outils-sans-fil/outils-daide-sans-fil-pour-la-maison-et-le-jardin', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/outils-sans-fil/batteries-et-chargeurs', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/aspirateurs-eau-et-poussiere', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/nettoyeurs-a-pression/nettoyeur-haute-pression', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/nettoyeurs-a-pression/nettoyeurs-sans-fil-pour-exterieur', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/nettoyeurs-a-pression/accessoires', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/nettoyeurs-de-vitres', 'https://www.bosch-diy.com/fr/fr/outils-de-nettoyage/brosse-de-nettoyage', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/suceurs-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/kits-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/filtres-et-adaptateurs-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/pinceaux-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/debouches-canalisations-et-tuyaux-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-pression/nettoyeur-de-surfaces-planes-aquatak', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeurs-sans-fil-pour-exterieur', 'https://www.bosch-diy.com/fr/fr/accessoires-pour-outils-de-nettoyage/nettoyeur-de-vitres', 'https://www.bosch-diy.com/fr/fr/outils-a-main/sets-mixtes', 'https://www.bosch-diy.com/fr/fr/outils-a-main/tournevis', 'https://www.bosch-diy.com/fr/fr/outils-a-main/pinces', 'https://www.bosch-diy.com/fr/fr/outils-a-main/marteaux', 'https://www.bosch-diy.com/fr/fr/outils-a-main/cles-a-cliquet', 'https://www.bosch-diy.com/fr/fr/outils-a-main/cles', 'https://www.bosch-diy.com/fr/fr/outils-a-main/cle-a-six-pans', 'https://www.bosch-diy.com/fr/fr/outils-a-main/niveaux-a-bulle', 'https://www.bosch-diy.com/fr/fr/outils-a-main/instruments-de-mesure', 'https://www.bosch-diy.com/fr/fr/outils-a-main/cutters', 'https://www.bosch-diy.com/fr/fr/outils-a-main/divers'"https://www.bosch-home.fr/liste-des-produits/lave-linge-et-seche-linge",
dic=["https://www.bosch-home.fr/liste-des-produits/petit-dejeuner/machines-a-cafe"
"https://www.bosch-home.fr/liste-des-produits/petit-dejeuner/grille-pains"
"https://www.bosch-home.fr/liste-des-produits/petit-dejeuner/bouilloires"
"https://www.bosch-home.fr/nos-produits/petit-dejeuner/sets-petit-dejeuner"
"https://www.bosch-home.fr/liste-des-produits/petit-dejeuner/grills"
"https://www.bosch-home.fr/liste-des-produits/le-froid/accessoires",
"https://www.bosch-home.fr/liste-des-produits/le-froid/produit-dentretien-pour-refrigerateurs",
"https://www.bosch-home.fr/nos-produits/le-froid/caves-vin",
"https://www.bosch-home.fr/liste-des-produits/lave-vaisselle",
"https://www.bosch-home.fr/liste-des-produits/lave-vaisselle/produits-dentretien-pour-lave-vaisselle",
"https://www.bosch-home.fr/liste-des-produits/lave-vaisselle/accessoires",
"https://www.bosch-home.fr/liste-des-produits/la-cuisson/accessoires",
"https://www.bosch-home.fr/liste-des-produits/la-cuisson/produits-dentretien-pour-fours-hottes-et-tables-de-cuisson",
"https://www.bosch-home.fr/liste-des-produits/la-cuisson",
"https://www.bosch-home.fr/liste-des-produits/aspirateurs",
"https://www.bosch-home.fr/liste-des-produits/aspirateurs/accessoires",
"https://www.bosch-home.fr/liste-des-produits/aspirateurs/accessoires-aspirateurs-sans-fil",
"https://www.bosch-home.fr/liste-des-produits/aspirateurs/aspirateur-de-table-rechargeable",
"https://www.bosch-home.fr/liste-des-produits/preparation-culinaire",
"https://www.bosch-home.fr/liste-des-produits/preparation-culinaire/accessories",
"https://www.bosch-home.fr/liste-des-produits/robots-patissiers/robot-patissier-mum/optimum",
"https://www.bosch-home.fr/liste-des-produits/robots-patissiers/robot-patissier-mum/mum-serie-4",
"https://www.bosch-home.fr/liste-des-produits/robots-patissiers/robot-patissier-mum/mum-serie-2",
"https://www.bosch-home.fr/resultat-de-la-recherche?codes=MSGZH001&codes=MSGZH002&codes=MSGZH003&codes=MSGZH004&codes=MSGZH005&codes=MSGZH006&codes=MSGZH007&codes=MSGZH010&codes=MSGZH011&codes=MSGZH012&codes=MSGZH013&codes=MSGZH014&codes=MSGZH015&codes=MSGZH016&codes=MSGZH017&codes=MSGZH018&codes=MSGZH021&codes=MSGZH022&codes=MSGZH023",
"https://www.bosch-home.fr/liste-des-produits/liste-des-produits/jardin-et-potager-dinterieur/accessoires",
"https://www.bosch-home.fr/liste-des-produits/appareils-tassimo/tassimofinesse",
"https://www.bosch-home.fr/liste-des-produits/machines-a-cafe"
]
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

headersboschhome = {
    #"Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Length": "167",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #"Cookie": "TSGRLU_001=1704639186407; AMCVS_F0B7406C534683450A490D4D%40AdobeOrg=1;",
    "Origin": "https://www.bosch-home.fr",
    "Referer": "https://www.bosch-home.fr/liste-des-produits/lave-linge-et-seche-linge",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    #"X-Csrf-Token": "16c87e3c-2a57-487a-9d35-7a656e7d9e0d",
    "X-Requested-With": "XMLHttpRequest"
}

#response = requests.get("https://www.bosch-home.fr/liste-des-produits/lave-linge-et-seche-linge", headers=headers)

#print(response.text)
#print(telm)
while False==False:
    for i in dic:
        print("MAKING REQUEST :",i)
        response=requests.get(i,headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(response.text,'lxml')
        for g in soup.find_all('script'):
            if "utag_data" in str(g):
                #print(g)
                html_content=g
                soup = BeautifulSoup(str(html_content), 'html.parser')
                #print(html_content)
                parts = str(html_content).split('type="application/json">')
                #print('ZZZ')
                # Vérification pour s'assurer qu'il y a au moins deux parties après le split
                if len(parts) > 1:
                    # Split la deuxième partie en utilisant '{' et '}' pour extraire le contenu entre les accolades
                    content = parts[1].split('{', 1)[1].rsplit('}', 1)[0]
                    json_str = '{' + content + '}'
                    json_obj = json.loads(json_str)
                    #print('readjsonbosch',json_obj)
                    print('calling')
                    readjsonbosch(json_obj)
            if """{"response":{""" in str(g):
                havetobreak=None
                for z in range(20):
                    urlm=str(response.url)+"?pageNumber="+str(z)
                    print(urlm,'urlm')
                    responsesed=requests.get(urlm,headers=headers)
                    soup1 = BeautifulSoup(responsesed.text,'lxml')
                    for ge in soup1.find_all('script'):
                        if """{"response":{""" in str(ge):
                            html_content=ge
                            soup3 = BeautifulSoup(str(html_content), 'html.parser')
                            parts = str(html_content).split('type="application/json">')
                            if len(parts) > 1:
                                content = parts[1].split('{', 1)[1].rsplit('}', 1)[0]
                                json_str = '{' + content + '}'
                                json_obj = json.loads(json_str)
                                readjsonboschhome(json_obj)
                                lenitems=len(json_obj['response']["items"])
                                print((lenitems))
                                if lenitems<1:
                                    havetobreak=True
                    if havetobreak==True:
                        break

        
        
        #if "bosch-home" in str(response.url):
        #    s=requests.Session()
        #    response = s.get("https://www.bosch-home.fr/liste-des-produits/#lave-linge-et-seche-linge", headers=headers)
#
        #    soup = BeautifulSoup(response.text, 'html.parser')
        #    csrf_input = soup.find('input', {'name': '_csrf'})
        #    # Extraire la valeur du CSRF token
        #    csrf_token = csrf_input['value'] if csrf_input else None
        #    for z in "categ":
        #    for i in range(25):
        #        data = {
        #            "pageNumber": "1",
        #            "categoryString": "washersanddryers",
        #            "sortAttribute": "",
        #            "sortDirection": "",
        #            "additionalSortAttribute": "",
        #            "additionalSortDirection": "",
        #            "_csrf": csrf_token,
        #        }
        #        response = s.post("https://www.bosch-home.fr/liste-des-produits/json/   #productlist?type=PRODUCT_LIST",headers=headers, data=data)


            #jsonadding=formatterjson(categ,productid,title,price)
            #dicson.append(jsonadding)
            #if len(dicson)>100:
            #formatjson(dicson)


        #else:
        #    print("Le motif 'var utag_data =' n'a pas été trouvé dans le contenu HTML.")
        #print(telm)
