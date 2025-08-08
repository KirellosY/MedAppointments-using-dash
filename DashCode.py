import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import kagglehub

# Load dataset
dataset_path = kagglehub.dataset_download('joniarroba/noshowappointments')
df = pd.read_csv(dataset_path + '/KaggleV2-May-2016.csv')

# Clean & prepare
df['AppointmentDate'] = pd.to_datetime(df['AppointmentDay'])
df['ScheduledDate'] = pd.to_datetime(df['ScheduledDay'])
df['AppointmentDay'] = df['AppointmentDate'].dt.day_name()
df['ScheduledDay'] = df['ScheduledDate'].dt.day_name()
df['WaitingDays'] = (df['AppointmentDate'] - df['ScheduledDate']).dt.days
df = df[df['WaitingDays'] > 0]
df = df[df['Age'].between(0, 120)]
df.drop(['PatientId', 'AppointmentID'], axis=1, inplace=True)

# Map binary features
df['Gender'] = df['Gender'].map({'M': 'Male', 'F': 'Female'})
df['Scholarship'] = df['Scholarship'].map({0: 'No', 1: 'Yes'})
df['Alcoholism'] = df['Alcoholism'].map({0: 'No', 1: 'Yes'})
df['Hipertension'] = df['Hipertension'].map({0: 'No', 1: 'Yes'})
df['Diabetes'] = df['Diabetes'].map({0: 'No', 1: 'Yes'})
df['Handcap'] = np.where(df['Handcap'] > 0, 'Yes', 'No')
df['SMS_received'] = df['SMS_received'].map({0: 'No', 1: 'Yes'})

# --- Dashboard Content Preparation ---
total_appointments = len(df)
noshow_rate = (df['No-show'] == 'Yes').mean() * 100
avg_waiting = df['WaitingDays'].mean()

# Overview plots
no_show_pie = px.pie(df, names='No-show', title='No-show Rate', color_discrete_sequence=['#FF6692', '#19d3f3'])
waiting_hist = px.histogram(df, x='WaitingDays', title='Waiting Days Distribution')

# SMS effect
sms_noshow = (
    df.groupby('SMS_received')['No-show']
    .value_counts(normalize=True).unstack().reset_index().melt(id_vars='SMS_received',
                                                                var_name='No-show',
                                                                value_name='Proportion')
)
sms_bar = px.bar(sms_noshow, x='SMS_received', y='Proportion', color='No-show',
                 barmode='group', title='No-show Rate by SMS Received')

# Neighborhood plots
top5_noshow_neigh = df[df['No-show'] == 'Yes']['Neighbourhood'].value_counts().head(5).reset_index()
top5_noshow_neigh.columns = ['Neighbourhood', 'Count']
top5_noshow_fig = px.bar(top5_noshow_neigh, x='Neighbourhood', y='Count', title='Top 5 Neighbourhoods (No-shows)')

all_neigh = df['Neighbourhood'].value_counts().reset_index()
all_neigh.columns = ['Neighbourhood', 'Appointments']
all_neigh_fig = px.bar(all_neigh.head(5), x='Neighbourhood', y='Appointments',
                       title='Appointments per Neighbourhood', height=500)

# Time series plots

# Appointments per Month
AppM = df['AppointmentDate'].dt.month.value_counts().sort_index()
fig2 = px.bar(
    x=AppM.index, y=AppM.values,
    title='Appointed Month Distribution in 2016',
    labels={'x': 'Month', 'y': 'Appointment Count'}
)

# Appointment Days of Week
fig3 = px.bar(
    x=df['AppointmentDay'].value_counts().index,
    y=df['AppointmentDay'].value_counts().values,
    title='Appointment Day of Week Distribution',
    labels={'x': 'Day of Week', 'y': 'Count'}
)

# Scheduled per Month
scheduled_month_counts = df['ScheduledDate'].dt.month.value_counts().sort_index()
fig5 = px.bar(
    x=scheduled_month_counts.index,
    y=scheduled_month_counts.values,
    title='Scheduled Month Distribution',
    labels={'x': 'Month', 'y': 'Scheduled Count'}
)

# Scheduled Day of Week
fig6 = px.bar(
    x=df['ScheduledDay'].value_counts().index,
    y=df['ScheduledDay'].value_counts().values,
    title='Scheduled Day of Week Distribution',
    labels={'x': 'Day of Week', 'y': 'Count'}
)

# Waiting Days Histogram
fig7 = px.histogram(df, x='WaitingDays', title='Waiting Days Distribution')

# Waiting vs no-show
wait_vs_noshow = px.box(df, x='No-show', y='WaitingDays',
                        title='Waiting Days vs No-show Status', color='No-show')

# Start app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "No-show Dashboard"

app.layout = dbc.Container([
    html.H2("No-show Appointments Dashboard", className="text-center my-3"),

    # Cards row
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Appointments", className="card-title"),
                html.H2(f"{total_appointments:,}")
            ])
        ], color="primary", inverse=True), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("No-show Rate", className="card-title"),
                html.H2(f"{noshow_rate:.1f}%")
            ])
        ], color="danger", inverse=True), md=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Avg. Waiting Days", className="card-title"),
                html.H2(f"{avg_waiting:.1f}")
            ])
        ], color="info", inverse=True), md=4),
    ], className="mb-4"),

    # Tabs
    dbc.Tabs([
        dbc.Tab(label="Overview", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=no_show_pie), md=6),
                dbc.Col(dcc.Graph(figure=waiting_hist), md=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=sms_bar), md=12)
            ])
        ]),

        dbc.Tab(label="Neighbourhoods", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=top5_noshow_fig), md=6),
                dbc.Col(dcc.Graph(figure=all_neigh_fig), md=6)
            ])
        ]),

        dbc.Tab(label="Time Series", children=[
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig2), md=6),
        dbc.Col(dcc.Graph(figure=fig3), md=6) 
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig5), md=6),  
        dbc.Col(dcc.Graph(figure=fig6), md=6)   
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig7), md=12) 
    ])
]),

        dbc.Tab(label="Summary", children=[
            dbc.Card([
                dbc.CardBody([
                    html.H4("Summary of Rare Features", className="card-title"),
                    html.P("These features were relatively uncommon among patients:"),
                    html.Ul([
                        html.Li("🎓 Only 9.27% had a scholarship."),
                        html.Li("🍷 Alcoholism: 2.5%"),
                        html.Li("💊 Hypertension: 20.9%"),
                        html.Li("🩸 Diabetes: 7.4%"),
                        html.Li("♿ Handicap: 1.82%"),
                    ]),
                    html.P("These may still be important in modeling no-shows.")
                ])
            ], className="mt-4")
        ])
    ]),

    html.Footer("Made with Dash", className="text-center text-muted my-4")
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
