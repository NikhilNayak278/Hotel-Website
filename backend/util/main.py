# prepare_data.py
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Hotel and Menu documentation
docs = [
    # Hotel Information & Overview
    "NN Residency (Nikhil Navaneeth Residency) is a family-run boutique hotel located in the heart of Bengaluru at R V Vidyanikethan Post, Mysuru Road, Bengaluru 560059. Phone: +91 123456788. Operating since 2010, the hotel offers comfortable rooms, warm hospitality, and modern amenities including free Wi-Fi, air conditioning, flat-screen TVs, and en-suite bathrooms.",
    
    "NN Residency features: comfortable rooms & suites, complimentary continental breakfast, free Wi-Fi, 24-hour front desk & concierge service, meeting space and event support. The hotel welcomes both business and leisure travelers with personalized service and attention to detail.",
    
    "Hotel amenities include clean comfortable rooms, friendly staff, small in-house kitchen serving regional favorites, free Wi-Fi, easy access to local transport, and a relaxed atmosphere. All guests receive complimentary continental breakfast each morning.",
    
    # Room Types & Accommodations
    "NN Residency offers various room types: Standard Single Rooms (₹2,500/night) with single bed, work desk, AC, and en-suite bathroom. Standard Double Rooms (₹3,200/night) with queen-size bed, seating area, and city view. Deluxe Rooms (₹4,500/night) with premium furnishing, larger space, and premium amenities.",
    
    "Suite accommodations include: Junior Suites (₹6,000/night) with separate living area, mini-fridge, and balcony. Executive Suites (₹8,500/night) with bedroom, living room, dining area, and premium city views. All rooms include complimentary breakfast, Wi-Fi, daily housekeeping, and 24-hour room service.",
    
    "Room amenities: Air conditioning with individual controls, flat-screen LED TV with cable channels, work desk with ergonomic chair, tea/coffee making facilities, mini-fridge, electronic safe, iron and ironing board, telephone with direct dialing, and premium toiletries in en-suite bathrooms.",
    
    # Hotel Services & Facilities
    "Hotel services include: 24-hour front desk reception, concierge services for local attractions and transport, laundry and dry cleaning services, wake-up call service, luggage storage, newspaper delivery, and travel desk for booking tours and tickets.",
    
    "Business facilities: Meeting room for up to 25 people with projector and audio-visual equipment, business center with computers and printing services, high-speed internet throughout the property, conference call facilities, and secretarial services on request.",
    
    "Additional facilities: Elevator access to all floors, wheelchair accessible rooms and common areas, parking space for 15 vehicles, power backup generator, CCTV security, fire safety systems, and first aid facilities. Pet-friendly accommodation available on request.",
    
    # Location & Transportation
    "NN Residency is strategically located on Mysuru Road, one of Bengaluru's major arterial roads. The hotel is 8 km from Kempegowda International Airport, 5 km from Bengaluru City Railway Station, and 3 km from Majestic Bus Stand. Easy access to IT corridors, shopping malls, and business districts.",
    
    "Nearby attractions include: Lalbagh Botanical Garden (4 km), Cubbon Park (6 km), Vidhana Soudha (7 km), UB City Mall (5 km), Commercial Street (6 km), and Bangalore Palace (8 km). The hotel provides directions and assistance for local sightseeing.",
    
    "Transportation options: Hotel can arrange airport pickup and drop services (₹800 one way), taxi bookings for local travel, auto-rickshaw services, and guidance for public transport including buses and metro connections. Car rental services available through partner agencies.",
    
    # Breakfast Menu (served 7:00 AM - 11:00 AM)
    "Breakfast menu at NN Residency includes traditional South Indian items: Masala Dosa (₹120) - crispy rice crepe with spiced potato filling and chutneys, Idli Sambar (₹80) - steamed rice cakes with lentil soup and coconut chutney, Poha (₹60) - flattened rice with onions, curry leaves and peanuts.",
    
    "Additional breakfast options: Upma (₹70) - semolina porridge with vegetables and spices, Aloo Paratha (₹90) - stuffed potato flatbread with butter and pickle, Uttapam (₹110) - thick rice pancake with vegetables and chutneys, Medu Vada (₹85) - crispy lentil donuts with sambar and chutney.",
    
    "North Indian breakfast items: Chole Bhature (₹140) - spicy chickpeas with deep-fried bread and pickle, Rava Dosa (₹130) - crispy semolina crepe with potato curry, Puri Sabzi (₹100) - deep-fried bread with spiced potato curry. All breakfast items are freshly prepared and served hot.",
    
    "Continental breakfast options: Fresh fruit platter (₹80), cornflakes with milk (₹60), toast with butter and jam (₹50), scrambled eggs (₹90), boiled eggs (₹40), pancakes with honey (₹100), and fresh juice selection - orange, apple, watermelon (₹60 each).",
    
    # Beverages & Drinks
    "Hot beverages: Masala Chai (₹30) - traditional spiced tea, Filter Coffee (₹35) - authentic South Indian coffee, Green Tea (₹40), Black Tea (₹25), Herbal Tea varieties (₹45), Hot Chocolate (₹70), and Fresh Lemon Tea (₹35).",
    
    "Cold beverages: Fresh Lime Soda (₹45), Fresh Fruit Juices - Mango, Orange, Apple, Pomegranate (₹60-80), Lassi - Sweet and Salted (₹50), Buttermilk (₹35), Coconut Water (₹40), Soft drinks - Coke, Pepsi, Sprite (₹45), and Mineral Water bottles (₹20-40).",
    
    # Main Course Menu (served 12:00 PM - 3:00 PM and 7:00 PM - 10:30 PM)
    "Main course menu features authentic Indian cuisine: Butter Chicken (₹320) - tender chicken in rich tomato and butter gravy with naan, Lamb Biryani (₹420) - fragrant basmati rice with spiced lamb and saffron, Paneer Tikka Masala (₹280) - grilled cottage cheese in creamy tomato curry.",
    
    "Popular main dishes include: Dal Makhani (₹220) - slow-cooked black lentils in cream and butter, Fish Curry (₹350) - fresh fish in coconut and spice curry, Chicken Tikka Masala (₹340) - grilled chicken in spiced tomato cream sauce, Palak Paneer (₹260) - cottage cheese cubes in creamy spinach gravy.",
    
    "Specialty main courses: Rogan Josh (₹380) - Kashmiri lamb curry with aromatic spices, Vegetable Biryani (₹250) - fragrant rice with mixed vegetables and spices, Malai Kofta (₹290) - deep-fried vegetable balls in rich cream curry. All main courses are served with rice or bread.",
    
    "Regional specialties: Bisi Bele Bath (₹180) - traditional Karnataka rice dish, Mysore Masala Dosa (₹140), Hyderabadi Dum Biryani (₹380), Kerala Fish Curry with Appam (₹320), Bengali Fish Curry (₹340), and Rajasthani Dal Baati Churma (₹280).",
    
    "Indo-Chinese options: Chicken Manchurian (₹280), Vegetable Fried Rice (₹180), Chilli Chicken (₹300), Hakka Noodles (₹200), Gobi Manchurian (₹220), and Sweet and Sour Vegetables (₹240).",
    
    # Rice & Bread Options
    "Rice varieties: Steamed Basmati Rice (₹80), Jeera Rice (₹100), Pulao (₹120), Fried Rice - Vegetable or Egg (₹150-180), Lemon Rice (₹90), Coconut Rice (₹100), and Tomato Rice (₹95).",
    
    "Bread selection: Tandoor Roti (₹25), Butter Naan (₹45), Garlic Naan (₹55), Cheese Naan (₹65), Aloo Kulcha (₹50), Onion Kulcha (₹45), Laccha Paratha (₹35), and Roomali Roti (₹40).",
    
    # Snacks Menu (served 4:00 PM - 7:00 PM and 11:00 PM - 12:00 AM)
    "Evening snacks and light bites: Samosas (₹40) - crispy pastries filled with spiced potatoes and peas, Pani Puri (₹60) - crispy hollow puris with flavored water and chutneys, Bhel Puri (₹50) - puffed rice salad with vegetables and tangy sauces, Aloo Tikki (₹45) - crispy potato patties with mint and tamarind chutney.",
    
    "Additional snack options: Dhokla (₹70) - steamed chickpea flour cake with mustard seeds, Pakoras (₹80) - mixed vegetable fritters with mint chutney, Dahi Vada (₹65) - lentil dumplings in yogurt with sweet and tangy chutneys, Kachori (₹35) - deep-fried pastry with spiced lentil filling.",
    
    "Street food favorites: Chole Kulche (₹90) - spicy chickpeas with soft leavened bread, Raj Kachori (₹85) - large crispy shell filled with yogurt, chutneys and sev. Perfect for evening tea time or late night cravings.",
    
    "Healthy snack options: Sprouts Chaat (₹65), Fruit Chaat (₹70), Roasted Peanuts (₹30), Mixed Nuts (₹80), Fresh Cut Fruits (₹60), and Cucumber Sandwich (₹55).",
    
    # Desserts Menu (available all day)
    "Traditional Indian desserts: Gulab Jamun (₹80) - soft milk dumplings in cardamom sugar syrup, Ras Malai (₹100) - spongy cheese balls in sweetened milk with pistachios, Kheer (₹70) - creamy rice pudding with cardamom and dry fruits, Jalebi (₹60) - crispy spiral sweets soaked in sugar syrup.",
    
    "Premium dessert selection: Kulfi (₹50) - traditional Indian ice cream with cardamom and nuts, Rabri (₹90) - thick sweetened milk with almonds and pistachios, Gajar Halwa (₹85) - carrot pudding with ghee, milk and dry fruits, Rasgulla (₹65) - spongy cottage cheese balls in sugar syrup.",
    
    "Regional specialties: Mysore Pak (₹75) - rich gram flour sweet with ghee and sugar, Shrikhand (₹95) - strained yogurt dessert with saffron and cardamom. All desserts are freshly made in-house using traditional recipes.",
    
    "Ice cream varieties: Vanilla (₹60), Chocolate (₹60), Strawberry (₹60), Mango (₹70), Butterscotch (₹65), and Seasonal Fruit Flavors (₹75). Sundaes and milkshakes also available.",
    
    # Dining Policies & Information
    "Restaurant timings: Breakfast 7:00 AM - 11:00 AM, Lunch 12:00 PM - 3:00 PM, Evening Snacks 4:00 PM - 7:00 PM, Dinner 7:00 PM - 10:30 PM, Late Night Snacks 11:00 PM - 12:00 AM. Room service available 24 hours with limited menu after midnight.",
    
    "The hotel's in-house kitchen specializes in regional Indian cuisine with both vegetarian and non-vegetarian options. All ingredients are fresh and locally sourced. Special dietary requirements and custom orders can be accommodated with advance notice.",
    
    "Dining facilities include a comfortable restaurant area and room service delivery. The hotel also offers catering services for meetings and events. Guests can use the menu calculator on the hotel website to estimate meal costs before ordering.",
    
    "Food safety and hygiene: The kitchen follows strict hygiene protocols, all staff are health certified, ingredients are fresh and sourced daily, and the restaurant has FSSAI license. Special attention to cleanliness during food preparation and service.",
    
    # Hotel Policies
    "Check-in and Check-out: Standard check-in time is 2:00 PM and check-out is 12:00 PM. Early check-in and late check-out available subject to availability and may incur additional charges. Express check-in/out services available for corporate guests.",
    
    "Cancellation policy: Free cancellation up to 24 hours before arrival. Cancellations within 24 hours will be charged one night's stay. No-show will be charged full amount. Special rates may have different cancellation terms.",
    
    "Payment methods accepted: Cash, Credit Cards (Visa, MasterCard, American Express), Debit Cards, UPI payments, Net Banking, and Digital Wallets. Corporate billing and group payment arrangements available.",
    
    "Guest policies: Maximum 2 adults per standard room, extra person charges ₹800 per night, children under 12 stay free with existing bedding, smoking is prohibited in rooms but allowed in designated areas, and quiet hours from 10 PM to 7 AM.",
    
    # Events & Meetings
    "Event services: The hotel can arrange small meetings, birthday celebrations, anniversary dinners, and corporate events. Meeting room capacity is 25 people in theater style, 15 people in boardroom style. Audio-visual equipment, projector, and refreshment services available.",
    
    "Catering services: Custom menu planning for events, buffet arrangements for groups, outdoor catering within city limits, and special dietary accommodations. Advance booking required for events with minimum 2-day notice.",
    
    # Local Area & Attractions
    "Shopping nearby: UB City Mall (5 km) - luxury shopping and dining, Commercial Street (6 km) - traditional shopping, Brigade Road (7 km) - street shopping and restaurants, Forum Mall (4 km) - family entertainment and shopping.",
    
    "Healthcare facilities: Fortis Hospital (3 km), Apollo Hospital (6 km), Manipal Hospital (4 km), and several clinics and pharmacies within 2 km radius. Emergency medical assistance available 24/7.",
    
    "Educational institutions nearby: Indian Institute of Science (10 km), Bangalore University (8 km), Christ University (12 km), and several engineering colleges in the vicinity.",
    
    "Entertainment options: PVR Cinemas (4 km), Innovative Film City (25 km), Wonderla Amusement Park (30 km), and various pubs and restaurants on Brigade Road and Koramangala.",
    
    # Seasonal Information & Weather
    "Best time to visit Bengaluru: October to February when weather is pleasant. Hotel offers special winter packages during peak season. Monsoon season (June to September) brings lush greenery but occasional travel disruptions.",
    
    "Seasonal menu variations: Summer special drinks and light meals, monsoon comfort food menu, and winter special warm beverages and hearty meals. Festival special menus during Diwali, Christmas, and New Year.",
    
    # Technology & Connectivity
    "Wi-Fi details: Complimentary high-speed internet throughout the property with speeds up to 50 Mbps. Business center has dedicated connections for video conferencing. Technical support available for connectivity issues.",
    
    "Digital services: Online booking system, digital menu access via QR codes, mobile check-in options, and WhatsApp support for guest services. Hotel website features room booking, menu calculator, and local attraction information.",
    
    # Contact & Booking Information
    "Contact details: Reception +91 123456788, Restaurant +91 123456789, General Manager +91 123456790. Email: info@nnresidency.com, reservations@nnresidency.com. Website: www.nnresidency.com",
    
    "Booking channels: Direct booking through hotel website (best rates guaranteed), phone reservations, walk-in bookings, travel agent bookings, and online travel portals. Group booking discounts available for 5+ rooms.",
    
    "Emergency contacts: 24-hour front desk for all guest needs, local police station, nearest hospital, and taxi services. The hotel maintains a comprehensive list of emergency contacts and services for guest safety and convenience."
]

# Compute embeddings
embeddings = model.encode(docs).tolist()

# Store in Chroma
chroma_client = PersistentClient(path="./my_chroma_store")
collection = chroma_client.create_collection(name="docs")

for i, doc in enumerate(docs):
    collection.add(documents=[doc], embeddings=[embeddings[i]], ids=[str(i)])

print("✅ Documents stored in ChromaDB")
