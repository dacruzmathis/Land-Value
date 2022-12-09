import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import plotly.graph_objects as go
import plotly.express as px
import time

def get_year(dt):
    return dt.year

def get_month(dt):
    return dt.month

def get_week(dt):
    return dt.week

def get_day(dt):
    return dt.day

def count_rows(rows):
    return len(rows)

def to_string(row):
    return str(row)

def get_quarter(day):
    return int(day / 7) + 1

def mean_value(rows):
    return rows['valeur_fonciere'].mean()

def select_full_path(datasets):
    full_path = ''
    if '2020' in datasets:
        full_path = 'csv/2020.csv'
    elif '2019' in datasets:
        full_path = 'csv/sample_2019.csv'
    elif '2018' in datasets:
        full_path = 'csv/sample_2018.csv'
    elif '2017' in datasets:
        full_path = 'csv/sample_2017.csv'
    elif '2016' in datasets:
        full_path = 'csv/sample_2016.csv'
    return full_path

def select_category(category):
    if 'Sale Repartition' in category:
        sale_repartition()
    elif 'Sale Type' in category:  
        sale_type()       
    elif 'Sale Location' in category: 
        sale_location()
    elif 'Sale Frequency' in category: 
        sale_frequency()
    elif 'Average Sale' in category:
        average_sale()
    elif 'Research' in category:
        research()

def get_slider(liste):
    switch = {}
    for i, v in enumerate(liste):
        switch[i+1] = v
    diapo = st.slider("Slider", min_value=1, max_value=len(liste))
    param = switch.get(diapo,"Invalid input")
    return param

def unique_map():
    fig = plt.figure(figsize=(15, 15))
    plt.title('France Land Sold')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.scatter(df_sample_resize['longitude'],df_sample_resize['latitude'],s=0.8, color="b" ,alpha=0.5) 
    plt.xlim(-5, 10)
    plt.ylim(41.2, 51.2)
    st.pyplot(fig)

def unique_histo(df_sample_resize):
    fig, axs = plt.subplots(figsize = (5,5))
    axs = df_sample_resize["nombre_pieces_principales"].plot.hist(bins = 10, rwidth = 0.8, range = (0,10))
    plt.title("Frequency by Months of 2020")
    plt.xlabel('Months of the year')
    plt.xticks(range(0,10))
    st.pyplot(fig)

def unique_histo2(by_days):
    fig, axs = plt.subplots(figsize = (5,5))
    plt.bar(range(0, 31), by_days.sort_values())
    plt.xticks(range(0, 31), by_days.sort_values().index)
    plt.xlabel('Day of the Month')
    plt.ylabel('Frequency')
    plt.title('Day of the Month Sorted by Sale Frequency')
    st.pyplot(fig)

def unique_histo3(by_days):
    fig, axs = plt.subplots(figsize = (5,5))
    plt.title('Sale Frequency by Day of the Month')
    plt.xlabel('Day of the Month')
    plt.ylabel('Frequency')
    plt.plot(by_days)
    st.pyplot(fig)

def my_map_streamlit(df_sample_resize):
    st.subheader('Sales Locations')
    new_df = df_sample_resize[['longitude', 'latitude']]
    st.map(new_df.dropna())

def my_line_chart_streamlit(x, title):
    st.subheader(title)
    st.line_chart(x)

def my_pie_chart_plotly(values, labels, title):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text=title)
    st.plotly_chart(fig)

def my_histo_plotly(df, bins, title, xlabel):
    fig = px.histogram(df, x=xlabel)
    fig.update_layout(bargap=0.2)
    fig.update_layout(title = title)
    st.plotly_chart(fig)

def my_plotly_city_map(df_cities):
    fig = px.scatter_mapbox(df_cities, lat="latitude", lon="longitude", hover_name="nom_commune", hover_data=['valeur_fonciere', 'type_local', 'nombre_pieces_principales', 'surface_reelle_bati'], color_discrete_sequence=["fuchsia"], zoom=10, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)  

def my_plotly_map():
    df_cities = df_sample_resize.groupby("nom_commune").mean()
    df_cities["text"] = df_cities.index + ', ' + df_cities['valeur_fonciere'].apply(to_string)
    fig = go.Figure(data=go.Scattergeo(lon = df_cities['longitude'], lat = df_cities['latitude'], text = df_cities["text"], mode = 'markers'))
    fig.update_layout(title = 'Cities with at least one sell last year in France', geo_scope = 'europe')
    st.plotly_chart(fig)

