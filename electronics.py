from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import datetime
import pandas as pd
from sklearn.neighbors import NearestNeighbors
shop_data = [
    # Banjara Hills
    {"name": "TechTrendz", "category": "phones", "latitude": 17.4170, "longitude": 78.4400, "rating": 4.6, "timings": "10:00-20:00",
     "stock": {"iPhone 15": 3, "Samsung S23": 0, "OnePlus 11": 5, "Google Pixel 8": 2, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "Gizmo Galaxy", "category": "tvs", "latitude": 17.4185, "longitude": 78.4425, "rating": 4.4, "timings": "09:00-21:00",
     "stock": {"LG OLED 55": 4, "Sony Bravia 50": 2, "Samsung QLED 65": 3, "TCL 43": 5, "Panasonic 60": 1},
     "prices": {"LG OLED 55": 129999, "Sony Bravia 50": 89999, "Samsung QLED 65": 149999, "TCL 43": 34999, "Panasonic 60": 79999}},
    {"name": "Phone Frenzy", "category": "phones", "latitude": 17.4200, "longitude": 78.4450, "rating": 4.3, "timings": "11:00-22:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 1, "OnePlus 11": 3, "Google Pixel 8": 0, "Xiaomi 14": 4},
     "prices": {"iPhone 15": 78999, "Samsung S23": 63999, "OnePlus 11": 55999, "Google Pixel 8": 58999, "Xiaomi 14": 48999}},
    {"name": "ElectroMart", "category": "tvs", "latitude": 17.4155, "longitude": 78.4430, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 3, "Sony Bravia 50": 1, "Samsung QLED 65": 4, "TCL 43": 2, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 125999, "Sony Bravia 50": 87999, "Samsung QLED 65": 145999, "TCL 43": 33999, "Panasonic 60": 78999}},
    {"name": "Laptop Hub", "category": "laptops", "latitude": 17.4160, "longitude": 78.4395, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 2, "Dell XPS 13": 3, "HP Spectre": 1, "Lenovo ThinkPad": 4, "Asus ZenBook": 0},
     "prices": {"MacBook Air": 99999, "Dell XPS 13": 85999, "HP Spectre": 92999, "Lenovo ThinkPad": 79999, "Asus ZenBook": 87999}},
    {"name": "CoolZone", "category": "refrigerators", "latitude": 17.4190, "longitude": 78.4410, "rating": 4.2, "timings": "10:00-19:00",
     "stock": {"Samsung 300L": 3, "LG 260L": 2, "Whirlpool 245L": 1, "Godrej 190L": 4, "Haier 320L": 0},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "WashTech", "category": "washing machines", "latitude": 17.4215, "longitude": 78.4460, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"LG 7kg": 2, "Samsung 6.5kg": 3, "Bosch 8kg": 1, "Bajaj 6kg": 4, "IFB 7.5kg": 0},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    {"name": "Mobile Haven", "category": "phones", "latitude": 17.4145, "longitude": 78.4380, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 1, "Samsung S23": 4, "OnePlus 11": 0, "Google Pixel 8": 3, "Xiaomi 14": 2},
     "prices": {"iPhone 15": 80999, "Samsung S23": 65999, "OnePlus 11": 57999, "Google Pixel 8": 60999, "Xiaomi 14": 50999}},
    {"name": "TV Spot", "category": "tvs", "latitude": 17.4220, "longitude": 78.4475, "rating": 4.2, "timings": "10:00-20:00",
     "stock": {"LG OLED 55": 2, "Sony Bravia 50": 0, "Samsung QLED 65": 5, "TCL 43": 1, "Panasonic 60": 3},
     "prices": {"LG OLED 55": 127999, "Sony Bravia 50": 88999, "Samsung QLED 65": 147999, "TCL 43": 35999, "Panasonic 60": 77999}},
    {"name": "Reliance Digital", "category": "laptops", "latitude": 17.4130, "longitude": 78.4365, "rating": 4.6, "timings": "10:00-22:00",
     "stock": {"MacBook Air": 3, "Dell XPS 13": 2, "HP Spectre": 4, "Lenovo ThinkPad": 1, "Asus ZenBook": 0},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    {"name": "Frosty Deals", "category": "refrigerators", "latitude": 17.4235, "longitude": 78.4480, "rating": 4.1, "timings": "09:00-19:00",
     "stock": {"Samsung 300L": 2, "LG 260L": 3, "Whirlpool 245L": 0, "Godrej 190L": 5, "Haier 320L": 1},
     "prices": {"Samsung 300L": 33999, "LG 260L": 31999, "Whirlpool 245L": 28999, "Godrej 190L": 23999, "Haier 320L": 35999}},
    {"name": "Bajaj Store", "category": "washing machines", "latitude": 17.4168, "longitude": 78.4418, "rating": 4.3, "timings": "10:00-20:00",
     "stock": {"LG 7kg": 1, "Samsung 6.5kg": 2, "Bosch 8kg": 3, "Bajaj 6kg": 5, "IFB 7.5kg": 0},
     "prices": {"LG 7kg": 27999, "Samsung 6.5kg": 24999, "Bosch 8kg": 32999, "Bajaj 6kg": 18999, "IFB 7.5kg": 30999}},
    {"name": "Phone Stop", "category": "phones", "latitude": 17.4180, "longitude": 78.4465, "rating": 4.4, "timings": "09:00-21:00",
     "stock": {"iPhone 15": 4, "Samsung S23": 2, "OnePlus 11": 1, "Google Pixel 8": 3, "Xiaomi 14": 0},
     "prices": {"iPhone 15": 77999, "Samsung S23": 62999, "OnePlus 11": 54999, "Google Pixel 8": 57999, "Xiaomi 14": 47999}},
    {"name": "TV Plaza", "category": "tvs", "latitude": 17.4150, "longitude": 78.4375, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"LG OLED 55": 1, "Sony Bravia 50": 3, "Samsung QLED 65": 2, "TCL 43": 4, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 128999, "Sony Bravia 50": 90999, "Samsung QLED 65": 148999, "TCL 43": 36999, "Panasonic 60": 78999}},
    {"name": "Laptop City", "category": "laptops", "latitude": 17.4205, "longitude": 78.4435, "rating": 4.3, "timings": "10:00-20:00",
     "stock": {"MacBook Air": 0, "Dell XPS 13": 4, "HP Spectre": 2, "Lenovo ThinkPad": 3, "Asus ZenBook": 1},
     "prices": {"MacBook Air": 97999, "Dell XPS 13": 83999, "HP Spectre": 90999, "Lenovo ThinkPad": 77999, "Asus ZenBook": 85999}},
    {"name": "ChillMart", "category": "refrigerators", "latitude": 17.4175, "longitude": 78.4390, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 4, "LG 260L": 1, "Whirlpool 245L": 3, "Godrej 190L": 0, "Haier 320L": 2},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashZone", "category": "washing machines", "latitude": 17.4195, "longitude": 78.4440, "rating": 4.2, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 3, "Samsung 6.5kg": 0, "Bosch 8kg": 2, "Bajaj 6kg": 4, "IFB 7.5kg": 1},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
    {"name": "TechBit", "category": "phones", "latitude": 17.4140, "longitude": 78.4420, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 3, "OnePlus 11": 0, "Google Pixel 8": 4, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "ScreenZone", "category": "tvs", "latitude": 17.4210, "longitude": 78.4405, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 3, "Sony Bravia 50": 1, "Samsung QLED 65": 4, "TCL 43": 0, "Panasonic 60": 2},
     "prices": {"LG OLED 55": 126999, "Sony Bravia 50": 87999, "Samsung QLED 65": 146999, "TCL 43": 33999, "Panasonic 60": 76999}},
    {"name": "ComputeShop", "category": "laptops", "latitude": 17.4165, "longitude": 78.4455, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 1, "Dell XPS 13": 3, "HP Spectre": 0, "Lenovo ThinkPad": 2, "Asus ZenBook": 4},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    # KPHB
    {"name": "TechZone KPHB", "category": "phones", "latitude": 17.4911, "longitude": 78.3965, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 1, "Samsung S23": 3, "OnePlus 11": 2, "Google Pixel 8": 4, "Xiaomi 14": 0},
     "prices": {"iPhone 15": 80999, "Samsung S23": 65999, "OnePlus 11": 57999, "Google Pixel 8": 60999, "Xiaomi 14": 50999}},
    {"name": "Mobile Mania", "category": "phones", "latitude": 17.4970, "longitude": 78.4023, "rating": 4.2, "timings": "09:00-20:00",
     "stock": {"iPhone 15": 0, "Samsung S23": 2, "OnePlus 11": 1, "Google Pixel 8": 3, "Xiaomi 14": 5},
     "prices": {"iPhone 15": 77999, "Samsung S23": 62999, "OnePlus 11": 54999, "Google Pixel 8": 57999, "Xiaomi 14": 47999}},
    {"name": "TV World", "category": "tvs", "latitude": 17.4935, "longitude": 78.3990, "rating": 4.3, "timings": "10:00-20:00",
     "stock": {"LG OLED 55": 2, "Sony Bravia 50": 3, "Samsung QLED 65": 1, "TCL 43": 4, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 127999, "Sony Bravia 50": 88999, "Samsung QLED 65": 147999, "TCL 43": 35999, "Panasonic 60": 77999}},
    {"name": "Reliance Digital KPHB", "category": "laptops", "latitude": 17.4950, "longitude": 78.4005, "rating": 4.6, "timings": "10:00-22:00",
     "stock": {"MacBook Air": 3, "Dell XPS 13": 2, "HP Spectre": 4, "Lenovo ThinkPad": 1, "Asus ZenBook": 0},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    {"name": "Frosty Deals KPHB", "category": "refrigerators", "latitude": 17.4920, "longitude": 78.3975, "rating": 4.1, "timings": "09:00-19:00",
     "stock": {"Samsung 300L": 2, "LG 260L": 3, "Whirlpool 245L": 0, "Godrej 190L": 5, "Haier 320L": 1},
     "prices": {"Samsung 300L": 33999, "LG 260L": 31999, "Whirlpool 245L": 28999, "Godrej 190L": 23999, "Haier 320L": 35999}},
    {"name": "Bajaj Store KPHB", "category": "washing machines", "latitude": 17.4945, "longitude": 78.4010, "rating": 4.3, "timings": "10:00-20:00",
     "stock": {"LG 7kg": 1, "Samsung 6.5kg": 2, "Bosch 8kg": 3, "Bajaj 6kg": 5, "IFB 7.5kg": 0},
     "prices": {"LG 7kg": 27999, "Samsung 6.5kg": 24999, "Bosch 8kg": 32999, "Bajaj 6kg": 18999, "IFB 7.5kg": 30999}},
    {"name": "Phone Galaxy", "category": "phones", "latitude": 17.4900, "longitude": 78.3950, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 3, "Samsung S23": 0, "OnePlus 11": 4, "Google Pixel 8": 2, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "TV Haven KPHB", "category": "tvs", "latitude": 17.4960, "longitude": 78.4030, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 4, "Sony Bravia 50": 1, "Samsung QLED 65": 3, "TCL 43": 0, "Panasonic 60": 2},
     "prices": {"LG OLED 55": 129999, "Sony Bravia 50": 89999, "Samsung QLED 65": 149999, "TCL 43": 34999, "Panasonic 60": 79999}},
    {"name": "Laptop Point", "category": "laptops", "latitude": 17.4930, "longitude": 78.3985, "rating": 4.2, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 2, "Dell XPS 13": 0, "HP Spectre": 3, "Lenovo ThinkPad": 4, "Asus ZenBook": 1},
     "prices": {"MacBook Air": 99999, "Dell XPS 13": 85999, "HP Spectre": 92999, "Lenovo ThinkPad": 79999, "Asus ZenBook": 87999}},
    {"name": "CoolMart KPHB", "category": "refrigerators", "latitude": 17.4915, "longitude": 78.3960, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 1, "LG 260L": 4, "Whirlpool 245L": 2, "Godrej 190L": 3, "Haier 320L": 0},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "WashPoint KPHB", "category": "washing machines", "latitude": 17.4955, "longitude": 78.4020, "rating": 4.4, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 3, "Samsung 6.5kg": 1, "Bosch 8kg": 0, "Bajaj 6kg": 4, "IFB 7.5kg": 2},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    {"name": "TechSphere", "category": "phones", "latitude": 17.4925, "longitude": 78.3995, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 4, "OnePlus 11": 0, "Google Pixel 8": 3, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 78999, "Samsung S23": 63999, "OnePlus 11": 55999, "Google Pixel 8": 58999, "Xiaomi 14": 48999}},
    {"name": "ScreenMart", "category": "tvs", "latitude": 17.4940, "longitude": 78.3970, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 3, "Sony Bravia 50": 0, "Samsung QLED 65": 2, "TCL 43": 4, "Panasonic 60": 1},
     "prices": {"LG OLED 55": 126999, "Sony Bravia 50": 87999, "Samsung QLED 65": 146999, "TCL 43": 33999, "Panasonic 60": 76999}},
    {"name": "ComputeZone", "category": "laptops", "latitude": 17.4965, "longitude": 78.4015, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 4, "Dell XPS 13": 1, "HP Spectre": 3, "Lenovo ThinkPad": 0, "Asus ZenBook": 2},
     "prices": {"MacBook Air": 99999, "Dell XPS 13": 85999, "HP Spectre": 92999, "Lenovo ThinkPad": 79999, "Asus ZenBook": 87999}},
    {"name": "ChillZone KPHB", "category": "refrigerators", "latitude": 17.4905, "longitude": 78.3945, "rating": 4.2, "timings": "09:00-19:00",
     "stock": {"Samsung 300L": 3, "LG 260L": 0, "Whirlpool 245L": 4, "Godrej 190L": 2, "Haier 320L": 1},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashMart KPHB", "category": "washing machines", "latitude": 17.4938, "longitude": 78.4000, "rating": 4.5, "timings": "10:00-20:00",
     "stock": {"LG 7kg": 2, "Samsung 6.5kg": 4, "Bosch 8kg": 1, "Bajaj 6kg": 3, "IFB 7.5kg": 0},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
    {"name": "Phone Nexus", "category": "phones", "latitude": 17.4918, "longitude": 78.3980, "rating": 4.3, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 1, "Samsung S23": 3, "OnePlus 11": 2, "Google Pixel 8": 0, "Xiaomi 14": 4},
     "prices": {"iPhone 15": 80999, "Samsung S23": 65999, "OnePlus 11": 57999, "Google Pixel 8": 60999, "Xiaomi 14": 50999}},
    {"name": "TV Nexus", "category": "tvs", "latitude": 17.4952, "longitude": 78.4025, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 2, "Sony Bravia 50": 4, "Samsung QLED 65": 1, "TCL 43": 3, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 128999, "Sony Bravia 50": 90999, "Samsung QLED 65": 148999, "TCL 43": 36999, "Panasonic 60": 78999}},
    {"name": "Laptop Nexus KPHB", "category": "laptops", "latitude": 17.4928, "longitude": 78.3968, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 3, "Dell XPS 13": 0, "HP Spectre": 2, "Lenovo ThinkPad": 4, "Asus ZenBook": 1},
     "prices": {"MacBook Air": 97999, "Dell XPS 13": 83999, "HP Spectre": 90999, "Lenovo ThinkPad": 77999, "Asus ZenBook": 85999}},
    # Mehdipatnam
    {"name": "Mobile Planet", "category": "phones", "latitude": 17.3930, "longitude": 78.4462, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 3, "Samsung S23": 0, "OnePlus 11": 4, "Google Pixel 8": 1, "Xiaomi 14": 2},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "TV Haven", "category": "tvs", "latitude": 17.3964, "longitude": 78.4511, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 1, "Sony Bravia 50": 4, "Samsung QLED 65": 2, "TCL 43": 3, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 128999, "Sony Bravia 50": 90999, "Samsung QLED 65": 148999, "TCL 43": 36999, "Panasonic 60": 78999}},
    {"name": "Laptop Zone", "category": "laptops", "latitude": 17.3945, "longitude": 78.4480, "rating": 4.2, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 1, "Dell XPS 13": 3, "HP Spectre": 0, "Lenovo ThinkPad": 2, "Asus ZenBook": 4},
     "prices": {"MacBook Air": 97999, "Dell XPS 13": 83999, "HP Spectre": 90999, "Lenovo ThinkPad": 77999, "Asus ZenBook": 85999}},
    {"name": "Reliance Cool", "category": "refrigerators", "latitude": 17.3955, "longitude": 78.4495, "rating": 4.5, "timings": "10:00-20:00",
     "stock": {"Samsung 300L": 4, "LG 260L": 1, "Whirlpool 245L": 3, "Godrej 190L": 0, "Haier 320L": 2},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashMart", "category": "washing machines", "latitude": 17.3925, "longitude": 78.4470, "rating": 4.3, "timings": "09:00-19:00",
     "stock": {"LG 7kg": 3, "Samsung 6.5kg": 0, "Bosch 8kg": 2, "Bajaj 6kg": 4, "IFB 7.5kg": 1},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
    {"name": "Phone Palace", "category": "phones", "latitude": 17.3915, "longitude": 78.4450, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 4, "OnePlus 11": 0, "Google Pixel 8": 3, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 78999, "Samsung S23": 63999, "OnePlus 11": 55999, "Google Pixel 8": 58999, "Xiaomi 14": 48999}},
    {"name": "ScreenHaven", "category": "tvs", "latitude": 17.3970, "longitude": 78.4520, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 3, "Sony Bravia 50": 0, "Samsung QLED 65": 4, "TCL 43": 2, "Panasonic 60": 1},
     "prices": {"LG OLED 55": 126999, "Sony Bravia 50": 87999, "Samsung QLED 65": 146999, "TCL 43": 33999, "Panasonic 60": 76999}},
    {"name": "ComputeMart", "category": "laptops", "latitude": 17.3935, "longitude": 78.4465, "rating": 4.3, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 4, "Dell XPS 13": 1, "HP Spectre": 3, "Lenovo ThinkPad": 0, "Asus ZenBook": 2},
     "prices": {"MacBook Air": 99999, "Dell XPS 13": 85999, "HP Spectre": 92999, "Lenovo ThinkPad": 79999, "Asus ZenBook": 87999}},
    {"name": "FrostMart", "category": "refrigerators", "latitude": 17.3960, "longitude": 78.4500, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 2, "LG 260L": 4, "Whirlpool 245L": 0, "Godrej 190L": 3, "Haier 320L": 1},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "WashHaven", "category": "washing machines", "latitude": 17.3940, "longitude": 78.4485, "rating": 4.2, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 1, "Samsung 6.5kg": 3, "Bosch 8kg": 4, "Bajaj 6kg": 0, "IFB 7.5kg": 2},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    {"name": "TechPulse Mehdipatnam", "category": "phones", "latitude": 17.3920, "longitude": 78.4445, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 3, "Samsung S23": 1, "OnePlus 11": 4, "Google Pixel 8": 0, "Xiaomi 14": 2},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "TV Pulse", "category": "tvs", "latitude": 17.3950, "longitude": 78.4475, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 2, "Sony Bravia 50": 3, "Samsung QLED 65": 1, "TCL 43": 4, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 127999, "Sony Bravia 50": 88999, "Samsung QLED 65": 147999, "TCL 43": 35999, "Panasonic 60": 77999}},
    {"name": "Laptop Pulse", "category": "laptops", "latitude": 17.3975, "longitude": 78.4515, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 0, "Dell XPS 13": 2, "HP Spectre": 4, "Lenovo ThinkPad": 1, "Asus ZenBook": 3},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    {"name": "CoolPulse", "category": "refrigerators", "latitude": 17.3910, "longitude": 78.4455, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 3, "LG 260L": 0, "Whirlpool 245L": 2, "Godrej 190L": 4, "Haier 320L": 1},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashPulse", "category": "washing machines", "latitude": 17.3965, "longitude": 78.4490, "rating": 4.3, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 4, "Samsung 6.5kg": 1, "Bosch 8kg": 3, "Bajaj 6kg": 0, "IFB 7.5kg": 2},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
    {"name": "PhoneTrendz", "category": "phones", "latitude": 17.3938, "longitude": 78.4478, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 1, "Samsung S23": 3, "OnePlus 11": 2, "Google Pixel 8": 4, "Xiaomi 14": 0},
     "prices": {"iPhone 15": 80999, "Samsung S23": 65999, "OnePlus 11": 57999, "Google Pixel 8": 60999, "Xiaomi 14": 50999}},
    {"name": "TVTrendz", "category": "tvs", "latitude": 17.3952, "longitude": 78.4505, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 4, "Sony Bravia 50": 2, "Samsung QLED 65": 0, "TCL 43": 3, "Panasonic 60": 1},
     "prices": {"LG OLED 55": 129999, "Sony Bravia 50": 89999, "Samsung QLED 65": 149999, "TCL 43": 34999, "Panasonic 60": 79999}},
    {"name": "LaptopTrendz", "category": "laptops", "latitude": 17.3928, "longitude": 78.4460, "rating": 4.2, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 2, "Dell XPS 13": 4, "HP Spectre": 1, "Lenovo ThinkPad": 3, "Asus ZenBook": 0},
     "prices": {"MacBook Air": 97999, "Dell XPS 13": 83999, "HP Spectre": 90999, "Lenovo ThinkPad": 77999, "Asus ZenBook": 85999}},
    {"name": "FrostTrendz", "category": "refrigerators", "latitude": 17.3972, "longitude": 78.4525, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 1, "LG 260L": 3, "Whirlpool 245L": 4, "Godrej 190L": 0, "Haier 320L": 2},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "WashTrendz", "category": "washing machines", "latitude": 17.3942, "longitude": 78.4488, "rating": 4.4, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 3, "Samsung 6.5kg": 0, "Bosch 8kg": 2, "Bajaj 6kg": 4, "IFB 7.5kg": 1},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    # Gachibowli
    {"name": "TechPulse", "category": "phones", "latitude": 17.4472, "longitude": 78.3495, "rating": 4.6, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 4, "OnePlus 11": 0, "Google Pixel 8": 3, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 78999, "Samsung S23": 63999, "OnePlus 11": 55999, "Google Pixel 8": 58999, "Xiaomi 14": 48999}},
    {"name": "TV Fusion", "category": "tvs", "latitude": 17.4338, "longitude": 78.3842, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 3, "Sony Bravia 50": 0, "Samsung QLED 65": 2, "TCL 43": 4, "Panasonic 60": 1},
     "prices": {"LG OLED 55": 126999, "Sony Bravia 50": 87999, "Samsung QLED 65": 146999, "TCL 43": 33999, "Panasonic 60": 76999}},
    {"name": "Laptop Nexus", "category": "laptops", "latitude": 17.4465, "longitude": 78.3510, "rating": 4.5, "timings": "10:00-22:00",
     "stock": {"MacBook Air": 4, "Dell XPS 13": 1, "HP Spectre": 3, "Lenovo ThinkPad": 0, "Asus ZenBook": 2},
     "prices": {"MacBook Air": 99999, "Dell XPS 13": 85999, "HP Spectre": 92999, "Lenovo ThinkPad": 79999, "Asus ZenBook": 87999}},
    {"name": "FrostZone", "category": "refrigerators", "latitude": 17.4480, "longitude": 78.3500, "rating": 4.3, "timings": "10:00-20:00",
     "stock": {"Samsung 300L": 1, "LG 260L": 4, "Whirlpool 245L": 2, "Godrej 190L": 3, "Haier 320L": 0},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "Reliance Wash", "category": "washing machines", "latitude": 17.4345, "longitude": 78.3870, "rating": 4.2, "timings": "09:00-19:00",
     "stock": {"LG 7kg": 4, "Samsung 6.5kg": 1, "Bosch 8kg": 0, "Bajaj 6kg": 3, "IFB 7.5kg": 2},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    {"name": "Phone Fusion", "category": "phones", "latitude": 17.4450, "longitude": 78.3480, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 3, "Samsung S23": 1, "OnePlus 11": 4, "Google Pixel 8": 0, "Xiaomi 14": 2},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "ScreenFusion", "category": "tvs", "latitude": 17.4320, "longitude": 78.3850, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 2, "Sony Bravia 50": 4, "Samsung QLED 65": 1, "TCL 43": 3, "Panasonic 60": 0},
     "prices": {"LG OLED 55": 128999, "Sony Bravia 50": 90999, "Samsung QLED 65": 148999, "TCL 43": 36999, "Panasonic 60": 78999}},
    {"name": "ComputeFusion", "category": "laptops", "latitude": 17.4475, "longitude": 78.3525, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 1, "Dell XPS 13": 3, "HP Spectre": 0, "Lenovo ThinkPad": 4, "Asus ZenBook": 2},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    {"name": "CoolFusion", "category": "refrigerators", "latitude": 17.4335, "longitude": 78.3860, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 4, "LG 260L": 2, "Whirlpool 245L": 1, "Godrej 190L": 3, "Haier 320L": 0},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashFusion", "category": "washing machines", "latitude": 17.4460, "longitude": 78.3490, "rating": 4.3, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 2, "Samsung 6.5kg": 4, "Bosch 8kg": 1, "Bajaj 6kg": 0, "IFB 7.5kg": 3},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
    {"name": "TechTrendz Gachibowli", "category": "phones", "latitude": 17.4485, "longitude": 78.3515, "rating": 4.6, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 4, "Samsung S23": 0, "OnePlus 11": 3, "Google Pixel 8": 2, "Xiaomi 14": 1},
     "prices": {"iPhone 15": 80999, "Samsung S23": 65999, "OnePlus 11": 57999, "Google Pixel 8": 60999, "Xiaomi 14": 50999}},
    {"name": "TVTrendz Gachibowli", "category": "tvs", "latitude": 17.4340, "longitude": 78.3880, "rating": 4.4, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 1, "Sony Bravia 50": 3, "Samsung QLED 65": 4, "TCL 43": 0, "Panasonic 60": 2},
     "prices": {"LG OLED 55": 127999, "Sony Bravia 50": 88999, "Samsung QLED 65": 147999, "TCL 43": 35999, "Panasonic 60": 77999}},
    {"name": "LaptopTrendz Gachibowli", "category": "laptops", "latitude": 17.4455, "longitude": 78.3475, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 3, "Dell XPS 13": 0, "HP Spectre": 2, "Lenovo ThinkPad": 4, "Asus ZenBook": 1},
     "prices": {"MacBook Air": 97999, "Dell XPS 13": 83999, "HP Spectre": 90999, "Lenovo ThinkPad": 77999, "Asus ZenBook": 85999}},
    {"name": "FrostTrendz Gachibowli", "category": "refrigerators", "latitude": 17.4470, "longitude": 78.3505, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 2, "LG 260L": 4, "Whirlpool 245L": 0, "Godrej 190L": 3, "Haier 320L": 1},
     "prices": {"Samsung 300L": 34999, "LG 260L": 32999, "Whirlpool 245L": 29999, "Godrej 190L": 24999, "Haier 320L": 36999}},
    {"name": "WashTrendz Gachibowli", "category": "washing machines", "latitude": 17.4330, "longitude": 78.3865, "rating": 4.4, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 3, "Samsung 6.5kg": 1, "Bosch 8kg": 4, "Bajaj 6kg": 0, "IFB 7.5kg": 2},
     "prices": {"LG 7kg": 28999, "Samsung 6.5kg": 25999, "Bosch 8kg": 33999, "Bajaj 6kg": 19999, "IFB 7.5kg": 31999}},
    {"name": "PhoneZone Gachibowli", "category": "phones", "latitude": 17.4468, "longitude": 78.3520, "rating": 4.5, "timings": "10:00-21:00",
     "stock": {"iPhone 15": 2, "Samsung S23": 3, "OnePlus 11": 1, "Google Pixel 8": 4, "Xiaomi 14": 0},
     "prices": {"iPhone 15": 79999, "Samsung S23": 64999, "OnePlus 11": 56999, "Google Pixel 8": 59999, "Xiaomi 14": 49999}},
    {"name": "ScreenZone Gachibowli", "category": "tvs", "latitude": 17.4350, "longitude": 78.3890, "rating": 4.3, "timings": "09:00-20:00",
     "stock": {"LG OLED 55": 4, "Sony Bravia 50": 1, "Samsung QLED 65": 3, "TCL 43": 0, "Panasonic 60": 2},
     "prices": {"LG OLED 55": 129999, "Sony Bravia 50": 89999, "Samsung QLED 65": 149999, "TCL 43": 34999, "Panasonic 60": 79999}},
    {"name": "ComputeZone Gachibowli", "category": "laptops", "latitude": 17.4482, "longitude": 78.3530, "rating": 4.4, "timings": "10:00-21:00",
     "stock": {"MacBook Air": 1, "Dell XPS 13": 4, "HP Spectre": 2, "Lenovo ThinkPad": 3, "Asus ZenBook": 0},
     "prices": {"MacBook Air": 98999, "Dell XPS 13": 84999, "HP Spectre": 91999, "Lenovo ThinkPad": 78999, "Asus ZenBook": 86999}},
    {"name": "ChillZone Gachibowli", "category": "refrigerators", "latitude": 17.4445, "longitude": 78.3470, "rating": 4.5, "timings": "09:00-20:00",
     "stock": {"Samsung 300L": 3, "LG 260L": 1, "Whirlpool 245L": 4, "Godrej 190L": 0, "Haier 320L": 2},
     "prices": {"Samsung 300L": 35999, "LG 260L": 33999, "Whirlpool 245L": 30999, "Godrej 190L": 25999, "Haier 320L": 37999}},
    {"name": "WashZone Gachibowli", "category": "washing machines", "latitude": 17.4462, "longitude": 78.3512, "rating": 4.3, "timings": "10:00-19:00",
     "stock": {"LG 7kg": 2, "Samsung 6.5kg": 3, "Bosch 8kg": 0, "Bajaj 6kg": 4, "IFB 7.5kg": 1},
     "prices": {"LG 7kg": 29999, "Samsung 6.5kg": 26999, "Bosch 8kg": 34999, "Bajaj 6kg": 20999, "IFB 7.5kg": 32999}},
]

