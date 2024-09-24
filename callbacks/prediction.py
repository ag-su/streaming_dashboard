from dash import dcc, Input, Output, State, ctx, ALL, dash_table
import dash
import requests
import plotly.graph_objs as go
from config import uri

def callback_prediction(dash_app1):
    @dash_app1.callback(  
        [
            Output("output-container-graph", "children", allow_duplicate=True),
            Output("output-container-table", "children", allow_duplicate=True),
        ],

        [ 
            Input({"type": "score-input-activae", "index": ALL}, "value"),
            Input("pred-btn", "n_clicks") 
        ], 

        [   
            State('model-artist', 'data'), 
            State('model-song', 'data') 
        ],

        # 모든 score-input의 value를 Input으로 사용
        prevent_initial_call=True
    )
    def handle_predict_and_update_graph(input_values_activae, pred_clicks, data_artist, data_song):
        def create_graph(output_activae, preds_activae, data_artist, data_song): 
            
            s = data_song['subject']
            lst_names = [dic['name'] for dic in data_artist]
            n = ', '.join(lst_names)

            def create_data(preds_activae):
                import numpy as np 
                np_preds_activae = np.array(preds_activae)
                preds_activae_mean = list(np.mean(np_preds_activae, axis=0))

                if len(preds_activae) >= 2: 
                    d = [
                        {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae[idx][len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': f'일감상자수 예측값 ({lst_names[idx]})',
                        } for idx in range(len(preds_activae))
                    ] + \
                    [
                      {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae_mean[len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': f'일감상자수 예측값 (평균)',
                            'line': {
                                    'color': "rgba(255, 0, 0, 0.8)"  # 선 색깔을 빨간색으로 설정
                                        },
                        } 
                    ] + \
                    [go.Scatter(
                        x=[len(output_activae)],
                        y=[preds_activae_mean[len(output_activae)-1]],
                        mode='markers',
                        name="전 날 예측값",
                        marker={
                            'size': 7,
                            'symbol': 'square',  # 점 모양을 원으로 설정
                            'color': "rgba(255, 0, 0, 0.5)"      # 색상 설정
                        },
                    ) ]

                else:
                    d = [
                        {
                            'x': list(range(len(output_activae), 32)), 
                            'y': [output_activae[-1]] + preds_activae[0][len(output_activae):], 
                            'type': 'line', 
                            'mode': 'lines+markers',  # 선과 점을 모두 표시
                            'name': '일감상자수 예측값',
                            'line': {
                                    'color': "rgba(255, 0, 0, 0.8)"  # 선 색깔을 빨간색으로 설정
                                        },
                        } 
                         ] + \
                        [go.Scatter(
                        x=[len(output_activae)],
                        y=[preds_activae[0][len(output_activae)-1]],
                            mode='markers',
                            name="전 날 예측값",
                            marker={
                                'size': 7,
                                'symbol': 'square',  # 점 모양을 원으로 설정
                                'color': "rgba(255, 0, 0, 0.5)"      # 색상 설정
                            },
                        )] 
                return d

            return dcc.Graph(
                    id='xgb-pred-graph',
                    figure={
                        'data': create_data(preds_activae) +\
                            [ {
                                'x': list(range(1, len(output_activae)+1)), 
                                'y': output_activae, 
                                'type': 'line', 
                                'mode': 'lines+markers',  # 선과 점을 모두 표시
                                'name': '일감상자수',
                                'line': {
                                        'color': 'gray'  # 선 색깔을 빨간색으로 설정
                                        },
                            },
                        ],
                                            
                        'layout': {
                            'title': f"{n} - {s}",
                            "xaxis":{
                                'title': 'Days',
                                'tickmode': 'linear',  # 수동으로 설정
                                'tick0': 1,            # 첫 번째 틱 마크 위치
                                'dtick': 1             # 1단위로 틱 마크
                            },
                            'yaxis': {
                                'tickformat': ',d',  # 천 단위 구분 없이 정수 형태로 표시
                            'legend': {
                                'x': 1,            # x 좌표 (오른쪽으로 1)
                                'y': 1,            # y 좌표 (위쪽으로 1)
                                'xanchor': 'right', # x 기준점을 오른쪽으로 설정
                                'yanchor': 'top',   # y 기준점을 위쪽으로 설정
                            }

                            }
                        }
                    }
                )

        if not ctx.triggered:
            return dash.no_update, dash.no_update

        if pred_clicks: 
            # 모든 인풋의 값을 받아옴
            output_activae = [int(v) for v in input_values_activae if v]
            
            data = {
                "song_id": data_song['song_id'],
                "activaeUsers": output_activae,
            }

            # 요청, 응답 받아옴  
            # song_id, activaeUsers 를 요청값으로 보냄 
            try:
                url = f"{uri}/predictions"  # Flask API의 POST 엔드포인트
                response = requests.post(url, json=data)


                if response.status_code in (201, 200):
                    response_data = response.json()  # JSON 데이터 파싱
                    preds_activae = list(response_data['pred_by_artist'].values())

                    table_dict = response_data['table_data'][0]
                    table_cols = response_data['table_data'][1]
                    
                    output_table = dash_table.DataTable(
                                                        id="table-result",
                                                        data=table_dict, 
                                                        columns=table_cols,
                                                        page_size=11,  
                                                        # style_table={'width': '80%'},  # 테이블의 너비를 50%로 설정
                                                        style_header={
                                                                        'backgroundColor': "#222222",  # 헤더의 배경색
                                                                        'color': 'white',           # 헤더의 텍스트 색
                                                                        'fontWeight': 'bold'        # 헤더 텍스트 굵게
                                                                     },
                                                        style_cell={'textAlign': 'center'},  # 셀의 텍스트 정렬
                                                        )

                else:
                    song_message = response_data.get('message')  # 응답에서 message 추출
                    print(f"Message: {song_message}")
                    print(f"Failed to add song. Status code: {response.status_code}")

            except requests.RequestException as e:
                print(f"Error sending data: {e}")

        
            return [ create_graph(output_activae, preds_activae, data_artist, data_song) ], [ output_table ]
        
        return dash.no_update, dash.no_update