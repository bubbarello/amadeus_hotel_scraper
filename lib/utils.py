def list_hotel_ids_as_string(array):
    hotels_ids = [elem['hotelId'] for elem in array]
    hotel_ids_str = ",".join(hotels_ids)
    return hotel_ids_str