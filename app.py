from dash import Dash, html, dcc, Input, Output, ctx
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Importação dos dados externos e criação de DataFrames
amazon_df = pd.read_csv("Assets/Data/Amazon.csv")
apple_df = pd.read_csv("Assets/Data/Apple.csv")
google_df = pd.read_csv("Assets/Data/Google.csv")
microsoft_df = pd.read_csv("Assets/Data/Microsoft.csv")
netflix_df = pd.read_csv("Assets/Data/Netflix.csv")

# Acrescentando a coluna de Nome aos DataFrames
amazon_df['Name'] = 'Amazon'
apple_df['Name'] = 'Apple'
google_df['Name'] = 'Google'
microsoft_df['Name'] = 'Microsoft'
netflix_df['Name'] = 'Netflix'


stocks_cpy = [
                amazon_df.copy(deep=True),
                apple_df.copy(deep=True),
                google_df.copy(deep=True),
                microsoft_df.copy(deep=True),
                netflix_df.copy(deep=True)
             ]

# Concatenando todos os DataFrames em um só DataFrame
stock_df = pd.concat(stocks_cpy, ignore_index=True)

# Fim da importação dos dados externos e criação de DataFrames

company_options = [{'label': x.upper(), 'value': x} for x in stock_df['Name'].unique()]

app.title = "Stock Chart"

# Inicio da construção do CSS do dashboard
div1_style = {'text-align': 'center'}

class_title = 'text-center'

class_button1 = """
                bg-transparent
                p-1 mt-2 text-center h2 
                text-secondary
                border rounded-0
                border-0
                border-end
                border-secondary
                px-3
                """

graph2_row_style = {
    'margin': '30px 1px'
}

# Selecionando os temas que vão ser utilizados no ThemeChangerAIO
available_themes = [
                        {"label": "Flatly", "value": dbc.themes.FLATLY},
                        {"label": "Cosmo", "value": dbc.themes.COSMO},
                        {"label": "Journal", "value": dbc.themes.JOURNAL},
                        {"label": "Cyborg", "value": dbc.themes.CYBORG},
                        {"label": "Darkly", "value": dbc.themes.DARKLY},
                        {"label": "Quartz", "value": dbc.themes.QUARTZ},
                        {"label": "Solar", "value": dbc.themes.SOLAR},
                        {"label": "Superhero", "value": dbc.themes.SUPERHERO},
                        {"label": "Vapor", "value": dbc.themes.VAPOR},
                    ]

# Fim da construção do CSS do dashboard


# Inicio da construção em HTML do dashboard
app.layout = dbc.Container([
    
    # Seção do gráfico de linhas com multi comparação
    # Utilizando o ThemeChangerAIO para mudança de tema
    dbc.Row(ThemeChangerAIO(aio_id="theme", radio_props={"value": dbc.themes.FLATLY, "options": available_themes})),

    dbc.Row([html.H1(children='Dash App', className=class_title)]),

    dbc.Row([dbc.Col([dcc.Dropdown(
        company_options,
        value=['Amazon', 'Apple', 'Google'],
        id='comparison-dropdown',
        multi=True
    )])]),

    dcc.Graph(id='multicomparison'),

    dbc.Row([
        dbc.Col([
            # Seção do gráfico de linhas
            html.H1("Stock Close Chart", className=class_title),

            dcc.Dropdown(company_options, value='Amazon', id='close-dropdown'),
            # Agrupamento de botões que permite filtrar a data
            html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('5 D', id='btn1', n_clicks=0, className=class_button1),
                        dbc.Button('1 M', id='btn2', n_clicks=0, className=class_button1),
                        dbc.Button('6 M', id='btn3', n_clicks=0, className=class_button1),
                        dbc.Button('1 A', id='btn4', n_clicks=0, className=class_button1),
                        dbc.Button('5 A', id='btn5', n_clicks=0, className=class_button1),
                        dbc.Button('Máx', id='btn6', n_clicks=0, className=class_button1)
                    ])
                ], style=div1_style),
            dcc.Graph(id='stocks')
        ], width=6),

        dbc.Col([
            # Seção do gráfico de CandleStick
            html.H1("Candlestick Chart", className=class_title),

            dcc.Dropdown(company_options, value='Amazon', id='candlestick-dropdown'),
            # Agrupamento de botões que permite filtrar a data
            html.Div([
                    dbc.ButtonGroup([
                        dbc.Button('5 D', id='btn7', n_clicks=0, className=class_button1),
                        dbc.Button('1 M', id='btn8', n_clicks=0, className=class_button1),
                        dbc.Button('6 M', id='btn9', n_clicks=0, className=class_button1),
                        dbc.Button('1 A', id='btn10', n_clicks=0, className=class_button1),
                        dbc.Button('5 A', id='btn11', n_clicks=0, className=class_button1),
                        dbc.Button('Máx', id='btn12', n_clicks=0, className=class_button1)
                    ])
                ], style=div1_style),
            dcc.Graph(id='candlestick')
        ], width=6)
    ], style=graph2_row_style)
])
# Fim da construção em HTML do dashboard