df = pd.DataFrame(shop_data)
user_data = {"user": ["user1", "user1", "user1", "user1", "user1"],
             "category": ["phones", "tvs", "laptops", "refrigerators", "washing machines"],
             "interest": [5, 4, 3, 2, 1]}
user_df = pd.DataFrame(user_data)
user_category_matrix = user_df.pivot_table(index="user", columns="category", values="interest", fill_value=0)
knn = NearestNeighbors(metric="cosine", algorithm="brute")
knn.fit(user_category_matrix.values)

def get_lat_lon(address):
    geolocator = Nominatim(user_agent="shop_locator")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def is_open_now(timings):
    now = datetime.now()
    current_time = now.hour * 100 + now.minute
    start, end = map(lambda x: int(x.replace(":", "")), timings.split("-"))
    return start <= current_time <= end

def find_nearest_shops(user_location, category, item=None):
    filtered_shops = df[df["category"] == category]
    nearest_shops = []
    for _, shop in filtered_shops.iterrows():
        shop_location = (shop["latitude"], shop["longitude"])
        distance = geodesic(user_location, shop_location).kilometers
        open_now = "Yes" if is_open_now(shop["timings"]) else "No"
        stock_status = "Unknown"
        price = "N/A"
        if item and item in shop["stock"]:
            stock_status = "In Stock" if shop["stock"][item] > 0 else "Out of Stock"
            price = shop["prices"][item] if stock_status == "In Stock" else "N/A"
        nearest_shops.append((shop["name"], shop["rating"], distance, open_now, stock_status, price))
    nearest_shops.sort(key=lambda x: x[2])
    return nearest_shops[:5]

