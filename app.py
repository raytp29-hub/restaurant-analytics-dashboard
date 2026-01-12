import pandas as pd
import streamlit as st
import plotly.express as px
from src.api_client import get_restaurants
from src.data_processor import process_restaurant_data
from src.visualizations import create_map
from src.database import init_db, save_to_db, load_from_db
from src.ai_insight import generate_insights, generate_insights_data


st.set_page_config(page_title="Restaurant Analytics", layout="wide")



if 'df' not in st.session_state:
    st.session_state.df = None
    
    
    
if 'insights_text' not in st.session_state:
    st.session_state.insights_text = None
    
if 'insights_data' not in st.session_state:
    st.session_state.insights_data = None    
    
    

init_db()


# Title
st.title("Food & Restaunrant Mapping")


# Sidebar
st.sidebar.header("Impostazioni ricerca")
city = st.sidebar.text_input("Città", "Catania, Italy")
limit = st.sidebar.slider("Numero Ristoranti", 50, 300, 150, 50)





if st.sidebar.button("Cerca"):
    with st.spinner("Caricamento dati..."):
        
        cached_df = load_from_db(city)
        
        if not cached_df.empty:
            st.info(f"Load in cache")
            df = cached_df
            
        else:
            st.info("Download from yelp")
            data = get_restaurants(city, limit_total=limit)
            df = process_restaurant_data(data)
            save_to_db(df, city)
        
        st.session_state.df = df

if st.session_state.df is not None:
    df = st.session_state.df
        
        
            
    st.sidebar.subheader("Filters")
    
    categories_list = df["categories"].unique().tolist()
    categories_filter = st.sidebar.multiselect(
        "Categories",
        options=categories_list,
        default=[]
    )
    
    
    min_rating = st.sidebar.slider("Rating minimo", 1.0, 5.0, 1.0, 0.5)
    min_reviews = st.sidebar.number_input("Recensioni minime", 0, value=0)
    
    
    df_filtered = df[
        (df["rating"] >= min_rating) & 
        (df["review_count"] >= min_reviews)
    ]
    
    if categories_filter: 
        df_filtered = df_filtered[df_filtered["categories"].isin(categories_filter)]
    
            

        
    st.metric("Totale ristoranti trovati", len(df_filtered))
        
    fig = create_map(df_filtered)
    st.plotly_chart(fig, use_container_width=True)
        
        
        

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Totale ristoranti", len(df_filtered))
        
    with col2:
        st.metric("Rating medio", f"{df_filtered["rating"].mean():.1f}")
        
    with col3:
        st.metric("Categorie Ristorative", df_filtered["categories"].nunique())
        
    with col4:
        st.metric("Ristorante top rated", df_filtered.loc[df_filtered["rating"].idxmax(), 'name'])
        
        
        
    # Data charts
    
    category_counts = df_filtered["categories"].value_counts()
    
    fig_bar = px.bar(
        category_counts,
        x=category_counts.index,
        y=category_counts.values,
        labels={'x': 'Category', 'y': 'Number of Restaurant'},
        color=category_counts.index,
        title='Distribution of category'
    )
    fig_bar.update_layout(showlegend=False)
    
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    
    
    # Histogram rating
    df_filtered["rating_rounded"] = df_filtered['rating'].round()
    
    
    fig_histo = px.histogram(
        df_filtered,
        x='rating',
        title='Distribution of Rating',
        labels={'rating': 'Rating', 'count': 'Number of restaurant'},
        nbins=10,
        color='rating_rounded',
        barmode='group'
    )
    
    
    st.plotly_chart(fig_histo, use_container_width=True)
    
    st.divider()
    
    st.subheader("AI Business Insights")
    
    
    col1, col2 = st.columns(2)
    
    
    
    with col1:
        if st.button("Genera Analisi AI"):
            with st.spinner("l'AI sta analizzando i dati..."):
                st.session_state.insights_text = generate_insights(df_filtered)

            
            
    with col2:
        if st.button("📊 Genera Grafici AI"):
            with st.spinner("🤖 Elaborazione dati..."):
                st.session_state.insights_data = generate_insights_data(df_filtered)

# 3. MOSTRA SE ESISTONO (fuori dai button!)
if st.session_state.insights_text:
    st.markdown("### Report Testuale")
    st.markdown(st.session_state.insights_text)

if st.session_state.insights_data:
    st.markdown("### Analisi Visuale")
    
    data = st.session_state.insights_data
    
    # Grafico 1: Market Gaps
    if 'market_gaps' in data:
        gaps_df = pd.DataFrame(data['market_gaps'])
        fig_gaps = px.bar(
            gaps_df, 
            x='category', 
            y='opportunity_score',
            color='opportunity_score',
            title='Opportunità di Mercato',
            hover_data=['reason']
        )
        st.plotly_chart(fig_gaps, use_container_width=True)
    
    # Grafico 2: Strategic Priorities
    if 'strategic_priorities' in data:
        priorities_df = pd.DataFrame(data['strategic_priorities'])
        fig_priorities = px.bar(
            priorities_df,
            x='action',
            y='priority',
            color='roi_potential',
            title='Priorità Strategiche'
        )
        st.plotly_chart(fig_priorities, use_container_width=True)
    
    # Grafico 3: Risk Assessment
    if 'risk_assessment' in data:
        risks_df = pd.DataFrame(data['risk_assessment'])
        fig_risks = px.scatter(
            risks_df,
            x='probability',
            y='severity',
            size='severity',
            hover_name='risk',
            title='Mappa dei Rischi'
        )
        st.plotly_chart(fig_risks, use_container_width=True)