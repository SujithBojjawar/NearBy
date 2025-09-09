from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Dataset: 80+ Shops from Banjara Hills, KPHB, Mehdipatnam, Gachibowli
shop_data = [
    # Banjara Hills Shops (20 total)
    {"name": "Magna Hypermarket", "category": "grocery", "latitude": 17.4149, "longitude": 78.4385, "rating": 4.5,
     "timings": "10 AM - 9 PM"},
    {"name": "Sabyasachi Boutique", "category": "fashion", "latitude": 17.4231, "longitude": 78.4397, "rating": 4.8,
     "timings": "11 AM - 8 PM"},
    {"name": "GVK One Mall", "category": "shopping", "latitude": 17.4210, "longitude": 78.4480, "rating": 4.6,
     "timings": "10 AM - 10 PM"},
    {"name": "24 Seven Store", "category": "grocery", "latitude": 17.4172, "longitude": 78.4382, "rating": 4.2,
     "timings": "24 Hours"},
    {"name": "EcoCycle E-Waste Center", "category": "e-waste", "latitude": 17.4165, "longitude": 78.4401, "rating": 4.3,
     "timings": "9 AM - 6 PM"},
    {"name": "Pixel Gaming Café", "category": "gaming", "latitude": 17.4203, "longitude": 78.4435, "rating": 4.4,
     "timings": "12 PM - 12 AM"},
    {"name": "Gadget Zone", "category": "customization", "latitude": 17.4189, "longitude": 78.4467, "rating": 4.2,
     "timings": "11 AM - 8 PM"},
    {"name": "EV Charge Point", "category": "ev-charging", "latitude": 17.4158, "longitude": 78.4379, "rating": 4.1,
     "timings": "24 Hours"},
    {"name": "WorkNest Co-Working", "category": "coworking", "latitude": 17.4240, "longitude": 78.4412, "rating": 4.6,
     "timings": "8 AM - 10 PM"},
    {"name": "Sneaker Lab", "category": "sneaker-care", "latitude": 17.4195, "longitude": 78.4450, "rating": 4.3,
     "timings": "11 AM - 7 PM"},
    {"name": "Smart Home Hub", "category": "smart-devices", "latitude": 17.4132, "longitude": 78.4390, "rating": 4.5,
     "timings": "10 AM - 8 PM"},
    {"name": "3D Print Studio", "category": "3d-printing", "latitude": 17.4220, "longitude": 78.4478, "rating": 4.4,
     "timings": "10 AM - 6 PM"},
    {"name": "PodSpace Studio", "category": "content-creation", "latitude": 17.4160, "longitude": 78.4365,
     "rating": 4.2, "timings": "9 AM - 9 PM"},
    {"name": "Quick Puncture Fix", "category": "puncture", "latitude": 17.4235, "longitude": 78.4408, "rating": 4.0,
     "timings": "8 AM - 8 PM"},
    {"name": "Tiffin Hut", "category": "tiffin", "latitude": 17.4178, "longitude": 78.4440, "rating": 4.3,
     "timings": "7 AM - 10 PM"},
    {"name": "Clean & Dry Laundry", "category": "laundry", "latitude": 17.4140, "longitude": 78.4415, "rating": 4.1,
     "timings": "8 AM - 9 PM"},
    {"name": "WoodFix Carpenter", "category": "carpenter", "latitude": 17.4215, "longitude": 78.4460, "rating": 4.2,
     "timings": "9 AM - 7 PM"},
    {"name": "Plumb & Wire Services", "category": "plumbing-electrical", "latitude": 17.4190, "longitude": 78.4420,
     "rating": 4.0, "timings": "8 AM - 8 PM"},
    {"name": "Stitch Master Tailor", "category": "tailor", "latitude": 17.4150, "longitude": 78.4380, "rating": 4.4,
     "timings": "10 AM - 7 PM"},
    {"name": "Tech Recycle Shop", "category": "second-hand", "latitude": 17.4168, "longitude": 78.4395, "rating": 4.1,
     "timings": "10 AM - 8 PM"},

    # KPHB Shops (20 total)
    {"name": "Ratnadeep Supermarket", "category": "grocery", "latitude": 17.4933, "longitude": 78.3991, "rating": 4.4,
     "timings": "7 AM - 11 PM"},
    {"name": "Brand Factory", "category": "fashion", "latitude": 17.4911, "longitude": 78.3965, "rating": 4.3,
     "timings": "10 AM - 9 PM"},
    {"name": "More Supermarket", "category": "grocery", "latitude": 17.4970, "longitude": 78.4023, "rating": 4.1,
     "timings": "8 AM - 10 PM"},
    {"name": "GreenTech E-Waste", "category": "e-waste", "latitude": 17.4905, "longitude": 78.3982, "rating": 4.2,
     "timings": "9 AM - 6 PM"},
    {"name": "GameZone Café", "category": "gaming", "latitude": 17.4952, "longitude": 78.4009, "rating": 4.5,
     "timings": "11 AM - 1 AM"},
    {"name": "SkinTech Gadgets", "category": "customization", "latitude": 17.4920, "longitude": 78.3975, "rating": 4.3,
     "timings": "11 AM - 8 PM"},
    {"name": "EV Power Hub", "category": "ev-charging", "latitude": 17.4940, "longitude": 78.4010, "rating": 4.0,
     "timings": "24 Hours"},
    {"name": "Freelance Haven", "category": "coworking", "latitude": 17.4965, "longitude": 78.3998, "rating": 4.6,
     "timings": "8 AM - 10 PM"},
    {"name": "KickClean Sneakers", "category": "sneaker-care", "latitude": 17.4890, "longitude": 78.3960, "rating": 4.4,
     "timings": "10 AM - 7 PM"},
    {"name": "IoT Solutions", "category": "smart-devices", "latitude": 17.4938, "longitude": 78.4025, "rating": 4.5,
     "timings": "10 AM - 8 PM"},
    {"name": "ProtoPrint 3D", "category": "3d-printing", "latitude": 17.4915, "longitude": 78.3988, "rating": 4.3,
     "timings": "9 AM - 6 PM"},
    {"name": "Creator’s Den", "category": "content-creation", "latitude": 17.4958, "longitude": 78.4000, "rating": 4.2,
     "timings": "10 AM - 9 PM"},
    {"name": "Tire Rescue", "category": "puncture", "latitude": 17.4925, "longitude": 78.3970, "rating": 4.1,
     "timings": "8 AM - 8 PM"},
    {"name": "Home Tiffin", "category": "tiffin", "latitude": 17.4900, "longitude": 78.3995, "rating": 4.3,
     "timings": "7 AM - 9 PM"},
    {"name": "Fresh Wash Laundry", "category": "laundry", "latitude": 17.4945, "longitude": 78.4015, "rating": 4.0,
     "timings": "8 AM - 9 PM"},
    {"name": "Furniture Fix", "category": "carpenter", "latitude": 17.4960, "longitude": 78.3980, "rating": 4.2,
     "timings": "9 AM - 7 PM"},
    {"name": "Quick Repairs", "category": "plumbing-electrical", "latitude": 17.4930, "longitude": 78.4005,
     "rating": 4.1, "timings": "8 AM - 8 PM"},
    {"name": "Custom Stitches", "category": "tailor", "latitude": 17.4918, "longitude": 78.3968, "rating": 4.4,
     "timings": "10 AM - 7 PM"},
    {"name": "Tech Reuse", "category": "second-hand", "latitude": 17.4950, "longitude": 78.3990, "rating": 4.0,
     "timings": "10 AM - 8 PM"},
    {"name": "Auto Care Hub", "category": "auto-spares", "latitude": 17.4928, "longitude": 78.4020, "rating": 4.2,
     "timings": "9 AM - 8 PM"},

    # Mehdipatnam Shops (20 total)
    {"name": "D-Mart", "category": "grocery", "latitude": 17.3951, "longitude": 78.4498, "rating": 4.6,
     "timings": "7 AM - 11 PM"},
    {"name": "RS Brothers", "category": "fashion", "latitude": 17.3930, "longitude": 78.4462, "rating": 4.5,
     "timings": "10 AM - 10 PM"},
    {"name": "Neeru’s Emporio", "category": "fashion", "latitude": 17.3964, "longitude": 78.4511, "rating": 4.7,
     "timings": "11 AM - 9 PM"},
    {"name": "Recycle Point", "category": "e-waste", "latitude": 17.3918, "longitude": 78.4474, "rating": 4.2,
     "timings": "9 AM - 6 PM"},
    {"name": "Cyber Gaming Lounge", "category": "gaming", "latitude": 17.3947, "longitude": 78.4509, "rating": 4.4,
     "timings": "11 AM - 12 AM"},
    {"name": "Phone Craft", "category": "customization", "latitude": 17.3925, "longitude": 78.4485, "rating": 4.3,
     "timings": "11 AM - 8 PM"},
    {"name": "EV Charge Stop", "category": "ev-charging", "latitude": 17.3955, "longitude": 78.4460, "rating": 4.1,
     "timings": "24 Hours"},
    {"name": "Flex Work Space", "category": "coworking", "latitude": 17.3970, "longitude": 78.4490, "rating": 4.5,
     "timings": "8 AM - 10 PM"},
    {"name": "Sneaker Spa", "category": "sneaker-care", "latitude": 17.3938, "longitude": 78.4470, "rating": 4.3,
     "timings": "10 AM - 7 PM"},
    {"name": "Smart Gadgets", "category": "smart-devices", "latitude": 17.3960, "longitude": 78.4500, "rating": 4.4,
     "timings": "10 AM - 8 PM"},
    {"name": "3D Creations", "category": "3d-printing", "latitude": 17.3940, "longitude": 78.4480, "rating": 4.2,
     "timings": "9 AM - 6 PM"},
    {"name": "VoiceBox Studio", "category": "content-creation", "latitude": 17.3920, "longitude": 78.4465,
     "rating": 4.1, "timings": "10 AM - 9 PM"},
    {"name": "Puncture Pro", "category": "puncture", "latitude": 17.3950, "longitude": 78.4495, "rating": 4.0,
     "timings": "8 AM - 8 PM"},
    {"name": "Tiffin Corner", "category": "tiffin", "latitude": 17.3935, "longitude": 78.4475, "rating": 4.3,
     "timings": "7 AM - 9 PM"},
    {"name": "Spotless Laundry", "category": "laundry", "latitude": 17.3965, "longitude": 78.4505, "rating": 4.1,
     "timings": "8 AM - 9 PM"},
    {"name": "WoodWorks", "category": "carpenter", "latitude": 17.3945, "longitude": 78.4488, "rating": 4.2,
     "timings": "9 AM - 7 PM"},
    {"name": "FixIt Services", "category": "plumbing-electrical", "latitude": 17.3928, "longitude": 78.4468,
     "rating": 4.0, "timings": "8 AM - 8 PM"},
    {"name": "Tailor’s Nook", "category": "tailor", "latitude": 17.3958, "longitude": 78.4492, "rating": 4.4,
     "timings": "10 AM - 7 PM"},
    {"name": "Gadget Resale", "category": "second-hand", "latitude": 17.3932, "longitude": 78.4472, "rating": 4.1,
     "timings": "10 AM - 8 PM"},
    {"name": "Car Spa", "category": "auto-spares", "latitude": 17.3962, "longitude": 78.4502, "rating": 4.2,
     "timings": "9 AM - 8 PM"},

    # Gachibowli Shops (20 total)
    {"name": "Decathlon", "category": "shopping", "latitude": 17.4483, "longitude": 78.3489, "rating": 4.8,
     "timings": "9 AM - 10 PM"},
    {"name": "Inorbit Mall", "category": "shopping", "latitude": 17.4338, "longitude": 78.3842, "rating": 4.6,
     "timings": "10 AM - 10 PM"},
    {"name": "Ratnadeep Supermarket", "category": "grocery", "latitude": 17.4491, "longitude": 78.3661, "rating": 4.5,
     "timings": "7 AM - 11 PM"},
    {"name": "E-Waste Solutions", "category": "e-waste", "latitude": 17.4329, "longitude": 78.3910, "rating": 4.3,
     "timings": "9 AM - 6 PM"},
    {"name": "Thunder Gaming Hub", "category": "gaming", "latitude": 17.4472, "longitude": 78.3495, "rating": 4.5,
     "timings": "11 AM - 1 AM"},
    {"name": "Custom Tech", "category": "customization", "latitude": 17.4460, "longitude": 78.3520, "rating": 4.4,
     "timings": "11 AM - 8 PM"},
    {"name": "EV Charge Zone", "category": "ev-charging", "latitude": 17.4345, "longitude": 78.3870, "rating": 4.2,
     "timings": "24 Hours"},
    {"name": "Collab Space", "category": "coworking", "latitude": 17.4485, "longitude": 78.3500, "rating": 4.6,
     "timings": "8 AM - 10 PM"},
    {"name": "Sneaker Shine", "category": "sneaker-care", "latitude": 17.4330, "longitude": 78.3850, "rating": 4.3,
     "timings": "10 AM - 7 PM"},
    {"name": "Smart Living Store", "category": "smart-devices", "latitude": 17.4475, "longitude": 78.3530,
     "rating": 4.5, "timings": "10 AM - 8 PM"},
    {"name": "PrintVerse 3D", "category": "3d-printing", "latitude": 17.4350, "longitude": 78.3890, "rating": 4.4,
     "timings": "9 AM - 6 PM"},
    {"name": "Content Cave", "category": "content-creation", "latitude": 17.4465, "longitude": 78.3510, "rating": 4.2,
     "timings": "10 AM - 9 PM"},
    {"name": "Tire Tech", "category": "puncture", "latitude": 17.4340, "longitude": 78.3860, "rating": 4.1,
     "timings": "8 AM - 8 PM"},
    {"name": "Tiffin Delight", "category": "tiffin", "latitude": 17.4480, "longitude": 78.3540, "rating": 4.3,
     "timings": "7 AM - 9 PM"},
    {"name": "PureClean Laundry", "category": "laundry", "latitude": 17.4335, "longitude": 78.3880, "rating": 4.0,
     "timings": "8 AM - 9 PM"},
    {"name": "Carpentry Corner", "category": "carpenter", "latitude": 17.4470, "longitude": 78.3525, "rating": 4.2,
     "timings": "9 AM - 7 PM"},
    {"name": "HomeFix Services", "category": "plumbing-electrical", "latitude": 17.4355, "longitude": 78.3900,
     "rating": 4.1, "timings": "8 AM - 8 PM"},
    {"name": "Sew Easy Tailor", "category": "tailor", "latitude": 17.4468, "longitude": 78.3505, "rating": 4.4,
     "timings": "10 AM - 7 PM"},
    {"name": "Tech Trade", "category": "second-hand", "latitude": 17.4348, "longitude": 78.3875, "rating": 4.0,
     "timings": "10 AM - 8 PM"},
    {"name": "Auto Zone", "category": "auto-spares", "latitude": 17.4478, "longitude": 78.3535, "rating": 4.2,
     "timings": "9 AM - 8 PM"},
]

