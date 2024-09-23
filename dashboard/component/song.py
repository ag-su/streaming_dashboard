from dash import html, dcc, dash_table
import pandas as pd

# 샘플 데이터 생성
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [24, 27, 22, 32, 29],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
})

# 모달3 - 곡 목록 모달창   
def create_modal_song_list(): 
    
    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    song_data = {
        '000001': ['제목 1', '2021-02-15'],
        '000002': ['제목 2', '2020-06-10'],
        '000003': ['제목 3', '2019-11-22']
    }

    return html.Div(
                className="modal-list",
                id="modal-song",
                children=[
                    
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-list",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 목록", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-song", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="곡 ID 또는 아티스트 ID를 입력해주세요.", id='search-input-song', className="search-input"),
                                    html.Button("🔍", id='btn-search-song', className="btn-search")
                                ] 
                            ),
                            # 새로운 중앙 컨텐츠: 인덱스와 리스트
                            html.Div(
                                className="modal-content",
                                children=[
                                    dash_table.DataTable(
                                        id='table-song',
                                        columns=[{"name": i, "id": i} for i in ["곡ID", '제목', '발매일']],
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
                                    html.Button("곡 정보 추가", id="open-modal-btn-add-song", className="btn-delete"),
                                    html.Button("상세 정보 보기", id="open-modal-btn-info-song", className="btn-detail"),
                                    html.Button("불러오기", id='load-btn-song', className="btn-load")
                                ]
                            ),

                            create_modal_song_info(),
                            create_modal_song_add()

                        ]
                    )
                ]
            )

# 모달3-1 - 곡 정보 모달창 
def create_modal_song_info(): 
    return  html.Div(
                className="modal-info",
                id="modal-info-song",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-info",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 정보", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-info-song", className="btn-close-modal")
                                ]
                            ),
                            

                            html.Div(
                                className="modal-content-info",
                                children=[
                                    # 인덱스와 값을 포함하는 Flexbox 컨테이너
                                    html.Div(
                                        className="index-value-container",
                                        children=[
                                            # 인덱스 열
                                            html.Div(
                                                className="index-column",
                                                children=[
                                                    html.Div("곡 ID", className="index-song-id-info"),
                                                    html.Div("제목", className="index-subject-info"),
                                                    html.Div("발매일", className="index-release-info"),
                                                    html.Div("장르", className="index-genre-info"),
                                                    html.Div("앨범타입", className="index-type-info"),
                                                    html.Div("가수", className="index-type-info")
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                id='output-container-song-info',
                                                className="value-column",
                                            ),
                                          
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )

# 모달3-2 - 곡 추가 모달창 
def create_modal_song_add(): 
    return  html.Div(
                className="modal-add",
                id="modal-add-song",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-add",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("곡 추가", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-add-song", className="btn-close-modal")
                                ] 
                            ),
                            
                            html.Div(
                                className="modal-content-info",
                                children=[
                                    # 인덱스와 값을 포함하는 Flexbox 컨테이너
                                    html.Div(
                                        className="index-value-container",
                                        children=[
                                            # 인덱스 열
                                            html.Div(
                                                className="index-column",
                                                children=[
                                                    html.Div("곡 ID", className="index-song-id-info"),
                                                    html.Div("제목", className="index-subject-info"),
                                                    html.Div("발매일", className="index-release-info"),
                                                    html.Div("장르", className="index-genre-info"),
                                                    html.Div("앨범타입", className="index-type-info"),
                                                    html.Div("가수", className="index-artist-info"),
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                className="value-column",
                                                children=[
                                                    dcc.Input(id={'type': 'input-song', 'index': 'id'}, className="input-song-id", type="text"),
                                                    dcc.Input(id={'type': 'input-song', 'index': 'subject'}, className="input-subject", type="text"),
                                                    dcc.Input(id={'type': 'input-song', 'index': 'release'}, className="input-release", type="text", placeholder="ex) 2024-09-09"),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-song', 'index': 'activity'}, 
                                                        className="input-genre",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': 'R&B/Soul', 'value': 'R&B/Soul'},
                                                            {'label': '국내드라마', 'value': '국내드라마'},
                                                            {'label': '댄스', 'value': '댄스'},
                                                            {'label': '랩/힙합', 'value': '랩/힙합'},
                                                            {'label': '록/메탈', 'value': '록/메탈'},
                                                            {'label': '발라드', 'value': '발라드'},
                                                            {'label': '인디음악', 'value': '인디음악'},
                                                            {'label': '포크/블루스', 'value': '포크/블루스'},
                                                        ],
                                                        placeholder='장르 선택 (복수 선택 가능)',  # 기본값
                                                        multi=True
                                                    ),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-song', 'index': 'album-type'}, 
                                                        className="input-type",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': '싱글', 'value': '싱글'},
                                                            {'label': 'EP', 'value': 'EP'},
                                                            {'label': '정규', 'value': '정규'},
                                                            {'label': 'OST', 'value': 'OST'},
                                                            {'label': '베스트', 'value': '베스트'},
                                                            {'label': '옴니버스', 'value': '옴니버스'},
                                                            {'label': '리믹스', 'value': '리믹스'},
                                                            {'label': '리메이크', 'value': '리메이크'},
                                                            {'label': '라이브', 'value': '라이브'},
                                                            {'label': '스페셜', 'value': '스페셜'},
                                                        ],
                                                        placeholder='앨범 타입 선택',  # 기본값
                                                    ),
                                                    dcc.Input(id={'type': 'input-song', 'index': 'artist-id'}, 
                                                              className="input-artist-id", 
                                                              type="text",
                                                              placeholder="ex) 00001,00002,00003"),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            
                            # 푸터: 추가 버튼 
                            html.Div(
                                className="modal-footer-add",
                                children=[
                                    html.Button("추가", id='add-btn-song', className="btn-add"),
                                ]
                            ),
                        ]
                    )
                ]
            )