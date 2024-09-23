from dash import html

# ===== 메인 시각화 컴포넌트 =====
def create_example_graph(): 
    return html.Div(
                        children=[
                                    html.Div(id="output-container-graph", className="container-graph"),
                                    html.Div(id="output-container-table", className="container-table")
                                ]
                    )