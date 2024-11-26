import random
import logging

def random_allocation(hotel_data, guest_data):
    hotels_copy = hotel_data.copy()
    allocation = []

    guest_ids = guest_data.index.tolist()
    random.shuffle(guest_ids)

    for guest_id in guest_ids:
        available_hotels = hotels_copy[hotels_copy['rooms'] > 0]
        if not available_hotels.empty:
            hotel_id = available_hotels.sample().index[0]
            hotel = available_hotels.loc[hotel_id]
            allocation.append({
                'guest_id': guest_id,
                'hotel_id': hotel_id,
                'final_price': float(hotel['price'] * (1 - guest_data.loc[guest_id, 'discount']))
            })
            hotels_copy.at[hotel_id, 'rooms'] -= 1
            logging.info("Random allocation: Guest %s assigned to hotel %s", guest_id, hotel_id)
        else:
            logging.info("Random allocation: Guest %s not assigned due to lack of available rooms", guest_id)

    return allocation

def preference_allocation(hotel_data, guest_data, preferences_data):
    hotels_copy = hotel_data.copy()
    allocation = []

    preferences_grouped = preferences_data.groupby('guest')

    for guest_id in guest_data.index:
        allocated = False

        if guest_id in preferences_grouped.groups:
            preferred_hotels = preferences_grouped.get_group(guest_id).sort_values('priority')
            available_hotels = preferred_hotels[preferred_hotels['hotel'].isin(hotels_copy[hotels_copy['rooms'] > 0].index)]
            if not available_hotels.empty:
                hotel_id = available_hotels.iloc[0]['hotel']
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': hotel_id,
                    'final_price': float(hotels_copy.loc[hotel_id, 'price'] * (1 - guest_data.loc[guest_id, 'discount']))
                })
                hotels_copy.at[hotel_id, 'rooms'] -= 1
                allocated = True
                logging.info("Preference allocation: Guest %s assigned to hotel %s", guest_id, hotel_id)

        if not allocated:
            available_hotels = hotels_copy[hotels_copy['rooms'] > 0]
            if not available_hotels.empty:
                hotel_id = available_hotels.index[0]
                hotel = available_hotels.loc[hotel_id]
                allocation.append({
                    'guest_id': guest_id,
                    'hotel_id': hotel_id,
                    'final_price': float(hotel['price'] * (1 - guest_data.loc[guest_id, 'discount']))
                })
                hotels_copy.at[hotel_id, 'rooms'] -= 1
                logging.info("Preference allocation: Guest %s assigned to hotel %s as fallback", guest_id, hotel_id)
            else:
                logging.warning("Preference allocation: No available rooms for guest %s", guest_id)

    return allocation

def price_allocation(hotel_data, guest_data):
    hotels_copy = hotel_data.sort_values('price').copy()
    allocation = []

    for guest_id in guest_data.index:
        available_hotels = hotels_copy[hotels_copy['rooms'] > 0]
        if not available_hotels.empty:
            hotel_id = available_hotels.index[0]
            hotel = available_hotels.loc[hotel_id]
            allocation.append({
                'guest_id': guest_id,
                'hotel_id': hotel_id,
                'final_price': float(hotel['price'] * (1 - guest_data.loc[guest_id, 'discount']))
            })
            hotels_copy.at[hotel_id, 'rooms'] -= 1
            logging.info("Price allocation: Guest %s assigned to cheapest hotel %s", guest_id, hotel_id)
        else:
            logging.warning("Price allocation: No available rooms for guest %s", guest_id)

    return allocation

def availability_allocation_optimized(hotel_data, guest_data):
    """
    Allocates guests to hotels based on room availability, starting with the most roomy hotel.
    Optimized to reduce iteration time and improve efficiency.
    """
    hotels_copy = hotel_data.sort_values('rooms', ascending=False).copy()
    allocation = []

    for guest_id in guest_data.index:
        available_hotels = hotels_copy[hotels_copy['rooms'] > 0]
        if not available_hotels.empty:
            hotel_id = available_hotels.index[0]
            hotel = available_hotels.loc[hotel_id]
            allocation.append({
                'guest_id': guest_id,
                'hotel_id': hotel_id,
                'final_price': float(hotel['price'] * (1 - guest_data.loc[guest_id, 'discount']))
            })
            hotels_copy.at[hotel_id, 'rooms'] -= 1
            logging.info("Availability allocation: Guest %s assigned to hotel %s with most rooms", guest_id, hotel_id)
        else:
            logging.warning("Availability allocation: No available rooms for guest %s", guest_id)

    return allocation
