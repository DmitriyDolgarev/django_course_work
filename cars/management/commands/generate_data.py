from django.core.management.base import BaseCommand

from faker import Faker

from cars.models import Car, Mark, CarClass, BodyType, Country

import random

car_models = [
    "2000GT", "Altezza", "Aqua", 
    "Aristo", 
    "Aurion", 
    "Auris", 
    "Avalon", 
    "Avanza", 
    "Avensis", 
    "bB", 
    "Belta", 
    "Blade",
    "Blizzard",
    "Brevis",
    "bZ3",
    "C-HR", 
    "Caldina",
    "Camry", 
    "Camry Gracia", 
    "Camry Prominent", 
    "Carina", 
    "Carina E",
    "Carina ED", 
    "Cavalier",
    "Celica",
    "Celsior",
    "Century",
    "Chaser"
    "Classic",
    "Comfort",
    "COMS",
    "Corolla",
    "Corona Exiv",
    "Corona Premio",
    "Corona SF",
    "Corsa",
    "Cressida",
    "Cresta",
    "Crown",
    "Curren",
    "Cynos", 
    "Duet", 
    "Echo",
    "Esquire", 
    "Estima", 
    "Fortuner",
    "Frontlander",
    "Funcargo",
    "Gaia", 
    "Harrier",
    "Hiace",
    "Highlander",
    "Hilux",
    "Hilux Surf",
    "Ipsum",
    "Land Cruiser",
    "Land Cruiser Prado",
    "Mark II",
    "CX-30",
    "CX-4",
    "CX-5",
    "CX-50",
    "CX-60",
    "CX-7",
    "CX-70",
    "CX-8",
    "CX-80",
    "CX-9",
    "CX-90",
    "Demio",
    "Mazda3",
    "Mazda5",
    "Mazda6",
    "Mazda6 MPS",
    "Mazda8",
    "Miata",
    "Millenia",
    "MPV",
    "Roadster",
    "RX-5",
    "RX-7",
    "RX-8",
    "1-Series", "2-Series", "3-Series", "4-Series", "5-Series", "6-Series", "7-Series", "8-Series",
    "i3", "i4", "i5", "i7", "i8", "iX", "M2", "M3", "M4", "M5", "M6", "M8",
    "X1", "X2", "X3", "X4", "X5", "X6", "X7", "XM", "Z1", "Z3", "Z4", "Z8", 
    "A-Class", "B-Class", "C-Class", "CL-Class", "CLA-Class", "CLC-Class", "CLE-Class", "CLK-Class",
    "CLS-Class", "E-Class", "EQA", "EQB", "EQC", "EQE", "EQS", "EQV", "G-Class", "GL-Class",
    "GLA-Class", "GLB-Class", "GLC", "GLC Coupe", "GLE", "GLE Coupe", "GLK-Class", "GLS-Class",
    "M-Class", "Metris", "R-Class", "S-Class", "SL-Class", "SLC-Class", "SLK-Class",
    "SLR McLaren", "SLS AMG", "V-Class", "X-Class", 
    "3000GT", "Airtrek", "Aspire", "ASX", "Attrage", "Bravo", "Carisma", "Celeste", "Challenger",
    "Chariot", "Chariot Grandis", "Colt", "Colt Plus", "Cordia", "Debonair", "Delica", "Delica Mini",
    "Diamante", "Dignity", "Dion", "Eclipse", "Eclipse Cross", "eK Active", "eK classy", "ek Custom",
    "eK Space", "eK Sport", "eK Wagon", "eK X", "Emeraude", "Endeavor", "Eterna", "Expo", "Freeca",
    "FTO", "Galant", "Galant Fortis", "Grandis", "Grunder", "GTO", "i", "i-MiEV", "Jeep", "L200",
    "L300", "L400", "Lancer", "Lancer Cedia", "Lancer Evolution", "Lancer EX", "Lancer Fortis",
    "Legnum", "Libero", "Minica", "Minica Toppo", "Minicab", "Minicab MiEV", "Mirage", "Mirage Dingo",
    "Montero", "Montero Sport", "Outlander", "Outlander Sport", "Pajero", "Pajero iO", "Pajero Junior",
    "Pajero Mini", "Pajero Pinin", "Pajero Sport", "Pistachio", "Proudia", "Raider", "RVR", "Sapporo",
    "Savrin", "Sigma", "Space Gear", "Space Runner", "Space Star", "Space Wagon", "Starion", "Strada",
    "Toppo", "Toppo BJ", "Toppo BJ Wide", "Town Box", "Town Box Wide", "Tredia", "Triton", "Xpander",
    "Xpander Cross", 
    "100NX", "180SX", "200SX", "240SX", "300ZX", "350Z", "370Z", "AD", "Almera", "Almera Classic",
    "Altima", "Ariya", "Armada", "Aura", "Auster", "Avenir", "Avenir Salut", "Bassara", "BE-1",
    "Bluebird", "Bluebird Maxima", "Bluebird Sylphy", "Caravan", "Caravan Elgrand", "Cedric",
    "Cedric Cima", "Cefiro", "Cherry", "Cima", "Clipper", "Crew", "Cube", "Cube Cubic", "Datsun",
    "DAYZ", "DAYZ Roox", "Dualis", "e-NV200", "Elgrand", "Exa", "Expert", "Fairlady Z", "Figaro",
    "Frontier", "Fuga", "Gloria", "Gloria Cima", "GT-R", "Homy", "Homy Elgrand", "Hypermini", "Juke",
    "Kicks", "Kix", "Lafesta", "Langley", "Lannia", "Largo", "Latio", "Laurel", "Laurel Spirit",
    "Leaf", "Leopard", "Liberta Villa", "Liberty", "Lucino", "March", "March Box", "Maxima", "Micra",
    "Micra C+C", "Mistral", "Moco", "Murano", "N7", "Navara", "Note", "NP300", "NV100 Clipper",
    "NV200", "NV350 Caravan", "NX-Coupe", "Otti", "Pao", "Pathfinder", "Patrol", "Pickup", "Pino",
    "Pixo", "Prairie", "Prairie Joy", "Presage", "Presea", "President", "Primera", "Primera Camino",
    "Pulsar", "Qashqai", "Qashqai+2", "Quest", "R'nessa", "Rasheen", "Rogue", "Rogue Sport", "Roox",
    "S-Cargo", "Safari", "Sakura", "Sentra", "Serena", "Silvia", "Skyline", "Skyline Crossover",
    "Skyline GT-R", "Stagea", "Stanza", "Sunny", "Sunny California", "Sunny RZ-1", "Sylphy", "Teana",
    "Terra", "Terrano", "Terrano II", "Terrano Regulus", "Tiida", "Tiida Latio", "Tino", "Titan",
    "Urvan", "Vanette", "Vanette Serena", "Versa", "Versa Note", "Violet", "Volkswagen Santana",
    "Wingroad", "X-Trail", "Xterra", "Z", 
    "Alcyone", "Ascent", "B9 Tribeca", "Baja", "Brat", "BRZ", "Chiffon", "Crosstrek", "Dex",
    "Dias Wagon", "Domingo", "Exiga", "Exiga Crossover 7", "Forester", "Impreza", "Impreza WRX",
    "Impreza WRX STI", "Impreza XV", "Justy", "Layback", "Legacy", "Legacy B4", "Legacy Lancaster",
    "Leone", "Levorg", "Lucra", "Outback", "Pleo", "Pleo Plus", "R1", "R2", "Rex", "Sambar",
    "Solterra", "Stella", "SVX", "Traviq", "Trezia", "Tribeca", "Vivio", "XV", 
    "356", "911", "918", "924", "928", "944", "968", "Boxster", "Carrera GT", "Cayenne",
    "Cayenne Coupe", "Cayman", "Macan", "Panamera", "Taycan", 
    "Aries", "Avenger", "Caliber", "Caravan", "Challenger", "Charger", "Dakota", "Dart", "Durango",
    "Dynasty", "Grand Caravan", "Hornet", "Intrepid", "JCUV", "Journey", "Magnum", "Neon", "Nitro",
    "Raider", "Ram", "Ramcharger", "Shadow", "Spirit", "Stealth", "Stratus", "Viper"
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        # Считаем количество записей
        total_count_marks = Mark.objects.count()
        total_count_carClasses = CarClass.objects.count()
        total_count_bodyTypes = BodyType.objects.count()
        total_count_countries = Country.objects.count()

        marks = Mark.objects.all()
        classes = CarClass.objects.all()
        body_types = BodyType.objects.all()
        countries = Country.objects.all()


        for _ in range(10):
            # Генерируем случайное число от 0 до total_count - 1
            random_index_marks = random.randint(0, total_count_marks - 1)
            random_index_carClasses = random.randint(0, total_count_carClasses - 1)
            random_index_bodyTypes = random.randint(0, total_count_bodyTypes - 1)
            random_index_countries = random.randint(0, total_count_countries - 1)

            Car.objects.create(
                model = random.choice(car_models), 
                mark_name = marks[random_index_marks], 
                car_class = classes[random_index_carClasses], 
                body_type = body_types[random_index_bodyTypes], 
                country = countries[random_index_countries]
            )