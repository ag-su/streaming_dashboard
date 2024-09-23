from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..database import records_collection, songs_collection, artists_collection
from bson import ObjectId
import json
from datetime import datetime

record_ns = Namespace("Record")


def serialize_record(record):
    """
    Convert MongoDB ObjectId to string for JSON serialization.
    """
    if isinstance(record, dict):
        for key, value in record.items():
            if isinstance(value, ObjectId):
                record[key] = str(value)
            elif isinstance(value, dict):
                serialize_record(value)
            elif isinstance(value, list):
                record[key] = [serialize_record(v) if isinstance(v, dict) else v for v in value]
    return record


@record_ns.route('')
class Records(Resource):
    def get(self): 
        # 쿼리 파라미터에서 페이지 번호와 페이지 크기 가져오기 
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # 추가된 쿼리 파라미터
        song_id = request.args.get('song_id', default=None, type=int)
        subject = request.args.get('subject', default=None, type=str)

        # 쿼리 필터링
        query = {}
        if song_id:
            query['song_id'] = int(song_id)
        if subject:
            query['subject'] = {'$regex': subject, '$options': 'i'}
        
        # 데이터 가져오기
        records = list(records_collection.find(query).skip((page - 1) * per_page).limit(per_page))

        total = records_collection.count_documents(query)
        
        # 문자열을 datetime 객체로 변환
        def format_date(created_at):
            created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f")
            return created_at_dt.strftime("%Y-%m-%d %H:%M:%S")

        # 결과를 JSON으로 변환
        result = {
            'total': total,
            'current_page': page,
            'per_page': per_page,
            'df_records': [{"곡ID": record['song_id'], "제목": record['subject'], '저장날짜': format_date(record['created_at'])} for record in records]
                            }

        return jsonify(result)


    def post(self): 
        # 클라이언트가 보낸 JSON 데이터를 가져오기
        data = request.get_json()

        # 데이터 유효성 검증
        required_fields = ['song_id', 'subject', 'activaeUsers']
        if not all(field in data for field in required_fields):
            return {'message': 'Invalid data'}, 400

        # 데이터베이스에 추가할 데이터 구성
        new_record = {
            'song_id': int(data.get('song_id')),
            'subject': data.get('subject'),
            'activaeUsers': data.get('activaeUsers'),
            'created_at': datetime.now().isoformat()
        }

        try:
            result = records_collection.update_one(
                {'song_id': int(data.get("song_id"))},  # 조건: song_id가 일치하는 문서
                {'$set': new_record},               # 업데이트할 데이터
                upsert=True)
                
            # 업데이트 결과 확인
            if result.modified_count > 0 or result.upserted_id:
                serialized_record = serialize_record(new_record)
                return {'message': 'Song added/updated successfully', 'song': serialized_record}, 200
            else:
                return {'message': 'Failed to add/update Song'}, 500

        except Exception as e:
            # 오류 발생 시 예외 처리
            return {'message': f'Error: {str(e)}'}, 500
        


@record_ns.route('/<int:song_id>')
class RecordSimple(Resource): 
    def get(self, song_id): 
        try:
            # record 조회
            record = records_collection.find_one({"song_id": song_id}, {"_id":0}) 
            if record is None:
                return {"message": "Record not found"}, 404

            # song 조회
            song = songs_collection.find_one({'song_id': song_id}, {"artist_id": 1, '_id':0})
            if song is None:
                return {"message": "Song not found"}, 404
            
            # artist_ids 리스트로 변환
            artist_ids = song.get('artist_id', [])
            if not isinstance(artist_ids, list):
                artist_ids = [artist_ids]
            
            # 아티스트 조회
            artists_cursor = artists_collection.find(
                {"artist_id": {"$in": list(map(int, artist_ids))}}, 
                {"artist_id": 1, 'name': 1, '_id':0}
            )
            artists_list = list(artists_cursor)
            
            # 아티스트 데이터 확인
            if not artists_list:
                return {"message": "Artists not found"}, 404
            
            # 아티스트 데이터 직렬화
            serialized_artists = serialize_record(artists_list)



            return {
                "activaeUsers": record["activaeUsers"],
                "artists": serialized_artists
            }, 200
        
        except Exception as e:
            # 예외 처리
            return {"message": f"An error occurred: {str(e)}"}, 500
