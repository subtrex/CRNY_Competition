import requests
import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim
import pydeck as pdk
from PIL import Image
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
from pydeck.types import String
from matplotlib_venn import venn2, venn3
import altair as alt
import plotly.graph_objects as go
#from chapter2 import chapter2

st.set_option('deprecation.showPyplotGlobalUse', False)

import plotly.io as pio
pio.templates.default = "plotly"

st.set_page_config(page_title="CRNY Data Visualization", page_icon=":1234:", layout="wide")

# Custom CSS for horizontal radio buttons
horizontal_radio_css = """
    div[data-baseweb="radio"] > label {
        display: inline-block;
        margin-right: 20px;
    }
"""

# Custom CSS for text justification
text_justification_css = """
    p {
        text-align: justify;
    }
"""

# Combined custom CSS
mystyle = f'''
    <style>
        {horizontal_radio_css}
        {text_justification_css}
    </style>
'''

st.markdown(mystyle, unsafe_allow_html=True)

with st.container():
    st.title("Bridging Gaps and Building Futures")
    st.markdown('<span style="font-size:20px; font-style: italic;"> The Role of CRNY Guaranteed Income Program in Supporting New Yorks Artists</span>', unsafe_allow_html=True)
    
image_ny_artists_1 = Image.open('./assets/nyc_artists_1.jpg')
#width=1750 use_column_width="auto"
st.image(image_ny_artists_1, width=None)

with st.container():
    st.write("\n")
    st.write("Embark on a journey through New York's artist community, uncovering the transformative impact of CRNY's Guaranteed Income (GI) Program. This data visualization dashboard peels back the layers, exploring the lives of artists, their challenges, and the unique role the GI program plays. From demographic breakdowns to pandemic struggles, each chapter unveils a different facet. Visualizations highlight how the GI program acts as a lifeline, offering financial stability and nurturing artistic resilience. Join us in envisioning a future where CRNY's GI program continues to bridge gaps, build futures, and uplift the heartbeat of New York's creative spirit.")
    st.write("---")

with st.container():
    st.subheader("Where's the Data Coming From?")
    st.write("The dataset draws information from two primary sources. The first set of data originates from the applications submitted by individuals aspiring to enroll in the CRNY Guaranteed Income (GI) for Artists program. This comprehensive dataset encompasses details from all applicants, irrespective of their final acceptance into the program. The second data source is derived from the Portrait of Artists survey administered by CRNY. This survey aims to comprehend the needs, circumstances, and experiences of artists in New York. These combined datasets provide a rich pool of information to explore and analyze.")
    # Graph Nodes
    nodes = []
    edges = []
    nodes.append( Node(id="DA", 
                   label="Dataset", 
                   size=25, 
                   shape="circularImage",
                   image="data:image/jpeg;base64,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") 
            ) # includes **kwargs
    nodes.append( Node(id="GI", 
                   label="Guaranteed Income Application",    
                   size=25,
                   shape="circularImage",
                   image="https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png") 
            )
    nodes.append( Node(id="PA", 
                   label="Portrait of Artists Survey",    
                   size=25,
                   shape="circularImage",
                   image="data:image/png;base64,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") 
            )
    edges.append( Edge(source="DA", 
                   label="sourced_from", 
                   target="GI", 
                   # **kwargs
                   ) 
            )
    edges.append( Edge(source="DA", 
                   label="sourced_from", 
                   target="PA", 
                   # **kwargs
                   ) 
            )  

    config = Config(width=None,
                height=300,
                directed=True, 
                physics=False, 
                hierarchical=False,
                nodeHighlightBehavior=True, 
                highlightColor="#F7A7A6",
                collapsible=True,
                # **kwargs
                )

    return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

    st.write("---")

    st.markdown('<span style="font-size:40px; font-style: italic;"> Let\'s begin our journey</span>', unsafe_allow_html=True)
    image_ny_artists_2 = Image.open('./assets/nyc_artists_2.jpg')
    st.image(image_ny_artists_2, width=None)

with st.container():
    st.write("\n")
    st.title("Chapter 1: The Artists of New York - Who Are They?")
    st.markdown('<span style="font-size:18px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Let\'s dive a bit deeper into the demographics of our artists. </span>', unsafe_allow_html=True)


# Dataframe reading and pre-processing
download_link = 'https://drive.google.com/file/d/1_0bQfQQLhOGLLUQqBbx9NkyO-ihLSSuz/view?usp=drive_link'
df = pd.read_csv('gi_and_poa_survey_data.csv')

# Ethnicity
ethnicity_data = df['p38_race1']
ethnicity_counts_df = ethnicity_data.value_counts()
ethnicity_categories = ethnicity_counts_df.index.tolist()
ethnicity_counts = ethnicity_counts_df.values.tolist()

ethnicity_data_list = {
    'Ethnicity': ["White", "Black/African-American","Hispanic/Latin-American", "Asian", "No answer", "Other", "Arab or Middle Eastern", "Indigenous American", "Pacific Islander"],
    'Count': ethnicity_counts
}

# Gender
gender_data = df['p41_gender1']
gender_counts_df = gender_data.value_counts()
gender_labels = gender_counts_df.index.tolist()
gender_counts = gender_counts_df.values.tolist()

gender_data_list = {
    'Gender': ["Woman", "Man", "Non-binary", "No answer", "Other", "Twospirit"],
    'Count': gender_counts
}

# Community
community_data = df['p36_community']
community_counts_df = community_data.value_counts()
community_labels = community_counts_df.index.tolist()
community_counts = community_counts_df.values.tolist()

community_data_list = {
    'Community': community_labels,
    'Count': community_counts
}


