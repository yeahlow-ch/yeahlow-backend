from googleplaces import GooglePlaces, types, lang

google_places = GooglePlaces('AIzaSyAJmLYaSxaHM1PrVMgDG7j6iAscbYrsPp4')

class Places:

    place_types = [types.TYPE_MUSEUM, types.TYPE_ZOO, types.TYPE_STADIUM, types.TYPE_BAR, types.TYPE_NIGHT_CLUB]

    def get_nearest_place(self, lat, long):
        for place_type in self.place_types:
            result = self.send_request(lat, long, place_type)
            if len(result.places) != 0:
                return result.places[0].name.encode()

    def send_request(self, lat, long, type):
        query_result = google_places.nearby_search(
                lat_lng={'lat': float(lat), 'lng': float(long)}, 
                radius=100,
                type=type)
        return query_result
    