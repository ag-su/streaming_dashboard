from dash import html, dcc

# 모달4 - 성적 입력 모달창 
def create_modal_score(): 
    return  html.Div(
                className="modal-score",
                id="modal-score",
                children=[ 
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-score",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("음원 성적 입력", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-score", className="btn-close-modal")
                                ]
                            ),


                            html.Div(
                                className="modal-content-score",
                                children=[
                                    html.Div(
                                        className="score-set",
                                        children=[
                                            html.Span(f"{i+1}일", className="score-index"),  # 인덱스 표시
                                            dcc.Input(id={"type": "score-input-activae", "index": f"{i+1}-1"}, type="text", className="score-input", placeholder=f"일 감상자수"),  # 첫 번째 인풋
                                        ]
                                    ) for i in range(30)  # 30개의 세트를 생성
                                ]
                            ),


                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("완료", id='complete-btn-score', className="btn-complete")
                                ]
                            )
                        ] 
                    )
                ]
            )                   