# Age Range
age_range_data = df['p_agerange']
age_range_counts_df = age_range_data.value_counts()
age_range_labels = age_range_counts_df.index.tolist()
age_range_counts = age_range_counts_df.values.tolist()

age_range_data_list = {
    'Age Range': age_range_labels,
    'Count': age_range_counts
}


# LGBTQIAP
lgbtqiap_data = df['p43_lgbtqiap']
lgbtqiap_counts_df = lgbtqiap_data.value_counts()
lgbtqiap_labels = lgbtqiap_counts_df.index.tolist()
lgbtqiap_counts = lgbtqiap_counts_df.values.tolist()

lgbtqiap_data_list = {
    'LGBTQIAP': lgbtqiap_labels,
    'Count': lgbtqiap_counts
}


# Language
language_data = df['p40_language']
language_counts_df = language_data.value_counts()
language_labels = language_counts_df.index.tolist()
language_counts = language_counts_df.values.tolist()

language_data_list = {
    'Language': language_labels,
    'Count': language_counts
}

language_data_list['Language'][2] = "Other"
language_data_list['Language'][11] = "No answer"
language_data_list['Count'][2] = 377

del language_data_list['Language'][12]
del language_data_list['Count'][12]

language_df = pd.DataFrame(language_data_list)

fig_6 = px.bar(language_df, x='Language', y='Count', text='Count', color_discrete_sequence=["Magenta"])
fig_6.update_layout(width=500, height=500, yaxis_type='log', legend=dict(font=dict(size=10)))
fig_6.update_xaxes(title_text='', showticklabels=True)

with st.container():

    col_1, col_2 = st.columns([1, 1], gap="large")

    # Ethnicity
    with col_1:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Ethnicity </span>', unsafe_allow_html=True)
        ethnicity_image = Image.open('./assets/ethnicity.jpg')
        st.image(ethnicity_image, width=None)
        st.write("New York's ethnic fabric is diverse, with Whites leading at 31%, showcasing a substantial demographic presence. Close behind, African Americans at 29.4% and Hispanics at 15.9% contribute significantly to the community's diversity. Representations from Indigenous American and Pacific Islander communities are smaller but integral. This snapshot reflects the intricate and varied mosaic of ethnicities, emphasizing the richness of New York's cultural landscape.")
        fig_1 = px.pie(ethnicity_data_list, names='Ethnicity', values='Count', hole=.4)
        fig_1.update_layout(width=None, height=500, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_1,use_container_width = True)
    
    # Age Range
    with col_2:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Age Range </span>', unsafe_allow_html=True)
        age_range_image = Image.open('./assets/age_range.jpg')
        st.image(age_range_image, width=None)
        st.write("In New York's demographic tapestry, age diversity is apparent. The 25-34 age range dominates at 43.1%, indicating a substantial community presence. Following closely, the 35-44 age group represents 22%, and the 18-24 age range, at 12.8%, denotes a youthful presence. This concise overview captures the varied age distribution, highlighting the significance of the 25-34 age range in shaping the art community's demographic landscape.")
        fig_4 = px.pie(age_range_data_list, names='Age Range', values='Count', hole=.4)
        fig_4.update_layout(width=None, height=500, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_4,use_container_width = True)


with st.container():

    col_1, col_2= st.columns([1, 1], gap="large")

    # Gender
    with col_1:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Gender </span>', unsafe_allow_html=True)
        gender_image = Image.open('./assets/gender.jpg')
        st.image(gender_image, width=None)
        st.write("Gender diversity in New York's art community is evident, with men representing 41.4%, women at 42.1%, and non-binary individuals making up 11.6%. These statistics underscore a balanced distribution, reflecting an inclusive and varied representation across gender identities. The nearly equal percentages between men and women indicate a harmonious gender presence, while the acknowledgment of non-binary individuals emphasizes a commitment to embracing diverse gender expressions within the vibrant New York art scene.")
        fig_2 = px.pie(gender_data_list, names='Gender', values='Count', hole=.4)
        fig_2.update_layout(width=None, height=500, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_2, use_container_width=True)

    # LGBTQIAP
    with col_2:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> LGBTQIAP+ </span>', unsafe_allow_html=True)
        lgbt_image = Image.open('./assets/LGBTQIAP.jpg')
        st.image(lgbt_image, width=None)
        st.write("In the New York art community, LGBTQIAP+ representation is diverse. About 43.7% openly identify, showing a vibrant presence. On the other hand, 47.8% choose not to, reflecting various viewpoints. Some, around 8.49%, prefer not to share, respecting their privacy. This mix highlights the different experiences within the community, creating an inclusive space that respects various perspectives, fostering an inclusive environment that values diverse perspectives on LGBTQIAP+ identity.")
        fig_5 = px.pie(lgbtqiap_data_list, names='LGBTQIAP', values='Count', hole=.4)
        fig_5.update_layout(width=500, height=500, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_5, use_container_width=True)
    