# Convert list to DataFrame
df = pd.DataFrame(shop_data)

#  Simulated User Preference Data (category interest scores)
# For simplicity, we'll use a small dataset of user-category interactions
user_data = {
    "user": ["user1", "user1", "user1", "user2", "user2"],
    "category": ["grocery", "tiffin", "puncture", "gaming", "coworking"],
    "interest": [5, 4, 3, 5, 4]  # Simulated interest scores (1-5)
}
user_df = pd.DataFrame(user_data)

# Create a pivot table for user-category matrix
user_category_matrix = user_df.pivot_table(index="user", columns="category", values="interest", fill_value=0)

#  Train k-NN Model
knn = NearestNeighbors(metric="cosine", algorithm="brute")
knn.fit(user_category_matrix.values)


#  Function to get latitude & longitude from user address
def get_lat_lon(address):
    geolocator = Nominatim(user_agent="shop_locator")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


# Function to find the 5 nearest shops in a given category
def find_nearest_shops(user_location, category):
    filtered_shops = df[df["category"] == category]

    nearest_shops = []
    for _, shop in filtered_shops.iterrows():
        shop_location = (shop["latitude"], shop["longitude"])
        distance = geodesic(user_location, shop_location).kilometers
        nearest_shops.append((shop["name"], shop["rating"], shop["timings"], distance))

    nearest_shops.sort(key=lambda x: x[3])  # Sort by distance
    return nearest_shops[:5]  # Return top 5 nearest shops


