from dash import html, dcc, dash_table

# 모달2 - 아티스트 목록 모달창 
def create_modal_artist_list(): 

    # 곡 정보 데이터 (곡 ID: [제목, 발매일])
    artist_data = {
        '000001': ['이름 1', '1999-02-15'],
        '000002': ['이름 2', '1997-06-10'],
        '000003': ['이름 3', '1980-11-22']
    }

    return  html.Div(
                className="modal-list",
                id="modal-artist",
                children=[
                    
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-list",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 목록", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-artist", className="btn-close-modal")
                                ]
                            ),
                            # 중앙: 검색창과 검색 버튼
                            html.Div(
                                className="modal-search",
                                children=[ 
                                    dcc.Input(type="text", placeholder="아티스트 ID를 입력해주세요.", id='search-input-artist', className="search-input"),
                                    html.Button("🔍", id='btn-search-artist', className="btn-search")
                                ] 
                            ),
                            # 새로운 중앙 컨텐츠: 인덱스와 리스트
                            html.Div(
                                className="modal-content",
                                children=[
                                    dash_table.DataTable(
                                        id='table-artist',
                                        columns=[{"name": i, "id": i} for i in ["아티스트ID", '이름', '생년월일']],
                                        page_current=0,
                                        page_size=10,
                                        page_action='custom',  # 서버 측 페이지네이션 활성화
                                        row_selectable='multi',
                                        selected_rows=[],
                                    ),
                                ]
                            ),                           
                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer",
                                children=[
                                    html.Button("아티스트 정보 추가", id="open-modal-btn-add-artist", className="btn-delete"),
                                    html.Button("상세 정보 보기", id="open-modal-btn-info-artist", className="btn-detail"),
                                    html.Button("불러오기", id='load-btn-artist', className="btn-load")
                                ]
                            ),

            
                            create_modal_artist_info(),
                            create_modal_artist_add()

                        ]
                    )
                ]
            )

