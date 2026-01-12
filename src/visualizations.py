import plotly.express as px


def create_map(df):
    lat_min = df['lat'].min()
    lat_max = df['lat'].max()
    lon_min = df['lon'].min()
    lon_max = df['lon'].max()
    
    
    # 2. Centro del poligono (media dei vertici)
    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2
    
    # 3. Dimensione del poligono (per calcolare zoom)
    lat_range = lat_max - lat_min
    lon_range = lon_max - lon_min
    max_range = max(lat_range, lon_range)
    
    # 4. Zoom inversamente proporzionale alla dimensione
    zoom = 11 - (max_range * 10)
    zoom = max(10, min(zoom, 15))
    
    fig = px.scatter_map(
        df,
        lat='lat',
        lon='lon',
        color='categories',
        size='rating',
        hover_name='name',
        hover_data=['rating', 'categories'],
        zoom=13,
        center={'lat': center_lat, 'lon': center_lon},
        size_max=13,
    )
    fig.update_layout(mapbox_style='open-street-map')

    return fig