#  Function to get AI-based shop recommendations
def get_ai_recommendations(user_id, current_category):
    # Simulate user's current interest vector
    user_vector = user_category_matrix.loc[user_id].values.reshape(1, -1)
    distances, indices = knn.kneighbors(user_vector, n_neighbors=1)  # Find similar users

    # Get categories preferred by similar users
    similar_user = user_category_matrix.iloc[indices[0][0]]
    preferred_categories = similar_user[similar_user > 0].index.tolist()

    # Filter shops from preferred categories, prioritize current category
    recommended_shops = df[df["category"].isin(preferred_categories)]
    if current_category in preferred_categories:
        recommended_shops = recommended_shops[recommended_shops["category"] == current_category]

    return recommended_shops[["name", "category", "rating", "timings"]].head(3)  # Top 3 recommendations


#  Main Program
user_id = "user1"  # Simulate a user (could be dynamic with more development)
user_colony = input("Enter your colony name: ")
user_address = input(f"Enter your address in {user_colony}: ")
full_address = f"{user_address}, {user_colony}, Hyderabad, Telangana, India"
category = input("Enter shop category (e.g., grocery, fashion, e-waste, gaming, tiffin, etc.): ").lower()

user_location = get_lat_lon(full_address)
if user_location:
    # Get nearest shops based on distance
    nearest_shops = find_nearest_shops(user_location, category)
    if nearest_shops:
        print("\nTop 5 Nearest Shops:")
        for name, rating, timings, distance in nearest_shops:
            print(f"- {name} (⭐ {rating}) - Open: {timings} - {distance:.2f} km away")
    else:
        print(f"No shops found in the '{category}' category!")

    # Get AI-based recommendations
    print("\nAI Recommendations (Based on Your Preferences):")
    ai_recommendations = get_ai_recommendations(user_id, category)
    for _, row in ai_recommendations.iterrows():
        print(f"- {row['name']} ({row['category']}) - ⭐ {row['rating']} - Open: {row['timings']}")
else:

    print("Invalid address! Please try again with a valid address.")
