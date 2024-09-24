from dash import html, Input, Output, State, ALL, callback_context
import dash
import requests
import math
import pandas as pd
from config import uri

def callback_artist(dash_app1): 
    @dash_app1.callback(
        [
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
            Output("search-input-artist", "value", allow_duplicate=True),
            Output('table-artist', 'data'),
        ],
        [
            Input("open-modal-btn-artist", "n_clicks"),
            Input("close-modal-btn-artist", "n_clicks"),
            Input("search-input-artist", "n_submit"),
            Input("btn-search-artist", "n_clicks"),
            Input("search-input-artist", "value"),
            Input('table-artist', 'page_current'),
            Input('table-artist', 'page_size'),
            Input('table-artist', 'selected_rows')
        ],
        [
            State("modal-artist", "style"),
            State("modal-state-artist", "data")
        ],
        prevent_initial_call="initial_duplicate",
    )
    def handle_modal_and_update_output_artist(open_clicks, close_clicks, submit, search_clicks, search_value, page_current, page_size, selected_rows,  style, is_open):
        
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            df_artists = data.get('df_artists', {})
            df_artists = pd.DataFrame(df_artists)
            total = data.get('total', 0)
            total_page = -(-total // page_size)
            
            return df_artists.to_dict('records')
        
        triggered = [p['prop_id'] for p in callback_context.triggered][0]
        page_current += 1 

        if ('open-modal-btn-artist' in triggered) or ('prev-button-artist' in triggered) or ('next-button-artist' in triggered) or ('table-artist' in triggered):
            url = f'{uri}/artists?page={page_current}&per_page={page_size}'
            
            try:

                dict_artists = request_and_create_result(url)

                return {"display": "flex"}, True, search_value, dict_artists

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')


        
        if ('search-input-artist.n_submit' in triggered) or ('btn-search-artist' in triggered):

            if search_value.isdigit(): 
                url = f'{uri}/artists?page={page_current}&per_page={page_size}&artist_id={search_value}'
            elif type(search_value) == str: 
                url = f'{uri}/artists?page={page_current}&per_page={page_size}&name={search_value}'

            try:

                dict_artists = request_and_create_result(url)

                return {"display": "flex"}, True, search_value, dict_artists

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-artist' in triggered:
            return {"display": "none"}, False, "", dash.no_update
        
        return style, is_open, search_value, dash.no_update




    @dash_app1.callback(
        [
            Output('output-container-artist', 'children', allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("modal-artist", "style", allow_duplicate=True),
            Output("modal-state-artist", "data", allow_duplicate=True),
            Output("search-input-artist", "value", allow_duplicate=True)
        ],
        [
            Input('load-btn-artist', 'n_clicks'),
        ],
        [
            State('model-artist', "data"),
            State("modal-artist", "style"),
            State("modal-state-artist", "data"),
            State('table-artist', 'selected_rows'),
            State('table-artist', 'data'),
        ],
        prevent_initial_call=True,
    )
    def handle_load_button_artist(load_clicks, train_data_artist, style, is_open, checked_idx, data):
        if not checked_idx:
            return dash.no_update,  dash.no_update, dash.no_update, dash.no_update, ""

        for idx in checked_idx:
            val = data[idx]
            train_data_artist.append({"id": val["아티스트ID"], "name": val["이름"]})
        
        output_list = [
            html.Div(
                className="span-output-artist",
                children=[
                    html.Span(dic['name'], className='item-name'),
                ]
            ) for dic in train_data_artist
        ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]


        return output_list, train_data_artist, {"display": "none"}, False, ""



    @dash_app1.callback(
        [
            Output("output-container-artist", "children", allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("search-input-artist", "value", allow_duplicate=True)
        ],

        [Input("delete-btn-artist", "n_clicks")],

        [State('model-artist', "data")],
        
        prevent_initial_call="initial_duplicate"
    )
    def handle_delete_artist(*args):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['value']

        # Clear the output and checklist
        if triggered:
            return [], [], ""


    # 콜백 설정
    @dash_app1.callback(
        [Output("modal-info-artist", "style"), 
        Output("modal-state-info-artist", "data"),
        Output("output-container-artist-info", "children"),],

        [Input("open-modal-btn-info-artist", "n_clicks"),
         Input("close-modal-btn-info-artist", "n_clicks")],

        [State("modal-info-artist", "style"), 
        State("modal-state-info-artist", "data"),
        State('table-artist', 'selected_rows'),
        State('table-artist', 'data'),],
    )
    def toggle_modal_artist_info(*args):

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
        checked_idx = args[-2]
        data = args[-1]

        if open_clicks and (not is_open): 

            idx = checked_idx[-1]
            artist_id = int(data[idx]['아티스트ID'])


            # Flask API URL
            url = f'{uri}/artists/{artist_id}'


            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                artist = response.json()  # JSON 형식으로 응답 데이터 파싱

                output_list = [
                    html.Div([
                            html.Div(get_value(artist, "name", default='N/A'), className="value-name"),
                            html.Div(get_value(artist, "birth", default='N/A'), className="value-birth"),
                            html.Div(get_value(artist, "debut", default='N/A'), className="value-debut"),
                            html.Div(get_value(artist, "activity_year", default='N/A'), className="value-activity"),
                            html.Div(get_value(artist, "activity_type", default='N/A'), className="value-type"),
                            html.Div(get_value(artist, "gender", default='N/A'), className="value-gender"),
                            html.Div(get_value(artist, "genre", default='N/A'), className="value-agency"),
                            html.Div(get_value(artist, "agency", default='N/A'), className="value-genre"),
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
        [Output("modal-add-artist", "style"), 
         Output("modal-state-add-artist", "data")],
        
        [Input("open-modal-btn-add-artist", "n_clicks"), 
         Input("close-modal-btn-add-artist", "n_clicks"),
         Input("add-btn-artist", "n_clicks"),
         Input({'type': "input-artist", 'index': ALL}, 'value')],
        
        [State("modal-add-artist", "style"), 
         State("modal-state-add-artist", "data")],
    )
    def toggle_modal_artist_add(open_clicks, close_clicks, add_clicks, input_values, style, is_open):
        ctx = callback_context  # 현재의 콜백 컨텍스트를 가져옵니다.
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

        if ("open-modal-btn-add-artist" in triggered) and (not is_open): 
            return {"display": "flex"}, True     
        
        if ("close-modal-btn-add-artist" in triggered) and is_open: 
            return {"display": "none"}, False 
        
        if ("add-btn-artist" in triggered) and is_open: 
            keys = ['artist_id', 'name', 'birth', 'debut', 'activity_year', 'activity_type', 'gender', 'artist_genre_main', 'agency']
            data = {keys[i]: v for i, v in enumerate(input_values)}
            
            try:
                url = f"{uri}/artists"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                # 요청이 성공했는지 확인
                if response.status_code == 201:
                    response_data = response.json()  # JSON 데이터 파싱
                    artist_info = response_data['artist']  # 응답에서 artist 정보 추출
                    artist_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {artist_message}")
                    print(f"Added Artist - ID: {artist_info['artist_id']}, Name: {artist_info['name']}")
                else:
                    print(f"Failed to add artist. Status code: {response.status_code}")
            
            except requests.RequestException as e:
                print(f"Error sending data: {e}")
    
            return {"display": "none"}, False
        
        return dash.no_update, dash.no_update