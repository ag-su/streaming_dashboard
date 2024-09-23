from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..database import artists_collection

artist_ns = Namespace("Artist")

@artist_ns.route('')
class Artists(Resource): 
    def get(self): 
        # 쿼리 파라미터에서 페이지 번호와 페이지 크기 가져오기 
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # 추가된 쿼리 파라미터
        artist_id = request.args.get('artist_id', default=None, type=int)
        name = request.args.get('name', default=None, type=str)

        # 쿼리 필터링
        query = {}
        if artist_id:
            query['artist_id'] = int(artist_id)
        if name:
            query['name'] = {'$regex': name, '$options': 'i'}
        
        # 데이터 가져오기
        artists = list(artists_collection.find(query).skip((page - 1) * per_page).limit(per_page))
        total = artists_collection.count_documents(query)

        # 결과를 JSON으로 변환
        result = {
            'total': total,
            'current_page': page,
            'per_page': per_page,
            'df_artists': [{"아티스트ID": artist['artist_id'], "이름": artist['name'], '생년월일': artist['birth']} for artist in artists]
        }

        return jsonify(result)

    def post(self): 
        # 클라이언트가 보낸 JSON 데이터를 가져오기
        data = request.get_json()

        # 데이터 유효성 검증
        required_fields = ['artist_id', 'name', 'birth', 'debut', 'activity_year', 'activity_type', 'gender', 'artist_genre_main', 'agency']
        if not all(field in data for field in required_fields):
            return {'message': 'Invalid data'}, 400

        # 데이터베이스에 추가할 데이터 구성
        new_artist = {
            'artist_id': int(data.get('artist_id')),
            'name': data.get('name'),
            'birth': data.get('birth'),
            'debut': data.get('debut'),
            'activity_year': data.get('activity_year'),
            'activity_type': data.get('activity_type'),
            'gender': data.get('gender'),
            'artist_genre_main': data.get('artist_genre_main'),
            'agency': data.get('agency')
        }

        # 데이터베이스에 추가
        result = artists_collection.insert_one(new_artist)

        # 추가된 데이터 확인
        if result.acknowledged:
            return {'message': 'Artist added successfully', 'artist': new_artist}, 201
        else:
            return {'message': 'Failed to add artist'}, 500


@artist_ns.route('/<int:artist_id>')
class ArtistSimple(Resource): 
    def get(self, artist_id): # artist_id를 URL 에서 받아온다.  
        artist = artists_collection.find_one({"artist_id": artist_id}) # artist_id로 DB에서 조회한다. 

        if artist is None: 
            return {"message": "Artist not found"}, 404
        
        return {
            "name": artist["name"],
            "birth": artist["birth"],
            "debut": artist["debut"],
            "activity_year": artist["activity_year"],
            "activity_type": artist["activity_type"],
            "gender": artist["gender"],
            "agency": artist["agency"],
            "artist_genre_main": artist["artist_genre_main"]
        }, 200
    

