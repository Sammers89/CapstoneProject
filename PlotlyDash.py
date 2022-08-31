import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
 # TASK 1: Add a dropdown 
 dcc.Dropdown(id='site-dropdown', 
                                             options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder='Select a Launch Site',
                                             searchable=True
                                             ,
                                html.Br(),

                                #pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # range slider 
                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:'0', 100:'100'},
                                                value=[min_payload, max_payload]
                                                ),
 # TASK 4: Add a scatter chart 
html.Div(dcc.Graph(id='success-payload-scatter-chart')),
# TASK 2: Add a pie chart based on selected site
                     

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_spacexdf=spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_spacexdf=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_spacexdf,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig

        # TASK 4: Callback function to render scatter plot

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(entered_site,payload):
    filtered_spacexdf2 = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]

    if entered_site=='ALL':
        fig=px.scatter(filtered_df2,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered_df[filtered_df2['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()