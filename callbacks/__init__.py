from callbacks.artist import callback_artist
from callbacks.song import callback_song
from callbacks.score import callback_score
from callbacks.prediction import callback_prediction
from callbacks.record import callback_record

def register_callbacks(dash_app1):
    # # 콜백 설정
    # @dash_app1.callback(
    #     [Output("modal-previous", "style"), Output("modal-state-previous", "data")],
    #     [Input("open-modal-btn-previous", "n_clicks"), Input("close-modal-btn-previous", "n_clicks")],
    #     [State("modal-previous", "style"), State("modal-state-previous", "data")],
    # )
    # def toggle_modal_record(open_clicks, close_clicks, style, is_open):
    #     if open_clicks and (not is_open): 
    #         return {"display": "flex"}, True     
        
    #     if close_clicks and is_open: 
    #         return {"display": "none"}, False 
        
    #     return {"display": "none"}, False



    callback_artist(dash_app1)
    
    callback_song(dash_app1)

    callback_score(dash_app1)

    callback_prediction(dash_app1)

    callback_record(dash_app1)