def get_ai_recommendations(user_id, current_category):
    user_vector = user_category_matrix.loc[user_id].values.reshape(1, -1)
    _, indices = knn.kneighbors(user_vector, n_neighbors=1)
    similar_user = user_category_matrix.iloc[indices[0][0]]
    preferred_categories = similar_user[similar_user > 0].index.tolist()
    recommended_shops = df[df["category"].isin(preferred_categories)]
    if current_category in preferred_categories:
        recommended_shops = recommended_shops[recommended_shops["category"] == current_category]
    return recommended_shops[["name", "category", "rating", "timings"]].head(3)

user_id = "user1"
user_colony = input("Enter your colony name: ")
user_address = input(f"Enter your address in {user_colony}: ")
full_address = f"{user_address}, {user_colony}, Hyderabad, Telangana, India"
category = input("Enter category (phones, tvs, laptops, refrigerators, washing machines): ").lower()
item = input(f"Enter item to check (e.g., iPhone 15, LG OLED 55, MacBook Air, Samsung 300L, LG 7kg) or leave blank: ") or None
user_location = get_lat_lon(full_address)
if user_location:
    nearest_shops = find_nearest_shops(user_location, category, item)
    if nearest_shops:
        print("\nTop 5 Nearest Shops:")
        for name, rating, distance, open_now, stock_status, price in nearest_shops:
            print(f"Shop: {name}")
            print(f"Rating: {rating}")
            print(f"Distance: {distance:.2f} km")
            print(f"Open Now: {open_now}")
            print(f"Stock: {stock_status}")
            print(f"Price: {price}")
            print("---")
    else:
        print(f"No shops found in the '{category}' category!")
    ai_recommendations = get_ai_recommendations(user_id, category)
    for _, row in ai_recommendations.iterrows():
        print(f"Shop: {row['name']}")
        print(f"Category: {row['category']}")
        print(f"Rating: {row['rating']}")
        print(f"Open: {row['timings']}")
        print("---")
else:
    print("Invalid address! Please try again with a valid address.")