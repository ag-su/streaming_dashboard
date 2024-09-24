from dash import html, dcc, Input, Output, State, ctx, ALL
import dash


def callback_score(dash_app1):
    # 콜백 설정
    @dash_app1.callback(
        [Output("modal-score", "style", allow_duplicate=True), 
        Output("modal-state-score", "data", allow_duplicate=True)],
        
        [Input("open-modal-btn-score", "n_clicks"), 
        Input("close-modal-btn-score", "n_clicks")],
        
        [State("modal-score", "style"), 
        State("modal-state-score", "data")],

        prevent_initial_call=True
    )
    def toggle_modal_score(open_clicks, close_clicks, style, is_open):
        if open_clicks and (not is_open): 
        
            return {"display": "flex"}, True     
        
        if close_clicks and is_open: 
            return {"display": "none"}, False 
        
        return {"display": "none"}, False


    @dash_app1.callback(  
        [Output("output-container-score", "children", allow_duplicate=True),
        Output("modal-score", "style", allow_duplicate=True), 
        Output("modal-state-score", "data", allow_duplicate=True), 
        Output("complete-btn-score", "n_clicks"),
        Output("output-container-graph", "children", allow_duplicate=True),
        Output({"type": "score-input-activae", "index": ALL}, "value")],

        [Input({"type": "score-input-activae", "index": ALL}, "value"),
        Input("complete-btn-score", "n_clicks")],

        [State("modal-score", "style"), 
        State("modal-state-score", "data"),
        State('model-artist', 'data'),
        State('model-song', 'data')],

        # 모든 score-input의 value를 Input으로 사용
        prevent_initial_call=True
    )
    def update_output_score(input_values_activae, complete_clicks, style, is_open, data_artist, data_song):
        def create_graph(output_activae, data_artist, data_song): 
            n = ', '.join([dic['name'] for dic in data_artist])
            s = data_song['subject']
            return dcc.Graph(
                    id='xgb-pred-graph',
                    className="xgb-pred-graph",
                    figure={
                        'data': [
                            {
                                'x': list(range(1, len(output_activae)+1)), 
                                'y': output_activae, 
                                'type': 'line', 
                                'name': '일감상자수',
                                'line': {
                                        'color': 'gray'  # 선 색깔을 빨간색으로 설정
                                            },
                                },
                        ],
                                            
                        'layout': {
                            'title': f"{n} - {s}",
                            'yaxis': {
                                'tickformat': ',d'  # 천 단위 구분 없이 정수 형태로 표시
                            }
                        }
                    }
                )

        if not ctx.triggered:
            return dash.no_update, dash.no_update, dash.no_update, create_graph([0, 0, 0, 0, 0], data_artist, data_song), dash.no_update
        
        # 모든 인풋의 값을 받아옴
        output_activae = [v for v in input_values_activae if v]

        output = html.Div(
            children=[
                html.Span(f"Day {len(output_activae)}", className="item-score"),
                html.Span(f"일감상자수  |  {output_activae[-1]}", className="item-score"),
                html.Button("X", id="delete-btn-score", className="delete-btn")
            ]
        )

        if complete_clicks and output_activae: 

            return output, {"display": "none"}, False, 0, create_graph(output_activae, data_artist, data_song), input_values_activae
        
        return output, dash.no_update, dash.no_update, 0, create_graph(output_activae, data_artist, data_song), dash.no_update

    @dash_app1.callback(
        [
            Output("output-container-score", "children", allow_duplicate=True),
            Output({"type": "score-input-activae", "index": ALL}, "value", allow_duplicate=True),
        ],
        
        [Input("delete-btn-score", "n_clicks")],

        prevent_initial_call=True
    )
    def handle_delete_score(clicks_delete):
        # Clear the output and checklist
        if clicks_delete:
            return [], [None]*30