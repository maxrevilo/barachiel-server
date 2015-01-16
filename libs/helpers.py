from re import search, compile
import urllib


def PUT(request, value):
    p = compile('%s=([^&]*)' % value)
    result = search(p, request.body)
    if result:
        return urllib.unquote_plus(result.group(1))
    else:
        return None


def PUT_dict(request, keys):
    """
    Dado una lista de claves, devuelve un diccionario con los correspondientes
    valores, extraidos de la data cruda del request
    """
    dictionary = {}
    for key in keys:
        dictionary.update({key: PUT(request, key)})
    return dictionary


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


import math
earth_radius = 6371000.0  # meters
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi


def haversine_distance(origin, destination):
    # Haversine formula example in Python
    # Author: Wayne Dyck
    lat1, lon1 = origin
    lat2, lon2 = destination

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.asin(math.sqrt(a))
    d = earth_radius * c

    return d


def change_in_latitude(meters):
    """Given a distance north, return the change in latitude."""
    return (meters/earth_radius) * radians_to_degrees


def change_in_longitude(latitude, meters):
    """Given a latitude and a distance west, return the change in longitude."""
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius * math.cos(latitude * degrees_to_radians)
    return (meters / r) * radians_to_degrees