with st.container():

    col_1, col_2 = st.columns([1, 1], gap="large")

    # Language
    with col_1:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Language </span>', unsafe_allow_html=True)
        lang_image = Image.open('./assets/language.jpg')
        st.image(lang_image, width=None)
        st.write("New York artists embrace linguistic diversity, with English as the predominant language spoken by 11,552 individuals. Spanish follows with 569 speakers, contributing to the multicultural fabric. Additionally, Mandarin boasts 185 speakers, and 377 artists communicate in other languages. This linguistic panorama underscores the rich tapestry of cultural backgrounds, fostering a vibrant and inclusive environment within the artistic community. Some other spoken languages include Russian, Korean, Italian, Polish, Haitian, Arabic, and Bengali.")
        st.plotly_chart(fig_6, use_container_width=True)

    # Community
    with col_2:
        st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Community </span>', unsafe_allow_html=True)
        comm_image = Image.open('./assets/community.jpg')
        st.image(comm_image, width=None)
        st.write("The majority of New York artists, approximately 81.1%, call urban areas home, illustrating the state's overall development. About 11.2% prefer suburban surroundings, offering a mix of urban and residential features. A smaller, yet notable, fraction of 7.16% originates from rural settings. These statistics unveil the diverse geographic backgrounds of artists, emphasizing the prevalent influence of urban development in shaping the cultural tapestry. This varied residential landscape reflects the dynamic choices artists make, contributing to the rich artistic fabric of New York.")
        fig_3 = px.pie(community_data_list, names='Community', values='Count', hole=.4)
        fig_3.update_layout(width=500, height=500, legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_3, use_container_width=True)

with st.container():

    st.markdown('<span style="font-size:18px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> What kind of disciplines do our artists practise? </span>', unsafe_allow_html=True)

    col_1, col_2 = st.columns([1, 1], gap="large")

    with col_1:
        st.write("New York's vibrant artistic community is a dynamic tapestry of creativity, with visual arts taking the lead at 5302 practitioners, a testament to the city's thriving visual culture. The resonant chords of music echo closely behind, with 4228 artists practising music. 2863 artists are in the Film discipline, entailing storytelling, cinematics, and filmmaking. Meanwhile, the impactful world of media arts finds expression through 2566 dedicated creators. These diverse disciplines collectively shape the city's cultural landscape, reflecting a kaleidoscope of talents. From the visual richness of photography and videography to the rhythmic landscapes of music and the narrative power of film and media arts, New York artists navigate and contribute to an artistic realm that celebrates diversity and innovation.")

    with col_2:
        # what type of art

        dis_labels = ['Craft', 'Dance', 'Design', 'Film', 'Literary Arts', 'Media Arts', 'Music', 'Theater', 'Visual Arts', 'Interdisciplinary Arts']
        dis_counts = [2014, 1206, 2256, 2863, 2084, 2566, 4228, 2179, 5302, 2253]
        dis_chart_data = pd.DataFrame({'Disciplines': dis_labels, 'Counts': dis_counts})
        
        dis_chart = alt.Chart(dis_chart_data).mark_bar().encode(
                x='Disciplines',
                y='Counts',
                tooltip=['Disciplines', 'Counts']
        )

        st.altair_chart(dis_chart, use_container_width=True)
    
# Location

with st.container():
    st.write("\n")
    st.markdown('<span style="font-size:18px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Let\'s see where our artists are from. </span>', unsafe_allow_html=True)
    county_ny_image = Image.open('./assets/county_ny.jpg')
    st.image(county_ny_image, width=None)
    st.write("Kings County, harboring major cities like Brooklyn, takes the lead with 4434 artists, a vibrant hub in the competition's dataset. Following closely, New York County with New York City contribute 2837 artists, marking a significant artistic presence. Queens County secures the third spot with 1618 artists. Impressively, 62 New York state counties are represented, showcasing diverse geographic origins. Notably, Schuyler County, Genesee County, Wayne County, and Madison County, primarily suburban and rural, have the least artist representation. The below scatterplot, followed by a deck chart and heatmap, vividly depict the nuanced population distribution of artists across the New York State Counties.")

# County
county_data = df['p34_county']
county_counts_df = county_data.value_counts()

county_counts_df.index = county_counts_df.index.str.split(' County').str[0]
county_counts_df = county_counts_df.sort_index()
#st.write(county_counts_df.sort_values(ascending=False))
county_counts_df = county_counts_df.groupby(county_counts_df.index).sum()

county_labels = county_counts_df.index.tolist()
county_counts = county_counts_df.values.tolist()

county_locator = Nominatim(user_agent="county_locator")

def get_coordinates(county_name):
    location = county_locator.geocode(county_name + ', New York, USA')
    if location:
        return location.latitude, location.longitude
    else:
        return None

county_lats = [42.6511674, 42.2446061, 40.8466508, 42.1455623, 42.2234823, 42.8093409, 42.2894671, 42.1384667, 42.4784565, 44.7278943, 42.2415027, 42.5842136, 42.194917, 41.7194303, 42.352098, 44.0638879, 44.5599139, 43.1061507, 43.0102726, 42.2628769, 43.6307863, 43.4911326, 44.059311, 43.1509069, 43.7344277, 42.7360902, 42.875882, 41.3304767, 42.8941269, 40.7352994, 40.7127281, 43.2042439, 43.2144051, 43.015598, 42.8580624, 41.3873306, 43.2244513, 43.4112973, 42.5984272, 41.426996, 40.7135078, 42.7091389, 42.7905911, 41.1519319, 43.0833231, 42.8142432, 42.5757217, 42.3903231, 42.7831619, 44.4973591, 42.2359045, 40.8832318, 41.7156311, 42.1333395, 42.118333, 41.8689317, 43.5018687, 43.2294536, 43.1500557, 41.1763139, 42.7039813, 42.6444444]
county_longs = [-73.754968, -78.0419281, -73.8785937, -75.8404114, -78.6477096, -76.5700777, -79.421728, -76.7725493, -75.6130279, -73.6686982, -73.6723456, -76.0704906, -75.0016302, -73.7516205, -79.322965, -73.7542043, -74.3273735, -74.4461771, -78.1780196, -74.0878112, -74.4659275, -74.9481252, -75.9995742, -73.8542895, -75.440289, -77.7781416, -75.6802581, -74.1866348, -74.4099745, -73.5615778, -74.0060152, -78.7676017, -75.4039155, -76.2257127, -77.295025, -74.2507287, -78.2272835, -76.1279841, -75.0142701, -73.760156, -73.8283132, -73.5107732, -77.5319396, -74.0357266, -73.8712155, -73.9395687, -74.4390277, -76.8691575, -76.8386051, -75.0657043, -77.3750862, -72.8578027, -74.7804323, -76.3309339, -75.249444, -74.2618518, -73.8164637, -73.4471343, -77.0377603, -73.7907554, -78.2415228, -77.112177]

