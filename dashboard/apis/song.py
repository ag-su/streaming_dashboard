from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..database import songs_collection, artists_collection, ranked_songs_collection, get_collection_by_release
from datetime import datetime

song_ns = Namespace("Song")

@song_ns.route('')
class Songs(Resource): 
    def get(self): 
        # 쿼리 파라미터에서 페이지 번호와 페이지 크기 가져오기 
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # 추가된 쿼리 파라미터
        song_id = request.args.get('song_id', default=None, type=int)
        subject = request.args.get('subject', default=None, type=str)

        # 쿼리 필터링
        query = {'test': True}
        if song_id:
            query['song_id'] = int(song_id)
        if subject:
            query['subject'] = {'$regex': subject, '$options': 'i'}
        
        # 데이터 가져오기
        songs = list(songs_collection.find(query).skip((page - 1) * per_page).limit(per_page))
        

        total = songs_collection.count_documents(query)

        # 결과를 JSON으로 변환
        result = {
            'total': total,
            'current_page': page,
            'per_page': per_page,
            'df_songs': [{"곡ID": song['song_id'], "제목": song['subject'], '발매일': song['release']} for song in songs]
        }

        return jsonify(result)

    def post(self): 
        # 클라이언트가 보낸 JSON 데이터를 가져오기
        data = request.get_json()

        # 데이터 유효성 검증
        required_fields = ['song_id', 'subject', 'release', 'genre', 'artist_id']
        if not all(field in data for field in required_fields):
            return {'message': 'Invalid data'}, 400

        lst_artist_ids = list(map(int, data.get('artist_id').split(",")))

        dic_col2lst_total = {"prior_activae":[], 'prior_release_count':[], "prior_release_gap":[]} 
        # MelonChart-RankedSongs:: Artist에 해당하는 Id, Release 추출 
        for idx, artist_id in enumerate(lst_artist_ids):
            results = ranked_songs_collection.find({
                "Artists": {
                    "$elemMatch": {
                        "_id": artist_id  # 배열 내부에 있는 필드 조건
                    }
                }
            }, {'Release': 1, "Id": 1})

            # SongDataDB:: 발매일 활용 컬렉션 검색 => Mid 검색 => 첫날 성적/정보 추출
            dic_col2lst = {"prior_activae":[], 'prior_release_count':0, "prior_release_gap":[]} 
            for result in results: 
                prev_release, prev_song_id = result['Release'], result['Id']
                song_data_collection = get_collection_by_release(prev_release)
                prev_song = song_data_collection.find_one({
                                                            "$or": [
                                                                {"mid": prev_song_id},  # "mid" 컬럼이 특정 값을 가지는 경우
                                                                {"Mid": prev_song_id}   # "Mid" 컬럼이 특정 값을 가지는 경우
                                                            ]
                                                        }, {"data":1})
                
                if len(prev_song['data']) == 0: 
                    continue
                
                if prev_release == data.get('release'):
                    continue

                d = prev_song['data']["0"]
                dic_col2lst["prior_activae"].append(d['activaeUser'])
                dic_col2lst["prior_release_count"] += 1
                dic_col2lst["prior_release_gap"].append(prev_release)
            

            dic_col2lst_total['prior_activae'].append(sum( dic_col2lst["prior_activae"])/dic_col2lst["prior_release_count"] )
            dic_col2lst_total['prior_release_count'].append(dic_col2lst["prior_release_count"])

            recent = max(dic_col2lst["prior_release_gap"])
            # 문자열을 datetime 객체로 변환
            date1 = datetime.strptime(recent, "%Y-%m-%d")
            date2 = datetime.strptime(data.get('release'), "%Y-%m-%d")
           
            dic_col2lst_total["prior_release_gap"].append((date2 - date1).days)

        # 데이터베이스에 추가할 데이터 구성
        new_song = {
            'song_id': int(data.get('song_id')),
            'subject': data.get('subject'),
            'release': data.get('release'),
            'genre': data.get('genre'),
            'album_type': data.get("album_type"),
            'artist_id': lst_artist_ids,
            'artist_cnt': len(lst_artist_ids),
            'avg_prior_activae': dic_col2lst_total['prior_activae'], # 이전 첫날 스트리밍 수 평균 
            'prior_release_count': dic_col2lst_total['prior_release_count'], # 이전 곡 발매 개수 
            'prior_release_gap': dic_col2lst_total['prior_release_gap'], # 최근 발매일과 차이 
            'test': True
        }

        # 데이터베이스에 추가
        result = songs_collection.insert_one(new_song)

        # 추가된 데이터 확인
        if result.acknowledged:
            return {'message': 'Song added successfully', 'song': new_song}, 201
        else:
            return {'message': 'Failed to add Song'}, 500


@song_ns.route('/<int:song_id>')
class SongSimple(Resource): 
    def get(self, song_id): # artist_id를 URL 에서 받아온다.  
        song = songs_collection.find_one({"song_id": song_id}) # artist_id로 DB에서 조회한다. 
        artist_ids = song['artist_id']

        artists = artists_collection.find({"artist_id": {"$in": artist_ids}})

        name = ', '.join([artist['name'] for artist in artists])

        if song is None: 
            return {"message": "Artist not found"}, 404
        
        return {
            "song_id": song['song_id'],
            "subject": song["subject"],
            "release": song["release"],
            "genre": song["genre"],
            "album_type": song['album_type'],
            "artist_name": name
        }, 200