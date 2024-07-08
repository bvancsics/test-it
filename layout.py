from dash import html
import dash_chat_components as dch


def get_layout():
    return html.Div([
        dch.Chat([
            dch.ChatMessageList(
                [],
                id="chat-msg-list",
                className="px-2",
                style={"height": "calc(100% - 65px)"}
            ),
            dch.ChatInput(
                id='chat-input',
                className="mt-2 mx-2",
                autofocus=True,
                style={"height": "65px"}
            ),
        ], className="h-100"),
    ], style={
        'height': 'calc(100vh - 40px)',
        'margin': '20px auto',
        'maxWidth': '900px'
    })