# Inicio da construção de callbacks do dashboard
@app.callback(
    [
     Output('comparison-dropdown', 'style'),
     Output('close-dropdown', 'style'),
     Output('candlestick-dropdown', 'style')
     ],
    Input(ThemeChangerAIO.ids.radio('theme'), 'value')
)
def update_dropdown(theme):
    """
        Este primeiro callback é sobre interação ThemeChangerAIO e o CSS do dropdown.
        Por serem classes dbc e dcc, o ThemeChanger não afeta o dropdown. Por isso,
        essa seção é destina a montar um CSS a depender do tema selecionado.
    """
    if theme == dbc.themes.FLATLY or theme == dbc.themes.COSMO or theme == dbc.themes.JOURNAL:
        dropdown_style = {'backgroundColor': 'white', 'color': 'black'}

    elif theme == dbc.themes.CYBORG:
        dropdown_style = {'backgroundColor': 'black', 'color': 'black'}
    elif theme == dbc.themes.DARKLY:
        dropdown_style = {'backgroundColor': '#494544', 'color': 'black'}

    elif theme == dbc.themes.QUARTZ:
        dropdown_style = {'backgroundColor': '#8c18f3', 'color': 'black'}

    elif theme == dbc.themes.SOLAR:
        dropdown_style = {'backgroundColor': '#104f5e', 'color': 'black'}

    elif theme == dbc.themes.SUPERHERO:
        dropdown_style = {'backgroundColor': '#505c6c', 'color': 'black'}

    elif theme == dbc.themes.VAPOR:
        dropdown_style = {'backgroundColor': '#200c34', 'color': '#e83cbc', 'border-color': '#e83cbc'}

    else:
        dropdown_style = {'backgroundColor': 'white', 'color': 'black'}

    return dropdown_style, dropdown_style, dropdown_style


@app.callback(
    Output(component_id='multicomparison', component_property='figure'),
    Input(component_id='comparison-dropdown', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), 'value')
)
def update_graph1(values, theme):
    """
        Este segundo callback é destinado a mudar o comportamento e o layout do gráfico
        com o input do dropdown e do ThemeChangerAIO. Por se tratar de um gráfico formado
        com várias outras linhas, é utilizado o fig.add_trace dentro do laço for.

        O uso do update_layout modifica o layout do gráfico. Usamos o template_from_url(theme)
        para usar um modelo do bootstrap. margin=dict(l=0, r=0, t=5, b=10) redefine as margens
        do gráfico.
    """

    fig = go.Figure()

    interval = ('2013-03-15', '2023-03-17')

    for value in values:
        sub_stock = (stock_df.loc[stock_df['Name'] == value]).copy(deep=True)
        date_filter = ((sub_stock['Date'] >= interval[0]) & (sub_stock['Date'] <= interval[1]))

        fig.add_trace(go.Scatter(
            x=sub_stock.loc[date_filter, 'Date'],
            y=sub_stock.loc[date_filter, 'Close'],
            mode='lines',
            name=value
        ))
        fig.update_layout(
            template=template_from_url(theme),
            xaxis_title="Date",
            yaxis_title="Stock Closing Price (USD)",
            legend_title="Companies",
            margin=dict(l=0, r=0, t=5, b=10)
        )
    return fig