min_count = min(county_counts)
max_count = max(county_counts)
normalized_counts = [(count - min_count) / (max_count - min_count) for count in county_counts]

county_map_df = pd.DataFrame({
    'County': county_labels,
    'latitude': county_lats,
    'longitude': county_longs,
    'Count': county_counts
})

# Create DataFrame
chart_data = pd.DataFrame({
    'county': county_labels,
    'lat': county_lats,
    'lon': county_longs,
    'count': county_counts
})

chart_data['log'] = np.log(chart_data['count'])

# Scatterplot proper

st.pydeck_chart(pdk.Deck(
            map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=41.730610,
            longitude=-76,
            zoom=6,
            pitch=40,
        ),
        layers=[
            pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            opacity=0.2,
            stroked=True,
            filled=True,
            radius_scale=3000,
            line_width_min_pixels=1,
            get_position='[lon, lat]',
            get_radius='log',
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
           
                  ),
               ],
            ))
         
with st.container():
    col_1, col_2= st.columns([1, 1], gap="small")

    with col_1:
            #PyDeck with rising bars

            st.pydeck_chart(pdk.Deck(
                map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=41.730610,
                longitude=-76,
                zoom=5,
                    pitch=50,
            ),
            layers=[
                pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                opacity=0.1,
                get_position='[lon, lat]',
                radius=2000,
                get_elevation_weight = 'log',
                elevation_scale=200,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=chart_data,
                    get_position='[lon, lat]',
                    get_color='[255, 140, 0, 160]',
                    get_radius = 3000,
                ),
            ],
        ))
            
    with col_2:
                # heatmap

                st.pydeck_chart(pdk.Deck(
                        map_style=None,
                        initial_view_state=pdk.ViewState(
                        latitude=41.730610,
                        longitude=-76,
                        zoom=5,
                        pitch=50,
                    ),
                    layers=[
                    pdk.Layer(
                        'HeatmapLayer',
                        data=chart_data,
                        opacity=1,
                        get_position='[lon, lat]',
                        threshold=0.9,
                        aggregation=String('MEAN'),
                        get_weight = 'log',
                    ),
                ],
            ))
                
st.write("------")