def my_map(title, c, vmin, vmax):
    fig = plt.figure(figsize=(15, 15))
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.scatter(df_sample_resize['longitude'],df_sample_resize['latitude'],s=0.8, c=c, vmin=vmin, vmax=vmax) 
    plt.xlim(-5, 10)
    plt.ylim(41.2, 51.2)
    st.pyplot(fig)

def my_plot(x, y, color, xlabel, title):
    fig = plt.figure(figsize=(15,10))
    plt.plot(x, y, color = color)
    plt.xlabel(xlabel)
    plt.ylabel("Average price")
    plt.title(title)
    st.pyplot(fig)

def my_histo_frequency_sale(title, df):
    fig= plt.figure(figsize=(15,10))
    sns.heatmap(df, linewidths = .5)
    plt.title(title)
    st.pyplot(fig)

def my_heatmap(title, x, vmin, vmax):
    fig = plt.figure(figsize=(15,10))
    sns.heatmap(x, linewidths = .5, vmin=vmin, vmax=vmax)
    plt.title(title)
    st.pyplot(fig)

def my_histo_type(x, color, xlabel, ylabel, title):
    fig = plt.figure(figsize=(15,10))
    plt.hist(x, bins = 100, range = (0, 300), color = color,alpha = 0.5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    st.pyplot(fig)

@st.cache(allow_output_mutation=True)
def load_sale_repartition_data():
    type_local = df_sample_resize.groupby('type_local').size()
    labels_type_local = ['Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé', 'Maison']
    values_type_local = [100781, 74293, 21663, 131957]    
    title_type_local = 'Type Local Repartition by Sale'
    nature_mutation = df_sample_resize.groupby('nature_mutation').size()
    labels_nature_mutation = ['Vente', "Vente en l'état futur d'achèvement", 'Autres']
    values_nature_mutation = [561439, 45092, 7490]
    title_nature_mutation = 'Nature Mutation Repartition by Sale'
    return (type_local, labels_type_local, values_type_local, title_type_local, nature_mutation, labels_nature_mutation, values_nature_mutation, title_nature_mutation)

@st.cache(allow_output_mutation=True)
def load_type_frequency_data():
    by_days = df_sample_resize.groupby('day').apply(count_rows)
    return by_days

@st.cache(allow_output_mutation=True)
def load_sale_location_data():
    df_sample_resize['prix_metre_carrez_surface_reelle_bati'] = df_sample_resize['valeur_fonciere'] / df_sample_resize['surface_reelle_bati']
    df_sample_resize['prix_metre_carrez_surface_terrain'] = df_sample_resize['valeur_fonciere'] / df_sample_resize['surface_terrain']
    return df_sample_resize

@st.cache(allow_output_mutation=True)
def load_sale_frequency_data():
    df_by_month_and_day = df_sample_resize.groupby(['month', 'day']).apply(count_rows).unstack()
    df_by_month_and_week = df_sample_resize.groupby(['month', 'week']).apply(count_rows).unstack()
    df_sample_resize['quarter']= df_sample_resize['day'].map(get_quarter)
    df_by_month_and_quarter = df_sample_resize.groupby(['month', 'quarter']).apply(count_rows).unstack()
    return (df_by_month_and_day, df_by_month_and_week, df_sample_resize, df_by_month_and_quarter)

@st.cache(allow_output_mutation=True)
def load_average_sale_data():
    nature_culture = df_sample_resize.groupby('nature_culture').size()
    average_sell_by_month = df_sample_resize.groupby(['month']).mean()
    average_sell_by_day1 = df_sample_resize.groupby(['day']).mean()            
    average_sell_by_day2 = df_sample_resize.groupby(['month', 'day']).apply(mean_value).unstack()
    average_sell_by_week = df_sample_resize.groupby(['month', 'week']).apply(mean_value).unstack()
    number_lot_mask = df_sample_resize['nombre_lots'] < 11
    number_room_mask1 = df_sample_resize['nombre_pieces_principales'] < 11
    number_room_mask2 = df_sample_resize['nombre_pieces_principales'] > 0
    number_room_mask = number_room_mask1 & number_room_mask2
    average_sell_by_rooms1 = df_sample_resize[number_lot_mask][number_room_mask].groupby(['nombre_pieces_principales', 'nombre_lots']).apply(mean_value).unstack()
    average_sell_by_rooms2 = df_sample_resize[number_room_mask].groupby(['nombre_pieces_principales', 'type_local']).apply(mean_value).unstack()
    average_sell_by_culture = df_sample_resize.groupby(['nature_culture', 'type_local']).apply(mean_value).unstack()
    return (nature_culture, average_sell_by_month, average_sell_by_day1, average_sell_by_day2, average_sell_by_week, number_lot_mask, number_room_mask, average_sell_by_rooms1, average_sell_by_rooms2, average_sell_by_culture)

@st.cache(allow_output_mutation=True)
def load_sale_research_data():
    return df_sample_resize

@st.cache(allow_output_mutation=True)
def load_main_data(full_path):   
    df_sample_resize = pd.read_csv(full_path)
    #df_sample = df.sample(frac =.25)
    #df_sample_resize = df_sample[['date_mutation','numero_disposition','nature_mutation','type_local','nombre_pieces_principales','nombre_lots',
    #'surface_reelle_bati','surface_terrain','nature_culture','valeur_fonciere','nom_commune','longitude','latitude']].copy()
    df_sample_resize["date_mutation"] = pd.to_datetime(df_sample_resize["date_mutation"])
    df_sample_resize['year'] = df_sample_resize['date_mutation'].map(get_year)
    df_sample_resize['month'] = df_sample_resize['date_mutation'].map(get_month)
    df_sample_resize['week'] = df_sample_resize['date_mutation'].map(get_week)
    df_sample_resize['day'] = df_sample_resize['date_mutation'].map(get_day)
    return df_sample_resize

def sale_repartition():
    (type_local, labels_type_local, values_type_local, title_type_local, nature_mutation, labels_nature_mutation, values_nature_mutation, title_nature_mutation) = load_sale_repartition_data()
    liste = []
    liste.append((values_type_local, labels_type_local, title_type_local))
    liste.append((values_nature_mutation, labels_nature_mutation, title_nature_mutation))          
    param = get_slider(liste)
    my_pie_chart_plotly(param[0], param[1], param[2])

def sale_type():
    by_days = load_type_frequency_data()
    liste = []
    liste.append((df_sample_resize['surface_reelle_bati'], 'b', 'Real Built Area', 'Frequency', 'Real Built Area Frequency'))
    liste.append((df_sample_resize['surface_terrain'], 'g', 'Land Surface', 'Frequency', 'Land Surface Frequency'))  
    liste.append(('', '', ''))   
    liste.append((df_sample_resize["month"], 12, 'Sale Frequency by Month', 'month'))
    liste.append((df_sample_resize["day"], 31, 'Sale Frequency by Day', 'day'))     
    liste.append(('', ''))
    liste.append((df_sample_resize['nombre_pieces_principales'], '', 'Sale Frequency by Number of Rooms', 'nombre_pieces_principales'))               
    param = get_slider(liste)
    if len(param) == 1:
        unique_histo(df_sample_resize)
    elif len(param) == 2:
        unique_histo2(by_days)
    elif len(param) == 3:
        unique_histo3(by_days)
    elif len(param) == 4:
        my_histo_plotly(param[0], param[1], param[2], param[3])
    else:
        my_histo_type(param[0], param[1], param[2], param[3], param[4])

def sale_location():
    df_sample_resize = load_sale_location_data()
    liste = []
    liste.append(('unique_map'))
    liste.append(('map', 'streamlit'))
    liste.append(('plotly', 'map', ''))
    liste.append(('France Land Sold by Room Numbers', df_sample_resize['nombre_pieces_principales'], 0, 5))
    liste.append(('France Land Sold by Land Value', df_sample_resize['valeur_fonciere'], 30_000, 300_000))     
    liste.append(('France Land Sold by m2 Real Built Area', df_sample_resize['prix_metre_carrez_surface_reelle_bati'], 100, 5_000))            
    liste.append(('France Land Sold by m2 Land Area', df_sample_resize['prix_metre_carrez_surface_terrain'], 100, 1_000))  
    param = get_slider(liste)
    if len(param) == 4:
        my_map(param[0], param[1], param[2], param[3])
    elif len(param) == 2:
        my_map_streamlit(df_sample_resize)
    elif len(param) == 3:
        my_plotly_map()
    else:
        unique_map()

def sale_frequency():
    (df_by_month_and_day, df_by_month_and_week, df_sample_resize, df_by_month_and_quarter) = load_sale_frequency_data()
    liste = []
    liste.append(('Sale Frequency by Day of the Year', df_by_month_and_day))
    liste.append(('Sale Frequency by Week of the Year', df_by_month_and_week))     
    liste.append(('Sale Frequency by Quarter of Month of the Year', df_by_month_and_quarter))       
    param = get_slider(liste)
    my_histo_frequency_sale(param[0], param[1])

def average_sale():
    (nature_culture, average_sell_by_month, average_sell_by_day1, average_sell_by_day2, average_sell_by_week, number_lot_mask, number_room_mask, average_sell_by_rooms1, average_sell_by_rooms2, average_sell_by_culture) = load_average_sale_data()
    liste = []
    liste.append((average_sell_by_month['valeur_fonciere'],'Average Sale by Month'))
    liste.append((average_sell_by_day1['valeur_fonciere'], 'Average Sale by Day of the Month'))     
    liste.append(('Average Sale by Day of the Year', average_sell_by_day2, 100_000, 500_000))
    liste.append(('Average Sale by Week of the Year', average_sell_by_week, 100_000, 1_000_000))       
    liste.append(('Average Sale by Number of Rooms', average_sell_by_rooms1, 50_000, 1_000_000))       
    liste.append(('Average Sale by Number of Rooms by Local Type', average_sell_by_rooms2, 10_000, 1_500_000))       
    liste.append(('Average Sale by Type of Culture by Local Type', average_sell_by_culture, 10_000, 1_000_000))              
    param = get_slider(liste)
    if len(param) == 4:
        my_heatmap(param[0], param[1], param[2], param[3])
    else:
        my_line_chart_streamlit(param[0], param[1])

def research():
    df_2020_sample_resize = load_sale_research_data()
    search = st.text_input('City')
    nom_commune_mask = df_2020_sample_resize['nom_commune'] == search
    if df_2020_sample_resize[nom_commune_mask].shape[0] != 0:
        local = st.radio("Local",('All', 'Maison', 'Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé'))
        local_mask = df_2020_sample_resize['type_local'] == local
        if df_2020_sample_resize[nom_commune_mask][local_mask].shape[0] != 0:
            rooms = st.number_input('Rooms')
            room_mask = df_2020_sample_resize['nombre_pieces_principales'] == rooms
            if df_2020_sample_resize[nom_commune_mask][local_mask][room_mask].shape[0] != 0:                   
                start_area, end_area = st.select_slider('Select a range of built area',options=[0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,250,300,400,500,600,700,800,900,1000,10_000], value=(0, 10_000))
                surface_reelle_bati_mask1 = df_2020_sample_resize['surface_reelle_bati'] >= start_area
                surface_reelle_bati_mask2 = df_2020_sample_resize['surface_reelle_bati'] <= end_area
                surface_reelle_bati_mask = surface_reelle_bati_mask1 & surface_reelle_bati_mask2
                if df_2020_sample_resize[nom_commune_mask][local_mask][room_mask][surface_reelle_bati_mask].shape[0] != 0:
                    st.write(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask][surface_reelle_bati_mask].head(10))
                    st.write('Average land value found : ', int(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask][surface_reelle_bati_mask]['valeur_fonciere'].mean()))
                    my_plotly_city_map(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask][surface_reelle_bati_mask])
                else:
                    st.write(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask].head(10))
                    st.write('Average land value found : ', int(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask]['valeur_fonciere'].mean()))
                    my_plotly_city_map(df_2020_sample_resize[nom_commune_mask][local_mask][room_mask]) 
            else:
                st.write(df_2020_sample_resize[nom_commune_mask][local_mask].head(10))
                st.write('Average land value found : ', int(df_2020_sample_resize[nom_commune_mask][local_mask]['valeur_fonciere'].mean()))
                my_plotly_city_map(df_2020_sample_resize[nom_commune_mask][local_mask]) 
        else:
            st.write(df_2020_sample_resize[nom_commune_mask].head(10))
            st.write('Average land value found : ', int(df_2020_sample_resize[nom_commune_mask]['valeur_fonciere'].mean()))
            my_plotly_city_map(df_2020_sample_resize[nom_commune_mask])

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' %\
                (method.__name__, (te - ts) * 1000))
        return result
    return timed

@timeit
def main():
    global df_sample_resize
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("# Dashboard - Land Value - France")

    datasets = st.selectbox('Dataset', ('Select', '2020', '2019', '2018', '2017', '2016'))
    full_path = select_full_path(datasets)

    if full_path != '':

        category = st.selectbox('Category', ('Select', 'Sale Repartition', 'Sale Type', 'Sale Location', 'Sale Frequency', 'Average Sale', 'Research'))
        df_sample_resize = load_main_data(full_path)
        select_category(category)

if __name__ == "__main__":
    main()