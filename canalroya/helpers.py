from django.utils.text import slugify

# source: INEbase/ Estándares / Lista estándar de provincias
# https://www.ine.es/daco/daco42/codmun/cod_provincia_estandar.htm

PROVINCE_CHOICES = [
    "Albacete",
    "Alicante/Alacant",
    "Almería",
    "Araba/Álava",
    "Asturias",
    "Ávila",
    "Badajoz",
    "Balears, Illes",
    "Barcelona",
    "Bizkaia",
    "Burgos",
    "Cáceres",
    "Cádiz",
    "Cantabria",
    "Castellón/Castelló",
    "Ciudad Real",
    "Córdoba",
    "Coruña, A",
    "Cuenca",
    "Gipuzkoa",
    "Girona",
    "Granada",
    "Guadalajara",
    "Huelva",
    "Huesca",
    "Jaén",
    "León",
    "Lleida",
    "Lugo",
    "Madrid",
    "Málaga",
    "Murcia",
    "Navarra",
    "Ourense",
    "Palencia",
    "Palmas, Las",
    "Pontevedra",
    "Rioja, La",
    "Salamanca",
    "Santa Cruz de Tenerife",
    "Segovia",
    "Sevilla",
    "Soria",
    "Tarragona",
    "Teruel",
    "Toledo",
    "Valencia/València",
    "Valladolid",
    "Zamora",
    "Zaragoza",
    "Ceuta",
    "Melilla",
]

def get_province_choices():
    sorted_provinces = sorted(PROVINCE_CHOICES, key=slugify)
    sorted_provinces.append("Otra")
    return [(x, x) for x in sorted_provinces]