with st.container():
    st.title("Chapter 2: The Challenges They Face")
    prob_image = Image.open('./assets/artist_problem.jpg')
    st.image(prob_image, width=None)
    st.write("\n")
    
    #Chapter 2: 

    # --------------------------------------------------------------energy expended------------------------------------------------------------------ 
    


    
    amount_of_energy_df = df['p5_amountofenergy']

    amount_of_energy_df = amount_of_energy_df.dropna()
    energy_frequency = amount_of_energy_df.value_counts()
    energy_frequency_df =energy_frequency.reset_index()


    legend_details = energy_frequency_df['p5_amountofenergy'].values
    hover_data = energy_frequency_df['count'].values

    # Given sizes of the bubbles (radius) and the data to show on hover
    bubble_sizes = [150, 110, 90, 70, 55]  # Radii provided by you
    bubble_colors = ['#fff5eb', '#fee6ce', '#fdd0a2', '#fdae6b', '#fd8d3c']
    bubble_colors = bubble_colors[::-1]
    # Create a figure
    fig_energy = go.Figure()

    # The largest bubble's bottom will serve as the reference for 'y' positions of other bubbles
    reference_bottom = -max(bubble_sizes) / 2

    # Add bubbles to the figure, with the bottom of the largest bubble at y=0
    for size, data, legend,colors in zip(bubble_sizes, hover_data, legend_details, bubble_colors):
        fig_energy.add_trace(go.Scatter(
            x=[0],  # Centered on x=0
            y=[reference_bottom + size / 2],  # Adjust y to make bubbles concentric from the bottom
            marker=dict(
                size=[size * 2],  # Multiply by 2 to get diameter
                sizemode='diameter',
                color = colors
            ),
            mode='markers',
            hoverinfo='text',
            text=[f'{data} people expended {legend} '],  # Text to show on hover
            name=f'Energy {legend}',  # Legend entry
        ))

    # Update the layout
    fig_energy.update_layout(
        template='plotly_white',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-max(bubble_sizes), max(bubble_sizes)]  # Set x-axis range to fit the largest bubble
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor="x",
            scaleratio=1,
            range=[reference_bottom * 2, max(bubble_sizes)]  # Set y-axis range to fit the stack
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Hide axis lines
    fig_energy.update_xaxes(visible=False)
    fig_energy.update_yaxes(visible=False)

    # Use Streamlit to display the figure
    # st.plotly_chart(fig)

    with st.container():
        col_1,col_2 = st.columns([1,1], gap= "large")

        with col_1:
           st.plotly_chart(fig_energy, use_container_width=True)

        with col_2:
            st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Energy Pulse of Artists </span>', unsafe_allow_html=True)
            # ethnicity_image = Image.open('./assets/age_range.jpg')
            # st.image(ethnicity_image, width=545)
            st.write("Assessing energy levels among New York artists, the data provides a comprehensive view of the artists' capacity for engaging in their practices. There were 221 artists (2.83%) who reported having no energy, indicating severe barriers to artistic activity. A significant number, 1,685 artists (21.61%), experienced very low energy, highlighting considerable challenges in their creative endeavors. A smaller group, comprising 578 artists (7.41%), had fluctuating energy levels, potentially leading to inconsistent artistic engagement. Positively, 2,654 artists (34.04%) felt they had sufficient energy, suggesting a stable ability to pursue their art. Lastly, the survey revealed that 2,658 artists (34.09%) had more than enough energy, indicating a strong capacity for sustained artistic involvement. These figures underscore the varied energy levels within the artist community, from significant challenges to robust engagement.")
            

    # --------------------------------------------------------------energy expended------------------------------------------------------------------


     # --------------------------------------------------------------time expended------------------------------------------------------------------
    amount_of_time_df = df['p6_amountoftime']

    amount_of_time_df = amount_of_time_df.dropna()
    time_frequency = amount_of_time_df.value_counts()
    time_frequency_df =time_frequency.reset_index()

    legend_details = time_frequency_df['p6_amountoftime'].values  
    hover_data = time_frequency_df['count'].values

    # Given sizes of the bubbles (radius) and the data to show on hover
    bubble_sizes = [150, 110, 90, 70, 55]  # Radii provided by you
    bubble_colors = ['#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4']
    bubble_colors = bubble_colors[::-1]
    # Create a figure
    fig_time = go.Figure()

    # The largest bubble's bottom will serve as the reference for 'y' positions of other bubbles
    reference_bottom = -max(bubble_sizes) / 2

    # Add bubbles to the figure, with the bottom of the largest bubble at y=0
    for size, data, legend,color in zip(bubble_sizes, hover_data, legend_details, bubble_colors):
        fig_time.add_trace(go.Scatter(
            x=[0],  # Centered on x=0
            y=[reference_bottom + size / 2],  # Adjust y to make bubbles concentric from the bottom
            marker=dict(
                size=[size * 2],  # Multiply by 2 to get diameter
                sizemode='diameter',
                color = color
            ),
            mode='markers',
            hoverinfo='text',
            text=[f'{data} people spent {legend}'],  # Text to show on hover
            name=f'time {legend}',  # Legend entry
        ))

    # Update the layout
    fig_time.update_layout(
        template='plotly_white',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-max(bubble_sizes), max(bubble_sizes)]  # Set x-axis range to fit the largest bubble
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor="x",
            scaleratio=1,
            range=[reference_bottom * 2, max(bubble_sizes)]  # Set y-axis range to fit the stack
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Hide axis lines
    fig_time.update_xaxes(visible=False)
    fig_time.update_yaxes(visible=False)

    # Use Streamlit to display the figure
    # st.plotly_chart(fig)
    with st.container():
        col_1,col_2 = st.columns([1,1], gap= "large")

        with col_1:
            st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Artists\' Financial Spectrum </span>', unsafe_allow_html=True)
            # ethnicity_image = Image.open('./assets/age_range.jpg')
            # st.image(ethnicity_image, width=545)
            st.write("The CRNY survey on New York artists reveals a diverse landscape of time availability for artistic and cultural practices. When the responses are broken down, 206 artists (1.5%) report having no time at all, highlighting a critical barrier in their pursuit of creative work. A significant portion, representing 2,250 individuals (16.4%), faces the challenge of very little time, underscoring a common struggle among artists to balance their craft with other demands. The largest group, with 5,387 respondents (39.2%), experiences fluctuating time availability, indicating a level of unpredictability in their ability to consistently engage in their art. On a more positive note, 3,304 artists (24.0%) have sufficient time, suggesting a stable opportunity for artistic endeavors. Remarkably, 2,603 respondents (18.9%) enjoy more than enough time, placing them in an advantageous position to fully embrace their artistic pursuits. This spectrum of time availability, from severe constraints to ample freedom, paints a vivid picture of the varying conditions under which New York's artists operate.")
            
        with col_2:
            
            st.plotly_chart(fig_time, use_container_width=True)


 # --------------------------------------------------------------time expended------------------------------------------------------------------




st.write("------")

with st.container():
    st.title("Chapter 3: The Pandemics Toll")
    st.write("\n")
    pandemic_image = Image.open('./assets/pandemic.jpg')
    st.image(pandemic_image, width=None)
    st.write("\n")
    st.write("\n")

# employment impact

def merge_columns(row):
    return [value for value in row if value is not None]

emp_impact_data = df[['p30_employimpact1', 'p30_employimpact2', 'p30_employimpact3', 'p30_employimpact4', 'p30_employimpact5', 'p30_employimpact6', 'p30_employimpact7', 'p30_employimpact8']]
columns_to_merge = ['p30_employimpact1', 'p30_employimpact2', 'p30_employimpact3', 'p30_employimpact4', 'p30_employimpact5', 'p30_employimpact6', 'p30_employimpact7', 'p30_employimpact8']
emp_impact_data['merged'] = emp_impact_data[columns_to_merge].apply(merge_columns, axis=1)

def contains_value(lst, value):
    return int(value in lst)

def get_data_venn_1(impacts):
    ans = []
    if ('furloughed' in impacts):
        ans.append(1)
    if ('freelanceworkcanceled' in impacts):
        ans.append(2)
    if ('industryshutdown' in impacts):
        ans.append(3)
    if ('furloughed' in impacts and 'freelanceworkcanceled' in impacts):
        ans.append(4)
    if ('furloughed' in impacts and 'industryshutdown' in impacts):
        ans.append(5)
    if ('freelanceworkcanceled' in impacts and 'industryshutdown' in impacts):
        ans.append(6)
    if ('furloughed' in impacts and 'freelanceworkcanceled' in impacts and 'industryshutdown' in impacts):
        ans.append(7)
    return ans

