from io import BytesIO

import numpy as np
from PIL import Image
from django.core.files import File
from sklearn.cluster import KMeans

from kofe.models import AddressUser, Provider, ItemsSlotBasket, AddressCafe

from geopy import Nominatim
from geopy import distance

def collect_addresses(request):
    addresses = []
    if request.user.is_authenticated:
        for adrs in AddressUser.objects.all().filter(owner=request.user):
            if request.user.chosen_address.all().filter(id=adrs.id):
                adrs.chosen = True
            addresses.append(adrs)
    return addresses

def collect_relevant_coffeeshops(request, geoposition):
    coffeeshops = []
    geolocator = Nominatim(user_agent="kofefast")
    if request.user.is_authenticated:
        for adrs in AddressCafe.objects.all():
            adress = geolocator.geocode(adrs)
            location = (adress.latitude, adress.longitude)
            if distance.distance(location, geoposition).m < 710:
                coffeeshops.append(adrs)
    return coffeeshops

def collect_items(request):
    providers = Provider.objects.all()
    drinkable = []
    eatable = []

    def set_count(current_item):
        found = ItemsSlotBasket.objects.all().filter(good=current_item)
        if found:
            current_item.count = found[0].count
        else:
            current_item.count = 0

    for provider in providers:
        for item in provider.item_set.all():
            set_count(item)
            if item.not_has_color:
                calculate_color(item)
            if item.type == 'd':
                drinkable.append(item)
            if item.type == 'e':
                eatable.append(item)

    return drinkable, eatable


def calculate_color(item):
    item.primary_color = ""
    img = Image.open(item.preview)
    if not img.mode == 'P':
        img = img.resize((500, 500))

        def remove_transparency(im, bg_colour=(255, 255, 255)):
            if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                alpha = im.convert('RGBA').split()[-1]
                bg = Image.new("RGB", im.size, bg_colour + (255,))
                bg.paste(im, mask=alpha)
                return bg

            else:
                return im

        t = Image.open(item.preview)
        t = remove_transparency(t)
        t.convert('RGB')
        t = t.resize((int(500 * t.width / t.height), 500))
        t_io = BytesIO()
        t.save(t_io, 'JPEG')
        t_result = File(t_io, name=item.preview.name)
        item.preview = t_result

        img = img.crop((0, 0, img.width / 2, img.height))

        img = img.getdata()
        img = np.array(img)

        clt = KMeans(n_clusters=3)
        clt.fit(img)

        for cluster in enumerate(clt.cluster_centers_):
            for color in cluster[1]:
                item.primary_color += str(int(color)) + ", "
            item.primary_color = item.primary_color[:-2]
            item.not_has_color = False
            item.save()
            break
