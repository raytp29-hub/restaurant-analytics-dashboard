import pandas as pd


def process_restaurant_data(data_lista):
    
    df = pd.DataFrame(data_lista)
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    
    return df