def get_data_venn_2(impacts):
    ans = []
    if ('laidofforfired' in impacts):
        ans.append(1)
    if ('freelanceworkcanceled' in impacts):
        ans.append(2)
    if ('industryshutdown' in impacts):
        ans.append(3)
    if ('laidofforfired' in impacts and 'freelanceworkcanceled' in impacts):
        ans.append(4)
    if ('laidofforfired' in impacts and 'industryshutdown' in impacts):
        ans.append(5)
    if ('freelanceworkcanceled' in impacts and 'industryshutdown' in impacts):
        ans.append(6)
    if ('laidofforfired' in impacts and 'freelanceworkcanceled' in impacts and 'industryshutdown' in impacts):
        ans.append(7)
    return ans

emp_impact_data['venn_1_data'] = emp_impact_data['merged'].apply(get_data_venn_1)
emp_impact_data['venn_2_data'] = emp_impact_data['merged'].apply(get_data_venn_2)

total_rows = len(emp_impact_data)

values_to_check = [1, 2, 3, 4, 5, 6, 7]

venn1_data = []
for value in values_to_check:
    column_name = f'contains_{value}'
    emp_impact_data[column_name] = emp_impact_data['venn_1_data'].apply(lambda x: contains_value(x, value))
    val = emp_impact_data[column_name].mean() * total_rows
    venn1_data.append(val)

venn2_data = []
for value in values_to_check:
    column_name = f'contains_{value}'
    emp_impact_data[column_name] = emp_impact_data['venn_2_data'].apply(lambda x: contains_value(x, value))
    val = emp_impact_data[column_name].mean() * total_rows
    venn2_data.append(val)

total_furloughed = int(venn1_data[0])
total_freeworkcanceled = int(venn1_data[1])
total_industryshutdown = int(venn1_data[2])
total_furloughed_and_freeworkcanceled = int(venn1_data[3])
total_furloughed_and_industryshutdown = int(venn1_data[4])
total_freeworkcanceled_and_industryshutdown = int(venn1_data[5])
total_furloughed_freeworkcanceled_industryshutdown = int(venn1_data[6])

total_laidofforfired = int(venn2_data[0])
total_freeworkcanceled = int(venn2_data[1])
total_industryshutdown = int(venn2_data[2])
total_laidofforfired_and_freeworkcanceled = int(venn2_data[3])
total_laidofforfired_and_industryshutdown = int(venn2_data[4])
total_freeworkcanceled_and_industryshutdown = int(venn2_data[5])
total_laidofforfired_freeworkcanceled_industryshutdown = int(venn2_data[6])

with st.container():
    col_1, col_2, col_3= st.columns([1, 1, 1], gap="large")

    with col_1:
        st.write("The data starkly illustrates the profound ramifications of the COVID-19 pandemic on artists, encompassing 4,247 individuals. Predominantly, job loss was the prevailing impact, affecting a majority of respondents. Notably, 2,284 artists grappled with the dual hardship of losing their jobs and experiencing canceled freelance work. Moreover, 1,884 faced the complete cessation of their respective industries, exacerbating the economic strain. The data becomes even more poignant with 996 artists enduring the triple blow of furloughs, canceled freelance work, and a total industry shutdown. This collective narrative vividly captures the extensive employment challenges that artists confronted during the pandemic's upheaval.")
        
    with col_2:
        plt.rcParams['text.color'] = 'white'
        plt.figure(figsize=None)
        venn_labels = {'100': total_laidofforfired,
               '010': total_freeworkcanceled,
               '110': total_laidofforfired_and_freeworkcanceled,
               '001': total_industryshutdown,
               '101': total_laidofforfired_and_industryshutdown,
               '011': total_freeworkcanceled_and_industryshutdown,
               '111': total_laidofforfired_freeworkcanceled_industryshutdown}

        venn3(subsets=(total_laidofforfired, total_freeworkcanceled, total_laidofforfired_and_freeworkcanceled,
               total_industryshutdown, total_laidofforfired_and_industryshutdown,
               total_freeworkcanceled_and_industryshutdown,
               total_laidofforfired_freeworkcanceled_industryshutdown),
        set_labels=('Laid off or Fired', 'Freelance Work Canceled', 'Industry Shutdown'), alpha=0.5,
        set_colors=('orange', 'lightgreen', 'royalblue'), normalize_to=total_furloughed_freeworkcanceled_industryshutdown)
        st.pyplot(transparent=True)

    with col_3:
        plt.rcParams['text.color'] = 'white'
        plt.figure(figsize=None)
        venn_labels = {'100': total_furloughed,
               '010': total_freeworkcanceled,
               '110': total_furloughed_and_freeworkcanceled,
               '001': total_industryshutdown,
               '101': total_furloughed_and_industryshutdown,
               '011': total_freeworkcanceled_and_industryshutdown,
               '111': total_furloughed_freeworkcanceled_industryshutdown}

        venn3(subsets=(total_furloughed, total_freeworkcanceled, total_furloughed_and_freeworkcanceled,
               total_industryshutdown, total_furloughed_and_industryshutdown,
               total_freeworkcanceled_and_industryshutdown,
               total_furloughed_freeworkcanceled_industryshutdown),
        set_labels=('Furloughed', 'Freelance Work Canceled', 'Industry Shutdown'), alpha=0.5,
        set_colors=('skyblue', 'violet', 'grey'), normalize_to=total_laidofforfired_freeworkcanceled_industryshutdown)
        st.pyplot(transparent=True)

# art practise impact

