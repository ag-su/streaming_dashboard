
from dash import html, Input, Output, State, ALL, callback_context
import dash
import requests
import math
import plotly.graph_objs as go
import pandas as pd
from config import uri

def callback_record(dash_app1):

    @dash_app1.callback(
        [
            Output("modal-record", "style"),
            Output("modal-state-record", "data"),
            Output("search-input-record", "value", allow_duplicate=True),
            Output('table-record', 'data'),
        ],
        [
            Input("open-modal-btn-record", "n_clicks"),
            Input("close-modal-btn-record", "n_clicks"),
            Input("search-input-record", "n_submit"),
            Input("btn-search-record", "n_clicks"),
            Input("search-input-record", "value"),
            Input('table-record', 'page_current'),
            Input('table-record', 'page_size'),
            Input('table-record', 'selected_rows')
        ],
        [
            State("modal-record", "style"),
            State("modal-state-record", "data"), 
        ],
            prevent_initial_call="initial_duplicate",

    )
    def handle_modal_and_update_output_record(open_clicks, close_clicks, submit, search_clicks, search_value, page_current, page_size, selected_rows,  style, is_open):
        def request_and_create_result(url):
            def get_value(value, default='N/A'):
                # 확인: value가 nan인지 확인
                if isinstance(value, float) and math.isnan(value):
                    return default
                return value

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            df_records = data.get("df_records", [])
            df_records = pd.DataFrame(df_records)
            total = data.get('total', 0)
            total_page = -(-total // page_size)
            
            
            return df_records.to_dict('records')
        
        triggered = [p['prop_id'] for p in callback_context.triggered][0]
        page_current = page_current + 1 


        if ('open-modal-btn-record' in triggered) or ('prev-button-record' in triggered) or ('next-button-record' in triggered) or ("table-record" in triggered):
            url = f'{uri}/records?page={page_current}&per_page={page_size}'
            
            try:

                dict_records = request_and_create_result(url)
                
                return {"display": "flex"}, True, search_value, dict_records

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')
        
        if ('search-input-record.n_submit' in triggered) or ('btn-search-record' in triggered):

            if search_value.isdigit(): 
                url = f'{uri}/records?page={page_current}&per_page={page_size}&song_id={search_value}'
            elif type(search_value) == str: 
                url = f'{uri}/records?page={page_current}&per_page={page_size}&subject={search_value}'

            try:

                dict_records = request_and_create_result(url)

                return {"display": "flex"}, True, search_value, dict_records

            except requests.RequestException as e:
                print('Error fetching data', f'Error: {str(e)}')

        
        elif 'close-modal-btn-record' in triggered:
            return {"display": "none"}, False, "", dash.no_update
        
        return style, is_open, search_value, dash.no_update



    @dash_app1.callback(
        [Output("confirm-add-record", "message"),
         Output("confirm-add-record", "displayed"),],
        
        [Input("add-btn-record", "n_clicks"),
        Input({"type": "score-input-activae", "index": ALL}, "value"),],

        [State('model-song', "data"),],

        prevent_initial_call="initial_duplicate"
    )
    def handle_add_record(add_clicks, activaeUsers, song_data):
        # Determine which button was clicked
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id']
        if "add-btn-record" in triggered: 

                    # 모든 인풋의 값을 받아옴
            output_activae = [int(v) for v in activaeUsers if v is not None]

            data = {
                "song_id": song_data['song_id'],
                'subject': song_data['subject'],
                "activaeUsers": output_activae,
            }

            try:
                url = f"{uri}/records"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)

                if response.status_code in (201, 200):
                    response_data = response.json()  # JSON 데이터 파싱
                    song_info = response_data['song']  # 응답에서 song 정보 추출
                    song_message = response_data['message']  # 응답에서 message 추출

                    print(f"Message: {song_message}")
                    print(f"Added Record - ID: {song_info['song_id']}")
                    
                    return [f"{song_data['song_id']}-{song_data['subject']}: 입력값이 저장되었습니다."], True
                
                else:
                    print(f"Failed to add song. Status code: {response.status_code}")
                    return [f"{response.status_code} Error:: {song_data['song_id']}-{song_data['subject']}: 저장에 실패하였습니다."], True

            except requests.RequestException as e:
                print(f"Error sending data: {e}")

        return dash.no_update, False
    

    @dash_app1.callback(
        [
            Output('output-container-artist', 'children', allow_duplicate=True),
            Output('output-container-song', 'children', allow_duplicate=True),
            Output("output-container-score", "children", allow_duplicate=True),
            Output("model-song", "data", allow_duplicate=True),
            Output('model-artist', 'data', allow_duplicate=True),
            Output("modal-record", "style", allow_duplicate=True),
            Output("modal-state-record", "data", allow_duplicate=True),
            Output({"type": "score-input-activae", "index": ALL}, "value", allow_duplicate=True),
        ],
        [
            Input('load-btn-record', 'n_clicks'),
        ],
        [
            State("modal-record", "style"),
            State("modal-state-record", "data"),
            State('table-record', 'selected_rows'),
            State('table-record', 'data'),
        ],
        prevent_initial_call=True,
    )
    def handle_load_button_record(load_clicks, style, is_open, checked_idx, data):
        
        def make_list(lst):
            return lst + [None] * (30-len(lst))

        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id']

        if "load-btn-record" in triggered:

            if not checked_idx:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
            val = data[checked_idx[0]    ]
            train_data_song = {"song_id": val["곡ID"], "subject": val["제목"]}

            # 여기서 얻은 song_id로 artist_id들을 불러오고, artist_id에 해당하는 name을 받아야 한다. 
            # song_id로 record 데이터, artist_name 응답받기 
            
            song_id = int(train_data_song['song_id'])

            url = f'{uri}/records/{song_id}'

            # API 요청 보내기
            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                record = response.json()  # JSON 형식으로 응답 데이터 파싱


                train_data_artist = [{"id":artist['artist_id'], "name": artist['name']} for artist in record['artists']]

                
                output_list_artist = [
                    html.Div(
                        className="span-output-artist",
                        children=[
                            html.Span(dic['name'], className='item-name'),
                        ]
                    ) for dic in train_data_artist
                ] + [html.Button("X", id="delete-btn-artist", className="delete-btn")]


                output_list_song = [
                    html.Div(
                        className="span-output-song",
                        children=[
                            html.Span(train_data_song['subject'], className='item-subject'),
                        ]
                    ) 
                ] + [html.Button("X", id="delete-btn-song", className="delete-btn")]

                output_list_score = html.Div(
                    children=[
                        html.Span(f"Day {len(record['activaeUsers'])}", className="item-score"),
                        html.Span(f"일감상자수  |  {record['activaeUsers'][-1]}", className="item-score"),
                        html.Button("X", id="delete-btn-score", className="delete-btn")
                    ]
                )

                return output_list_artist, output_list_song, output_list_score, train_data_song, train_data_artist, {"display": "none"}, False, make_list(record["activaeUsers"])
            
            except requests.RequestException as e:

                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, [None]*30, [None]*30, [None]*30