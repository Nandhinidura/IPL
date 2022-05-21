
#Libraries
from email.mime import application
from optparse import Values
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import gunicorn
from dash import dash_table

#Importing Csv File
path = "https://raw.githubusercontent.com/immangeek/IPL-Data-app/master/resources/IPL_Matches.csv"
df = pd.read_csv(path)

#Dropping unneccesaries
df = df.drop(columns=['method','umpire1','umpire2'],axis=1)

#Adding Year
df['date'] = pd.to_datetime(df['date'])
df['season'] = df['date'].dt.year

#matches win by season
teams_per_season = df.groupby('season')['winner'].value_counts()
year = 2008
win_per_season_df = pd.DataFrame(columns=['year','team','wins'])
for items in teams_per_season.iteritems():
    if items[0][0]==year:
        print(items)
        win_series = pd.DataFrame({
            'year' : [items[0][0]],
            'team' : [items[0][1]],
            'wins' : [items[1]]
            
        })
        win_per_season_df = win_per_season_df.append(win_series)
        year += 1

#Luckiest Venues
venue_ser = df.groupby('venue')['winner'].value_counts()
venue_df = pd.DataFrame(columns=['venue','team','wins'])
for items in venue_ser.iteritems():
    temp_df = pd.DataFrame({
        'venue':[items[0][0]],
        'team':[items[0][1]],
        'wins':[items[1]]
    })
    venue_df = venue_df.append(temp_df,ignore_index=True)
                                 
lucky_venue=venue_df.sort_values(by='wins',ascending=False)
  
                                
                                 



#matches win by team
best_team = df['winner'].value_counts()
best_team_df = pd.DataFrame(columns = ['team','wins'])
for items in best_team.iteritems():
    temp_team = pd.DataFrame({
        'team' : [items[0]],
        'wins' : [items[1]]   
    })
    best_team_df = best_team_df.append(temp_team,ignore_index=True)

#Best players by awards
best_player = df['player_of_match'].value_counts()
best_player_df = pd.DataFrame(columns=['player','won_award'])
for items in best_player.iteritems():
    temp_player = pd.DataFrame({
        "player": [items[0]],
        'won_award': [items[1]]
    })
    
    best_player_df = best_player_df.append(temp_player,ignore_index=True)

#Top_Ten_Players
top_ten_players = best_player_df.iloc[0:10]

#Most win by Runs
most_runs_win = df[df['result']=='runs']
most_runs_win = most_runs_win.sort_values(by='result_margin',ascending=False)
most_runs_win = most_runs_win.iloc[0:3,[10,12,14 ]]

#Most Win by Wickets
most_wickets_win = df[df['result']=='wickets']
most_wickets_win = most_wickets_win.sort_values(by='result_margin',ascending=False)
most_wickets_win = most_wickets_win.iloc[0:10,[10,12,14 ]]


#Figure
fig_bestteam = px.bar(
    best_team_df,x='team',y='wins',color='team'
)
fig_bestteam.update_layout(xaxis_tickangle=-90)

fig_most_runs = px.bar(
    most_runs_win,x='winner',y='result_margin',orientation='v'
)






#Heroku App Intializing



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],)
server=app.server

#Layout Section: Bootstrap

app.layout = html.Div([
    dbc.Row([ (html.H1("IPL Data Dashboard",
        className='text-center font-weight-bold text-success')),
        (html.H3("Developed By Nandhini",className='text-center font-weight-bold text-success'))
        
    ]),

    dbc.Row([
        dbc.Col([
            (html.H5("Top Ten Players",className='text-center')),
        dash_table.DataTable(
            id='table',
            columns=[{"name":i,"id":i}
            for i in top_ten_players.columns],
            data = top_ten_players.to_dict('records'),
            style_cell=dict(textAlign='center'),
            style_header=dict(backgroundColor="palegreen"),
            style_data=dict(backgroundColor="lightcyan")
            
        )
            

        ]),

        dbc.Col([
            (html.H5("The Best Winning Teams",className="text-center")),
            dcc.Graph(id="box", figure=fig_bestteam)
            
            
             
        ])
    ]),

    dbc.Row([
        dbc.Col([
             (html.H5("Luckiest Venues for Teams",className='text-center')),
               dcc.Dropdown(id='dpdn1',value='Delhi Capitals',
               options=[{'value': x, 'label': x}
               for x in sorted(lucky_venue['team'].unique())
               
               ]),
               dcc.Graph(id= 'pie-chart' ,figure={})
                
        ]),


        dbc.Col([
            (html.H5("Matches win by Runs",className='text-center')),
               dcc.Graph(id="box1", figure=fig_most_runs)

             

        ])
    ])

    


])




#App Callback

@app.callback(
    Output("pie-chart", "figure"), 
    Input("dpdn1", "value") 
)
def generate_chart(team_selected):
    dff = lucky_venue[lucky_venue['team'] == team_selected]
    fig1 = px.pie(dff, values='wins', names='venue')
    return fig1





#App Debuging
if __name__=='__main__':
    app.run_server(debug=True)