@app.callback(
    Output(component_id='stocks', component_property='figure'),
    Input(component_id='close-dropdown', component_property='value'),
    Input('btn1', 'n_clicks'),
    Input('btn2', 'n_clicks'),
    Input('btn3', 'n_clicks'),
    Input('btn4', 'n_clicks'),
    Input('btn5', 'n_clicks'),
    Input('btn6', 'n_clicks'),
    Input(ThemeChangerAIO.ids.radio('theme'), 'value')
)
def update_graph2(value, btn1, btn2, btn3, btn4, btn5, btn6, theme):
    """
        Este terceiro callback tem o comportamento muito semelhante ao segundo.
        A diferença está na presença dos Inputs do botão. Usamos botões para
        modificar o intervalo de tempo e, consequentemente, o gráfico mostrado.

        ctx.triggered_id possui informações sobre o que iniciou o callback.
        Usamos o mesmo para descobrir qual o id do botão que iniciou o evento.
        Utilizamos laços de seleção e modificamos o intervalo de acordo com
        que foi selecionado.

        Com o intervalo em mãos, é selecionado o primeiro e o segundo valor de
        fechamento da ação. Se o primeiro valor for maior que o segundo, o
        gráfico ficará vermelho, indicando desvalorização naquele intervalo e
        verde caso contrário.

        Com o gráfico de linhas, também temos o Indicator. O Indicator serve
        para visualizar uma variação resumida de valores. O Indicator possui
        alguns modos de gráficos como o number, delta e gauge. No nosso exemplo
        estamos usando o number e delta. Esses modos foram usados para formatar
        no estilo nasdaq.
    """

    sub_stock = (stock_df.loc[stock_df['Name'] == value]).copy(deep=True)

    interval = ('2013-03-15', '2023-03-17')
    suffix = ' all time'

    # 5 Dias
    if "btn1" == ctx.triggered_id:
        interval = ('2023-03-10', '2023-03-17')
        suffix = ' past five days'
    # 1 Mês
    elif "btn2" == ctx.triggered_id:
        interval = ('2023-02-15', '2023-03-17')
        suffix = ' past month'
    # 6 Meses
    elif "btn3" == ctx.triggered_id:
        interval = ('2022-09-10', '2023-03-17')
        suffix = ' past 6 months'
    # 1 Ano
    elif "btn4" == ctx.triggered_id:
        interval = ('2022-03-15', '2023-03-17')
        suffix = ' past year'
    # 5 Anos
    elif "btn5" == ctx.triggered_id:
        interval = ('2018-03-15', '2023-03-17')
        suffix = ' past 5 years'
    # Máximo
    elif "btn6" == ctx.triggered_id:
        interval = ('2013-03-15', '2023-03-17')
        suffix = ' all time'

    date_filter = ((sub_stock['Date'] >= interval[0]) & (sub_stock['Date'] <= interval[1]))

    fst_close = sub_stock.loc[date_filter, 'Close'].iloc[0]
    lst_close = sub_stock.loc[date_filter, 'Close'].iloc[-1]

    color = '#9ac692' if lst_close > fst_close else '#dd9999'
    line_c = '#53bf3f' if lst_close > fst_close else '#ea5d5d'


    fig = go.Figure(go.Indicator(
        mode="number+delta",
        align='center',
        value=lst_close,
        number={"valueformat": "0.2f", "suffix": " USD"},
        delta={"reference": fst_close, 'relative': True, "valueformat": ".2%", "suffix": suffix},
        domain={'y': [0.75, 1], 'x': [0, 0.25]}
    ))

    fig.add_trace(go.Scatter(
        x=sub_stock.loc[date_filter, 'Date'],
        y=sub_stock.loc[date_filter, 'Close'],
        mode='lines',
        name=value,
        fill='tonexty',
        fillcolor=color,
        line={'color': line_c}
    ))

    fig.update_layout(
        template=template_from_url(theme),
        margin=dict(l=0, r=0, t=5, b=10)
    )

    return fig


@app.callback(
    Output('candlestick', 'figure'),
    Input('candlestick-dropdown', 'value'),
    Input('btn7', 'n_clicks'),
    Input('btn8', 'n_clicks'),
    Input('btn9', 'n_clicks'),
    Input('btn10', 'n_clicks'),
    Input('btn11', 'n_clicks'),
    Input('btn12', 'n_clicks'),
    Input(ThemeChangerAIO.ids.radio('theme'), 'value')
)
def update_graph3(value, btn7, btn8, btn9, btn10, btn11, btn12, theme):
    """
        Este quarto callback tem o comportamento muito semelhante ao terceiro.
        A única diferença reside no fato que usamos um candlestick chart
    """

    sub_stock = (stock_df.loc[stock_df['Name'] == value]).copy(deep=True)
    interval = ('2013-03-15', '2023-03-17')

    # 5 Dias
    if "btn7" == ctx.triggered_id:
        interval = ('2023-03-10', '2023-03-17')
    # 1 Mês
    elif "btn8" == ctx.triggered_id:
        interval = ('2023-02-15', '2023-03-17')
    # 6 Meses
    elif "btn9" == ctx.triggered_id:
        interval = ('2022-09-10', '2023-03-17')
    # 1 Ano
    elif "btn10" == ctx.triggered_id:
        interval = ('2022-03-15', '2023-03-17')
    # 5 Anos
    elif "btn11" == ctx.triggered_id:
        interval = ('2018-03-15', '2023-03-17')
    # Máximo
    elif "btn12" == ctx.triggered_id:
        interval = ('2013-03-15', '2023-03-17')

    date_filter = ((sub_stock['Date'] >= interval[0]) & (sub_stock['Date'] <= interval[1]))
    sub_stock = sub_stock.loc[date_filter]

    fig = go.Figure(data=[
                        go.Candlestick(x=sub_stock['Date'],
                        open=sub_stock['Open'],
                        high=sub_stock['High'],
                        low=sub_stock['Low'],
                        close=sub_stock['Close'])
                    ])

    fig.update_layout(
        template=template_from_url(theme),
        margin=dict(l=0, r=0, t=5, b=10)
    )

    return fig
# Fim da construção de callbacks do dashboard


if __name__ == '__main__':
    app.run(debug=True)
