import requests
from config import YELP_API_KEY


def get_restaurants(location, term="ristorante", limit_total=150):
    
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer ' + YELP_API_KEY}
    
    params = {
        'location': location,
        'term': term,
        'limit': 50
    }
    
    
    data_lista = []
    
    for offset in range(0,limit_total,50):
        params['offset'] = offset
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            for business in data["businesses"]:
                
                try:
                    ristorante = {
                        'name': business["name"],
                        'lat': business["coordinates"]["latitude"],
                        'lon': business["coordinates"]["longitude"],
                        'rating': business["rating"],
                        'categories': business["categories"][0]["title"],
                        'review_count': business.get("review_count", 0),
                        'address': business["location"]["display_address"][0] if business["location"].get("display_address") else 'N/A',
                        'phone':business.get("display_phone", "N/A"),
                        'url': business.get("url", "")
                    }
                    data_lista.append(ristorante)
                except (KeyError, IndexError):
                    continue
        else:
            print(f"Errore: {response.status_code}")
            print(response.text)
            
    return data_lista