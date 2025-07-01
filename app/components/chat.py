from dash import html, dcc
import dash_bootstrap_components as dbc

def create_chat_component():
    return html.Div(
        id='chat-component',
        className='chat-container',
        children=[
            html.Div(id='chat-display', className='chat-display'),
            dcc.Input(
                id='user-input',
                type='text',
                placeholder='Escribe tu mensaje...',
                className='chat-input'
            ),
            dbc.Button(
                'Enviar',
                id='send-button',
                n_clicks=0,
                className='send-button'
            ),
            dcc.Store(id='chat-history')
        ]
    )