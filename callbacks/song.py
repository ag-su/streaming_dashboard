from dash import html, Input, Output, State, ALL, callback_context
import dash
import requests
import math
import pandas as pd
from config import uri

def callback_song(dash_app1): 
    @dash_app1.callback(
        [
            Output("modal-song", "style"),
            Output("modal-state-song", "data"),
            Output("search-input-song", "value", allow_duplicate=True),
            Output('table-song', 'data'),
        ],
        [
            Input("open-modal-btn-song", "n_clicks"),
            Input("close-modal-btn-song", "n_clicks"),
            Input("search-input-song", "n_submit"),
            Input("btn-search-song", "n_clicks"),
            Input("search-input-song", "value"),
            Input('table-song', 'page_current'),
            Input('table-song', 'page_size'),
            Input('table-song', 'selected_rows')
        ],
        [
            State("modal-song", "style"),
            State("modal-state-song", "data"), 
        ],
            prevent_initial_call="initial_duplicate",

    )
    def handle_modal_and_update_output_song(open_clicks, close_clicks, submit, search_clicks, search_value, page_current, page_size, selected_rows,  style, is_open):
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            df_songs = data.get("df_songs", [])
            df_songs = pd.DataFrame(df_songs)
            total = data.get('total', 0)
            total_page = -(-total // page_size)
            
            
            return df_songs.to_dict('records')
        
        triggered = [p['prop_id'] for p in callback_context.triggered][0]
        page_current = page_current + 1 


        if ('open-modal-btn-song' in triggered) or ('prev-button-song' in triggered) or ('next-button-song' in triggered) or ("table-song" in triggered):
            url = f'{uri}/songs?page={page_current}&per_page={page_size}'
            
            try:

                dict_songs = request_and_create_result(url)
                
                return {"display": "flex"}, True, search_value, dict_songs

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')
        
        if ('search-input-song.n_submit' in triggered) or ('btn-search-song' in triggered):

            if search_value.isdigit(): 
                url = f'{uri}/songs?page={page_current}&per_page={page_size}&song_id={search_value}'
            elif type(search_value) == str: 
                url = f'{uri}/songs?page={page_current}&per_page={page_size}&subject={search_value}'

            try:

                dict_songs = request_and_create_result(url)

                return {"display": "flex"}, True, search_value, dict_songs

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-song' in triggered:
            return {"display": "none"}, False, "", dash.no_update
        
        return style, is_open, search_value, dash.no_update


    @dash_app1.callback(
        [
            Output('output-container-song', 'children', allow_duplicate=True),
            Output('model-song', 'data', allow_duplicate=True),
            Output("modal-song", "style", allow_duplicate=True),
            Output("modal-state-song", "data", allow_duplicate=True),
            Output("search-input-song", "value", allow_duplicate=True)
        ],
        [
            Input('load-btn-song', 'n_clicks'),
        ],
        [
            State('table-song', 'selected_rows'),
            State('table-song', 'data'),
            State('model-song', "data"),
            State("modal-song", "style"),
            State("modal-state-song", "data"),
        ],
        prevent_initial_call=True,
    )
    def handle_load_button_song(load_clicks, checked_idx, data, train_data_song, style, is_open):

        if not checked_idx:
            return dash.no_update, checked_idx, dash.no_update, dash.no_update, ""
        
        val = data[checked_idx[0]]
        train_data_song = {"song_id": val["곡ID"], "subject": val["제목"]}
        
        
        output_list = [
            html.Div(
                className="span-output-song",
                children=[
                    html.Span(train_data_song['subject'], className='item-subject'),
                ]
            ) 
        ] + [html.Button("X", id="delete-btn-song", className="delete-btn")]

        return output_list, train_data_song, {"display": "none"}, False, ""


    @dash_app1.callback(
        [
            Output("output-container-song", "children", allow_duplicate=True),
            Output('model-song', 'data', allow_duplicate=True),
        ],

        [Input("delete-btn-song", "n_clicks")],
        
        [State('model-song', "data")],

        prevent_initial_call="initial_duplicate"
    )
    def handle_delete_song(*args):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['value']

        # Clear the output and checklist
        if triggered:
            return [], []

    # 콜백 설정
    @dash_app1.callback(
        [Output("modal-info-song", "style"), 
        Output("modal-state-info-song", "data"),
        Output("output-container-song-info", "children")],
       
        [Input("open-modal-btn-info-song", "n_clicks"),
         Input("close-modal-btn-info-song", "n_clicks")],
        
        [State("modal-info-song", "style"), 
        State("modal-state-info-song", "data"),
        State('table-song', 'selected_rows'),
        State('table-song', 'data'),],
    )
    def toggle_modal_song_info(*args):

        def get_value(d, key, default='N/A'):
            value = d.get(key, default)
            # 확인: value가 nan인지 확인
            if isinstance(value, float) and math.isnan(value):
                return default
            return value
        
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0] if ctx.triggered else None

        open_clicks = triggered['value']
        close_clicks = args[1]
        is_open = args[3]
        idx = args[-2][0]
        data = args[-1]

        if open_clicks and (not is_open): 

            # json_string = triggered['prop_id'].split(".")[0]
            song_id = int(data[idx]['곡ID'])

            # Flask API URL
            url = f'{uri}/songs/{song_id}'


            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                song = response.json()  # JSON 형식으로 응답 데이터 파싱

                output_list = [
                    html.Div([
                            html.Div(get_value(song, "song_id", default='N/A'), className="value-song-id"),
                            html.Div(get_value(song, "subject", default='N/A'), className="value-subject"),
                            html.Div(get_value(song, "release", default='N/A'), className="value-release"),
                            html.Div(get_value(song, "genre", default='N/A'), className="value-genre"),
                            html.Div(get_value(song, "album_type", default='N/A'), className="value-album-type"),
                            html.Div(get_value(song, "artist_name", default='N/A'), className="value-artist-name")
                    ]) 
                ]
                
                return {"display": "flex"}, True, output_list     
            
            except requests.RequestException as e:
                return {"display": "flex"}, True, [] 
        
        if close_clicks and is_open: 
            return {"display": "none"}, False, [] 
        
        return {"display": "none"}, False, []


    # 콜백 설정

    @dash_app1.callback(
        [Output("modal-add-song", "style"), 
         Output("modal-state-add-song", "data")],
        
        [Input("open-modal-btn-add-song", "n_clicks"), 
         Input("close-modal-btn-add-song", "n_clicks"),
         Input("add-btn-song", "n_clicks"),
         Input({'type': "input-song", 'index': ALL}, 'value')],
        
        [State("modal-add-song", "style"), 
         State("modal-state-add-song", "data")],
    )
    def toggle_modal_song_add(open_clicks, close_clicks, add_clicks, input_values, style, is_open):
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

        if ("open-modal-btn-add-song" in triggered) and (not is_open): 
            return {"display": "flex"}, True     
        
        if ("close-modal-btn-add-song" in triggered) and is_open: 
            return {"display": "none"}, False 
        
        if ("add-btn-song" in triggered) and is_open: 
            keys = ['song_id', 'subject', 'release', 'genre', 'album_type', 'artist_id']
            data = {}
            for i, v in enumerate(input_values):
                if i == 3:
                    data[keys[i]] = ', '.join(v)
                else: 
                    data[keys[i]] = v 
            
            try:
                url = f"{uri}/songs"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                # 요청이 성공했는지 확인
                if response.status_code == 201:
                    response_data = response.json()  # JSON 데이터 파싱
                    song_info = response_data['song']  # 응답에서 song 정보 추출
                    song_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {song_message}")
                    print(f"Added Artist - ID: {song_info['song_id']}, Name: {song_info['name']}")
                else:
                    print(f"Failed to add song. Status code: {response.status_code}")
            
            except requests.RequestException as e:
                print(f"Error sending data: {e}")
    
            return {"display": "none"}, False
        
        return dash.no_update, dash.no_update