# 모달2-1 - 아티스트 정보 모달창 
def create_modal_artist_info(): 
    return  html.Div(
                className="modal-info",
                id="modal-info-artist",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-info",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 정보", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-info-artist", className="btn-close-modal")
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
                                                    html.Div("이름", className="index-name-info"),
                                                    html.Div("생년월일", className="index-birth-info"),
                                                    html.Div("데뷔일", className="index-debut-info"),
                                                    html.Div("활동년대", className="index-activity-info"),
                                                    html.Div("유형", className="index-type-info"),
                                                    html.Div("성별", className="index-gender-info"),
                                                    html.Div("주장르", className="index-artist-genre-info"),
                                                    html.Div("소속사", className="index-agency-info"),
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                id='output-container-artist-info',
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

# 모달2-2 - 아티스트 추가 모달창 
def create_modal_artist_add(): 
    return  html.Div(
                className="modal-add",
                id="modal-add-artist",
                children=[
                    # 모달 컨텐츠
                    html.Div(
                        className="modal-body-add",
                        children=[
                            # 상단: 제목과 닫기 버튼
                            html.Div(
                                className="modal-header",
                                children=[
                                    html.Span("아티스트 추가", className="modal-title"),
                                    html.Button("X", id="close-modal-btn-add-artist", className="btn-close-modal")
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
                                                    html.Div("아티스트 ID", className="index-artist-id-info"),
                                                    html.Div("이름", className="index-name-info"),
                                                    html.Div("생년월일", className="index-birth-info"),
                                                    html.Div("데뷔일", className="index-debut-info"),
                                                    html.Div("활동년대", className="index-activity-info"),
                                                    html.Div("유형", className="index-type-info"),
                                                    html.Div("성별", className="index-gender-info"),
                                                    html.Div("주장르", className="index-artist-genre-info"),
                                                    html.Div("소속사", className="index-agency-info"),
                                                ]
                                            ),
                                            # 값 열
                                            html.Div(
                                                className="value-column",
                                                children=[
                                                    dcc.Input(id={'type': 'input-artist', 'index': 'id'}, className="input-artist-id", type="text"),
                                                    dcc.Input(id={'type': 'input-artist', 'index': 'name'}, className="input-name", type="text"),
                                                    dcc.Input(id={'type': 'input-artist', 'index': 'birth'}, className="input-birth", type="text"),
                                                    dcc.Input(id={'type': 'input-artist', 'index': 'debut'}, className="input-debut", type="text"),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-artist', 'index': 'activity'}, 
                                                        className="input-activity",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': '2020', 'value': '2020 년대'},
                                                            {'label': '2010-2020', 'value': '2010, 2020 년대'},
                                                            {'label': '2000-2020', 'value': '2000, 2010, 2020 년대'},
                                                            {'label': '1990-2020', 'value': '1990, 2000, 2010, 2020 년대'},
                                                            {'label': '1980-2020', 'value': '1980, 1990, 2000, 2010, 2020 년대'},
                                                            {'label': '1970-2020', 'value': '1970, 1980, 1990, 2000, 2010, 2020 년대'},
                                                            {'label': '1960-2020', 'value': '1960, 1970, 1980, 1990, 2000, 2010, 2020 년대'},
                                                            {'label': '2010', 'value': '2010 년대'},
                                                            {'label': '2000-2010', 'value': '2000, 2010 년대'},
                                                            {'label': '1980', 'value': '1980 년대'},
                                                            {'label': '1960-1970', 'value': '1960, 1970 년대'},
                                                        ],
                                                        value='2020 년대'  # 기본값
                                                    ),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-artist', 'index': 'type'}, 
                                                        className="input-type",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': '솔로', 'value': '솔로'},
                                                            {'label': '그룹', 'value': '그룹'},
                           
                                                        ],
                                                        value='솔로'  # 기본값
                                                    ),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-artist', 'index': 'gender'},
                                                        className="input-gender",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': '남성', 'value': '남성'},
                                                            {'label': '여성', 'value': '여성'},
                                                            {'label': '혼성', 'value': '혼성'},
                           
                                                        ],
                                                        value='남성'  # 기본값
                                                    ),
                                                    dcc.Dropdown(
                                                        id={'type': 'input-artist', 'index': 'genre'},
                                                        className="input-artist-genre",
                                                        options=[
                                                            {'label': '정보 없음', 'value': ''},
                                                            {'label': '댄스', 'value': '댄스'},
                                                            {'label': '발라드', 'value': '발라드'},
                                                            {'label': '랩/힙합', 'value': '랩/힙합'},
                                                            {'label': '클래식', 'value': '클래식'},
                                                            {'label': '록/메탈', 'value': '록/메탈'},
                                                            {'label': 'R&B/Soul', 'value': 'R&B/Soul'},
                                                            {'label': '국내드라마', 'value': '국내드라마'},
                                                            {'label': '인디음악', 'value': '인디음악'},
                                                            {'label': 'POP', 'value': 'POP'},
                                                            {'label': '포크/블루스', 'value': '포크/블루스'},
                                                            {'label': '일렉트로니카', 'value': '일렉트로니카'},
                                                            {'label': '성인가요/트로트', 'value': '성인가요/트로트'},
                                                            {'label': '국악', 'value': '국악'},
                                                            {'label': '국내영화', 'value': '국내영화'},
                                                            {'label': '키즈', 'value': '키즈'},
                                                            {'label': '재즈', 'value': '재즈'},
                                                            {'label': '월드뮤직', 'value': '월드뮤직'},
                                                            {'label': 'J-POP', 'value': 'J-POP'},
                                                            {'label': '국외드라마', 'value': '국외드라마'},
                                                        ],
                                                        value='발라드'  # 기본값
                                                    ),
                                                    dcc.Input(id={'type': 'input-artist', 'index': 'agency'}, className="input-agency", type="text"),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            
                            # 푸터: 삭제 버튼과 불러오기 버튼
                            html.Div(
                                className="modal-footer-add",
                                children=[
                                    html.Button("추가", id='add-btn-artist', className="btn-add"),
                                ]
                            ),
                        ]
                    )
                ]
            )