ap_labels = ['Canceled travel prevented me from attending my exhibitions/shows/performances/gigs',
             'I could no longer afford a studio/rehearsal space',
             'I was less motivated to pursue my artistic practice',
             'My scheduled exhibitions/shows/performances/gigs were canceled',
             'My studio/rehearsal space closed due to the pandemic',
             'I could no longer collaborate safely with others']
ap_counts = [4444, 3918, 5275, 7073, 3437, 7956]

st.write("\n")

with st.container():
    col_1, col_2= st.columns([1, 2], gap="large")
    
    with col_1:
        st.write("The relentless grip of the COVID-19 pandemic has reverberated through New York's artistic community, leaving a negative mark on the very fabric of creativity. A staggering 4,444 individuals lament the cancellation of travel, hindering their presence at exhibitions, shows, and performances—a profound disruption to the showcasing of their artistry. For 3,918 artists, the inability to sustain studio or rehearsal spaces became a harsh reality, jeopardizing their creativity. Safety concerns surrounding collaboration echoed in the minds of 7,956 individuals, casting shadows over the vibrant synergy that fuels artistic endeavors. Additionally, the cancellation of 7,073 paid shows and gigs dealt a severe blow to artists reliant on these platforms. The numbers paint a poignant picture of the immense artistic toll, revealing the pandemic's seismic impact on the essence of New York's artistic expression.")

    with col_2:
        ap_chart_data = pd.DataFrame({'Impact': ap_labels, 'Count': ap_counts})
        art_impact_chart = alt.Chart(ap_chart_data).mark_bar(color='#4c78a8').encode(
            x=alt.X('Count:Q', title='Count'),
            y=alt.Y('Impact:O', title=None, sort='-x'),
            tooltip=['Impact:N', 'Count:Q']
            ).properties(
            height=400,
        )

# Add text labels on the bars
        text = art_impact_chart.mark_text(
            align='left',
            baseline='middle',
            dx=3,  # Nudges text to the right so it doesn't overlap with the bar
            color='white'
        ).encode(
            text=alt.Text('Count:N', format=''),
            detail='Impact:N',
            
        )

# Combine the chart and text
        final_chart = (art_impact_chart + text).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )

        #final_chart
        st.altair_chart(final_chart, use_container_width=True)

st.write("------")

with st.container():
    st.title("Chapter 4: The Support They Need and Deserve")

    # Public Policy Awareness

    aware_of_gi = df['p26_awareofgi'].value_counts(normalize=True) * 100
    policy_group_participation = df['p28_policygroup'].value_counts(normalize=True) * 100

    aware_of_gi_df = aware_of_gi.reset_index()
    aware_of_gi_df.columns = ['Category', 'Percentage']
    policy_group_participation_df = policy_group_participation.reset_index()
    policy_group_participation_df.columns = ['Category', 'Percentage']

    st.markdown('<span style="font-size:20px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Public Policy Awareness among Artists </span>', unsafe_allow_html=True)
    st.write(" The heart of every successful artistic community is connected to public policy. In New York, where creativity is essential for culture and the economy, it's crucial to know and get involved in policy matters. For artists, dealing with advocacy and laws can be complicated, but knowing about them is the first step in creating a future where art doesn't just mirror society, but helps change it.")

    col1, col2 = st.columns(2)

    # Awareness of Guaranteed Income chart
    with col1:
        st.subheader("Artists' Knowledge of Financial Aid Programs")
        chart1 = alt.Chart(aware_of_gi_df).mark_bar().encode(
            x=alt.X('Category', axis=alt.Axis(labelAngle=0)),  
            y='Percentage',
            color=alt.Color('Category', legend=alt.Legend(title="Responses"), scale=alt.Scale(scheme='tableau20'))  
        ).properties(
            width=alt.Step(50)  
        )
        st.altair_chart(chart1, use_container_width=True)
        st.write("The data here reflects responses to whether artists were aware of concepts like guaranteed income or universal basic income before being introduced to Creatives Rebuild New York. With 25% answering yes, it's clear that there's awareness among some artists. Yet, a significant 70% were not aware, and about 6% were uncertain about these policies. This insight is crucial as it highlights a gap in knowledge that, if addressed, could open doors for many artists to financial resources aimed at sustaining their creative endeavors.")
    # Participation in Policy/Advocacy Groups chart
    with col2:
        st.subheader("Artists' Engagement in Shaping Policy")
        chart2 = alt.Chart(policy_group_participation_df).mark_bar().encode(
            x=alt.X('Category', axis=alt.Axis(labelAngle=0)), 
            y='Percentage',
            color=alt.Color('Category', legend=alt.Legend(title="Responses"), scale=alt.Scale(scheme='tableau20'))  
        ).properties(
            width=alt.Step(50) 
        )
        st.altair_chart(chart2, use_container_width=True)
        st.write("The chart presents a striking reality: only a small fraction of artists are actively involved in groups influencing public policy. With 81.47% not participating in such advocacy groups, it highlights an opportunity for more artists to voice their unique perspectives in forums that shape the legislative landscape. This low engagement rate suggests potential barriers that prevent artists from contributing to policy discussions that can significantly impact their professional and creative lives. Encouraging and facilitating artists' involvement in advocacy could pave the way for more inclusive and representative cultural policies.")
        
    # Navigating Health, Housing, and Financial Wellbeing
    st.markdown('<span style="font-size:20px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Navigating Health, Housing, and Financial Wellbeing </span>', unsafe_allow_html=True)
    health_image = Image.open('./assets/health.jpg')
    st.image(health_image, width=None)
    st.write("Let's dive into the crucial elements that form the bedrock of an artist's life: their health, housing, and financial stability. These are not mere conveniences, but the foundational pillars that support not only the creation of art but also the overall wellbeing and sustainability of an artist's career. Adequate health insurance, a stable home, a sound body and mind, and financial security are intertwined facets that fuel an artist's potential. Understanding how these elements interact is key to building robust support systems that ensure artists can thrive and contribute to our cultural fabric.")
    st.write("\n")

    def create_altair_bar_chart(category, title):
        #  handling for 'p14_carryingdebt' to merge duplicated responses
        if category == 'p14_carryingdebt':
            df[category] = df[category].replace({
                'Prefer not to answer ': 'Prefer not to answer'
            })

        
        data = df[category].value_counts().reset_index()
        data.columns = ['Response', 'Count']

        
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('Count:Q', title='Count'),
            y=alt.Y('Response:N', title=None, sort='-x'), 
            color=alt.Color('Response:N', legend=alt.Legend(title=''), scale=alt.Scale(scheme='tableau20')),
            tooltip=[alt.Tooltip('Response:N'), alt.Tooltip('Count:Q')]  
        ).properties(
            width=300,  
            height=300, 
            title=title  
        ).configure_title(
            anchor='start'
        )
        
        return chart


    # Health Insurance and Housing Stability
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Participants with Health Insurance Coverage")
        st.altair_chart(create_altair_bar_chart('p12_healthinsurance', 'Participants with Health Insurance Coverage'), use_container_width=True)
    with col2:
        st.write("### Stability of Housing")
        st.altair_chart(create_altair_bar_chart('p17_stablehousing', 'Stability of Housing'), use_container_width=True)

    st.markdown("---") 
    # Physical and Mental Health Status
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Physical Health Status")
        st.altair_chart(create_altair_bar_chart('p15_physicalhealth', 'Physical Health Status'), use_container_width=True)
    with col2:
        st.write("### Mental Health Status")
        st.altair_chart(create_altair_bar_chart('p16_mentalhealth', 'Mental Health Status'), use_container_width=True)
    st.markdown("---") 

    # debt and it's management.
    col1, col2 = st.columns(2)
    # Participants Carrying Debt
    with col1:
        st.write("### Participants Carrying Debt")
        st.altair_chart(create_altair_bar_chart('p14_carryingdebt', 'Participants Carrying Debt'), use_container_width=True)
    with col2:
        st.write("### Are they able to manage their debts?")
        st.altair_chart(create_altair_bar_chart('p14b_debtmanageable', 'Debt Management'), use_container_width=True)

