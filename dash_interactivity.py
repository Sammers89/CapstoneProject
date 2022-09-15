import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash import Output, Input
import dash_html_components as html	
import dash_core_components as dcc	
from dash.dependencies import Input, Output	



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
                                              ),
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
def get_scatter_chart(entered_site, payload):
    print(entered_site)
    print(payload)
    if entered_site == 'ALL':
        new_df = spacex_df
        new_df2 = new_df[new_df["Payload Mass (kg)"]>=payload[0]]
        new_df3 = new_df2[new_df["Payload Mass (kg)"]<=payload[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", 
        color= "Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    else:
        new_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        new_df2 = new_df[new_df["Payload Mass (kg)"]>=payload[0]]
        new_df3 = new_df2[new_df["Payload Mass (kg)"]<=payload[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", 
        color="Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    return fig2 


# Run the app
if __name__ == '__main__':
    app.run_server()