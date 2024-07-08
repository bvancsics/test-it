from message import get_messages
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_chat_components as dch
from app import app


@app.callback(
    Output("chat-msg-list", "children", allow_duplicate=True),
    Output("chat-input", "disabled", allow_duplicate=True),
    Output("chat-input", "autofocus"),
    Input("chat-input", "n_submit"),
    State("chat-input", "value_on_submit"),
    State("chat-msg-list", "children"), prevent_initial_call=True)
def send_message(n_submit, value_on_submit, msg_list):
    if n_submit is None:
        raise PreventUpdate
    else:
        msg_list = msg_list + [
            dch.ChatMessage(
                value_on_submit,
                avatar="user.png",
                direction="outgoing",
            )
        ] + [
            dch.ChatMessage(
                m["content"],
                avatar=m["avatar"],
                direction=m["direction"],
            ) for m in get_messages(value_on_submit)]

        return msg_list, False, True