image_aep = Image.open('./assets/AEP.jpg')
image_guaranteed_income = Image.open('./assets/GIA.jpg')

# AEP Image and Text
# Text for AEP and Guaranteed Income
st.write("---")

st.title("Chapter 5: The Impact of CRNYs GI Program")
st.markdown('<span style="font-size:20px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> CRNY\'s Melody in the Lives of New York\'s Artists </span>', unsafe_allow_html=True)
text_content = """
Inspiring Collaboration and Empowerment: The Artist Employment Program by Creatives Rebuild New York vividly comes to life in this illustration, where we see a tapestry of artists immersed in their crafts. From painters to musicians and dancers, these creators are not just engaging in artistic endeavors but are also forming synergistic partnerships with community organizations. Each artist, representing the diversity and vibrancy of New York, is empowered through a substantial salary, echoing the program's commitment to fostering both creative expression and financial stability. This image is a celebration of artistic collaboration, financial support, and the vibrant impact on local communities, encapsulating the essence of AEP's transformative vision.

Empowerment through Unconditional Support: This depiction of the Guaranteed Income for Artists program captures the essence of financial liberation and artistic freedom. Here, we see a kaleidoscope of 2,400 artists from various backgrounds, each engaged in their unique creative process, receiving a symbolic lifeline of $1,000 monthly payments. This initiative by Creatives Rebuild New York transcends traditional grantmaking, providing no-strings-attached support that empowers artists to pursue their passions while meeting basic needs. The image radiates a sense of security and opportunity, highlighting how this groundbreaking program is not just supporting artists financially but also nurturing their creative spirits and enriching the cultural tapestry of New York.
"""

# Define a layout with three columns
col1, col2, col3 = st.columns([1, 2, 1], gap="small")

with col1:
    st.image(image_aep, width=None, caption='Artist Employment Program by Creatives Rebuild New York' )  # Adjust width as needed

with col2:
    st.write(text_content)

with col3:
    st.image(image_guaranteed_income, width=None, caption='Guaranteed Income for Artists Program by Creatives Rebuild New York' )  # Adjust width as needed

st.write("------")

with st.container():
    st.subheader("Chapter 6: Reflections and Future Pathways")
    future_image = Image.open('./assets/future.jpg')
    st.image(future_image, width=None)
    st.write("\n")
    st.write("In conclusion, our exploration into New York's artistic community has revealed a multifaceted landscape, rich in diversity and creativity. Creatives Rebuild New York (CRNY) has positively influenced New York’s artistic landscape, enhancing artists’ financial, health, and housing stability. Acknowledging the demographic diversity of applicants, CRNY tailors support to artists of various ages, races, ethnicities, genders, and LGBTQIAP+ identities, recognizing the unique challenges each group faces. However, the COVID-19 pandemic's impact, which led to job losses and financial instability, underscores the need for ongoing and expanded public awareness. Effective outreach is essential to ensure artists are fully aware of the resources available to them. Moving forward, CRNY's continued collaboration with communities will be key in amplifying its initiatives, providing artists not only with the support they need but also the platforms to advocate for sustained change in public policy and social support systems.")
    st.markdown('<span style="font-size:30px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> Thank You. </span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:15px; font-style: italic; font-family: \'Times New Roman\', Times, serif;"> by Atharv Pramod Jangam, Smit Raichura, Subhadeep Jana </span>', unsafe_allow_html=True)
