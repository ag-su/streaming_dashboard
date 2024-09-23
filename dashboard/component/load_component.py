from dash import html, dcc, dash_table
from .artist import create_modal_artist_list
from .song import create_modal_song_list
from .score import create_modal_score
from .prediction import create_example_graph


def load_component(): 
    return html.Div(children=[

            dcc.ConfirmDialog(
                id='confirm-add-record',
                message="저장"
            ),

            # 상단바 컴포넌트
            create_navbar(),

            # 데이터 입력 컴포넌트 
            create_data_insert(),
            
            # 메인 시각화 컴포넌트 
            create_example_graph(),


            
            # ===== 모달 ===== 
            # [ 이전 기록 불러오기 ]
            create_modal_previous_record(),
            
            # [ 가수 리스트 ]
            create_modal_artist_list(),

            # [ 곡 리스트 ]
            create_modal_song_list(),

            # [ 음원 성적 입력 ]
            create_modal_score(),

            # ===== 상태 변수 =====
            # 상태 저장 컴포넌트
            create_store(),
            
            # 스크립트 추가
            dcc.Location(id="url", refresh=False),
            html.Script(src="/assets/scroll.js"),

            # 하단 푸터 컴포넌트 
            # create_footer(),

        ])





# ===== 상단바 컴포넌트 =====
def create_navbar():
    return html.Div(
        id='navbar',
        className="navbar",
        children=[
            html.A(
                id='navbar-title',
                className="navbar-title",
                href="#",
                children="MF",
            ),
            html.Div(
                className="navbar-dashboard-title",
                    children=[
                                html.A("데이터 입력", href="#", className="link-class", id='link-class-1'),
                                html.A("예측 결과", href="#output-container-graph", className="link-class", id='link-class-2'),
                            ]
            )
        ],
    )


# ===== 상단바 컴포넌트 =====
def create_footer():
    return     html.Footer(
        children="© 2024 Your Company",
    )



# ===== 데이터 입력 컴포넌트 =====
def create_data_insert():  
    return html.Div(
        id='data-insert',
        className="data-insert",
        children=[

            # 입력값 저장, 이전 기록 불러오기 버튼 
            html.Div(
                className="button-container",
                children=[
                    html.Button('입력값 저장', id='add-btn-record', className='button-1'),

                    # 버튼을 클릭하여 모달을 열도록 설정
                    html.Button("이전 기록 불러오기", id="open-modal-btn-record", className="button-1"),
                ]
            ),

            # 가수 정보 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("가수 정보", className="text-artist"),
                    html.Button('+', id="open-modal-btn-artist", className='button-plus'),
                    html.Div(id='output-container-artist', className='output-container-artist')
                ]
            ),

            # 곡 정보 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("곡 정보", className="text-song"),
                    html.Button('+', id="open-modal-btn-song", className='button-plus'),
                    html.Div(id='output-container-song', className='output-container-song')
                ]
            ),

            # 음원 성적 입력 
            html.Div(
                className="data-container",
                children=[
                    html.Div("음원 성적", className="text-score"),
                    html.Button('+', id="open-modal-btn-score", className='button-plus'),
                    html.Div(id='output-container-score', className='output-container-score')
                ]
            ),


            # 예측 버튼 
            html.Div(
                className="button-container-pred",
                children=[
                    html.Button('일감상자수 예측', id="pred-btn", className='button-pred'),
                ]
            ), 

            ])

# 모달1 - [ 이전 기록 불러오기 ]
def create_modal_previous_record(): 
    return  html.Div(
                className="modal-previous",
                id="modal-record",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-previous",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("이전 기록 불러오기", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-record", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="곡 ID를 입력해주세요.", id="search-input-record", className="search-input"),
                                    html.Button("🔍", id="btn-search-record", className="btn-search")
                                ] 
                            ),
                            # 새로운 중앙 컨텐츠: 인덱스와 리스트
                            html.Div(
                                className="modal-content",
                                children=[
                                    dash_table.DataTable(
                                        id='table-record',
                                        columns=[{"name": i, "id": i} for i in ["곡ID", '제목', '저장날짜']],
                                        page_current=0,
                                        page_size=10,
                                        page_action='custom',  # 서버 측 페이지네이션 활성화
                                        row_selectable='single',
                                        selected_rows=[],
                                    ),
                                ]
                            ),                           
                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("삭제", className="btn-delete"),
                                    html.Button("불러오기", id="load-btn-record", className="btn-load")
                                ]
                            )
                        ]
                    )
                ]
            )

# ===== 상태 저장 컴포넌트 =====
def create_store():
    return html.Div(
        children=[
            dcc.Store(id='modal-state-record', data=False),
            dcc.Store(id='modal-state-artist', data=False),
            dcc.Store(id='modal-state-info-artist', data=False),
            dcc.Store(id='modal-state-add-artist', data=False),
            dcc.Store(id='modal-state-song', data=False),
            dcc.Store(id="modal-state-info-song", data=False),
            dcc.Store(id='modal-state-add-song', data=False),
            dcc.Store(id='modal-state-score', data=False),
            
            dcc.Store(id='value-score', data={}),

            dcc.Store(id='model-artist', data=[]),
            dcc.Store(id='model-song', data={}),

            dcc.Store(id='current-page-artist', data=1),
            dcc.Store(id='total-page-artist', data=100),

            dcc.Store(id='current-page-song', data=1),
            dcc.Store(id='total-page-song', data=100),

            dcc.Store(id='current-page-record', data=1),
            dcc.Store(id='total-page-record', data=100)
        ]
    )
