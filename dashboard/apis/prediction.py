from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..database import records_collection, songs_collection, artists_collection
from bson import ObjectId
import json
from datetime import datetime
import pandas as pd 
from preprocessing import *
import joblib
from tabulate import tabulate
# from xgboost import XGBRegressor

prediction_ns = Namespace("Prediction")

X_cols = ["artist_id", 'day',
          'activaeUser', 'activaeUser_camulative_avg', 'activaeUser_diff_camulative_avg',
        'genre', 'album_type', 'artist_cnt', 
          'avg_prior_activae', 'prior_release_count', 'prior_release_gap',
      'birth_year', 'activity_year', 'activity_type', 'gender',
      'agency', 'artist_genre_main', 'year', 'month', 'day2', 'week_of_month',
      'weekday', 'quarter', 'day_of_year', 'week_of_year', 'is_holiday',
      'is_vacation', 'is_exam', 'season', 'release_year', 'release_month',
      'release_day', 'release_weekday', 'release_quarter', 'release_season',
      'is_olympic', 'debut_year', 'debut_month', 'debut_day', 'release_age']

y_col = ['day', 'activaeUser']

@prediction_ns.route('')
class Predictions(Resource):
    def post(self):

        ##### 6. 응답값 전송 
        try:
            # song_id, artist_id, 음원 성적 요청 
            ##### 1. 클라이언트가 보낸 데이터 받아오기 
            data = request.get_json()

            # 데이터 유효성 검증: song_id, activaeUsers, streamings, listeners 데이터 받아와야 함 
            required_fields = ['song_id', "activaeUsers"]
            if not all(field in data for field in required_fields):
                return {'message': 'Invalid data'}, 400
            
            song_id = data.get("song_id")
            activaeUsers = data.get("activaeUsers")

            ##### 2. DB에서 데이터 불러오기 (song, artist)
            # song 
            song = songs_collection.find_one({"song_id": int(song_id)}, {"_id": 0})
            
            # artist: song 데이터의 artist_id를 활용하여 불러온다. 
            artist_ids = song['artist_id']

            artists = artists_collection.find({"artist_id": {"$in": artist_ids}}, {"_id": 0})

            ##### 3. 데이터 전처리 (입력 데이터에 맞는 계산)
            # song 
            df_song = pd.DataFrame(song)  
            df_song = df_song.drop(columns=['artist_id', 'test'])

            # release => release_year release_month release_day release_weekday release_quarter release_season
            # song도 여러개구나.....................
            df_song = parse_release(df_song)
            df_song['release_season'] = df_song['release_month'].map(parse_season)
            
            # artist 
            dic_artist = {}
            for artist in artists: 
                for k, v in artist.items(): 
                    if k not in dic_artist: 
                        dic_artist[k] = [] 
                    dic_artist[k].append(v)

            df_artist = pd.DataFrame(dic_artist) 

            # birth => birth_year
            df_artist = parse_birth_year(df_artist)
            # debut => debut_year debut_month debut_day
            df_artist = parse_debut(df_artist)

            # record 
            # date => 
            # year month day2 week_of_month weekday quarter day_of_year week_of_year 
            # is_holiday is_vacation is_exam season is_olympic
            # season

            df_record = pd.DataFrame({
                'activaeUser': activaeUsers + [0] * (30-len(activaeUsers)),
                'date': pd.date_range(start=song['release'], periods=30),
                'day': list(range(1, 31))
            })

            df_record = parse_date(df_record)
            df_record = parse_holidays(df_record)
            df_record['is_vacation'] = df_record.apply(determine_vacation, axis=1)
            df_record['is_exam'] = df_record.apply(determine_exam, axis=1)
            df_record['is_olympic'] = df_record['date'].apply(classify_period)
            df_record['season'] = df_record['month'].map(parse_season)
            
            # song + record 
            # df_song_repeat = pd.concat([df_song]*len(df_record), ignore_index=True)
            # df_merged = pd.concat([df_song_repeat, df_record], axis=1)

            ##### 4. 모델 불러오기
            xgb  = joblib.load('models/xgb_0911.joblib')

            ##### 5. 모델 예측 => artist 별로 예측한다. 
            # 아티스트 1, 아티스트2, ..., 평균 
            # ⭐ 추가 작업
                # 연쇄 예측: 예측일 부터 30일까지 예측 수행 
                # 아티스트 2명일 때 예측: 기본적으로는 평균을 사용하고, 추가적으로 아티스트 별 버튼, 평균 버튼 생성 
            y_preds = [] 
            df_y_pred_tmp = pd.DataFrame()  
            # for _, artist in df_artist.iterrows():
            for (_, artist), (_, song) in zip(df_song.iterrows(), df_artist.iterrows()):
                df_song_repeat = pd.concat([song.to_frame().T]*len(df_record), ignore_index=True)
                df_merged = pd.concat([df_song_repeat, df_record], axis=1)

                df_artist_repeat = pd.concat([artist.to_frame().T] * len(df_record), ignore_index=True)
                df_merged_final = pd.concat([df_merged, df_artist_repeat], axis=1)

                df_merged_final["release_age"] = parse_age(df_merged_final)                
                df_merged_final = label_encoding(df_merged_final)
                df_merged_final = add_column(df_merged_final)
                 
                # df_X: 1일 ~ 30일 (입력값) 
                # df_y_pred:1일 ~ 31일 (출력값 저장) 
                df_X = df_merged_final[X_cols] # X (1일 ~ 30일 실제값) 
                df_y_pred = df_merged_final[y_col] # y, y_pred (2일 ~ 31일 예측값) 
                df_y_pred = pd.concat([df_y_pred, pd.DataFrame({"day": [31], "activaeUser": 0})]) 
                df_y_pred['activaeUser_pred'] = df_y_pred['activaeUser'] 
                df_y_pred = df_y_pred.reset_index(drop=True) 

                for i in range(30):

                    if i >= len(activaeUsers): # 실제값이 없는 데이터 부터는 예측값 사용하여 예측 
                        df_X.loc[i, 'activaeUser'] = df_y_pred.iloc[i]['activaeUser_pred']

                    df_X_1 = df_X.iloc[:(i+1)] # 1일 부터 30일까지 순차적으로 예측함  
                    df_X_1 = add_column(df_X_1)

                    df_y_pred.loc[i+1, 'activaeUser_pred'] = xgb.predict(df_X_1.iloc[-1].values.reshape(1, -1))
                
                # print(tabulate(df_y_pred, headers='keys', tablefmt='fancy_outline'))
                y_preds.append(df_y_pred['activaeUser_pred'].values.tolist())
                if len(df_y_pred_tmp) == 0: 
                    df_y_pred_tmp = df_y_pred.copy()
                else: 
                    df_y_pred_tmp = (df_y_pred_tmp + df_y_pred) / 2 

            df_y_pred_tmp['오차(%)'] = round(abs((df_y_pred_tmp['activaeUser'] - df_y_pred_tmp['activaeUser_pred']) / df_y_pred_tmp['activaeUser']) * 100, 2)
            df_y_pred_tmp['오차(%)'] = df_y_pred_tmp['오차(%)'].apply(lambda x: f'{x}%').replace("inf%", "")
            df_y_pred_tmp['activaeUser_pred'] = round(df_y_pred_tmp['activaeUser_pred'])
            table_dict = df_y_pred_tmp.to_dict('records')
            table_cols = [{"name": i, "id": i} for i in df_y_pred_tmp.columns]

            return {
                "pred_by_artist": {
                                    artist_id: y_pred
                                    for artist_id, y_pred in zip(artist_ids, y_preds)
                                   },
                "table_data": [table_dict, table_cols] 
            }, 200
        
        except Exception as e:
            # 예외 처리
            return {"message": f"An error occurred: {str(e)}"}, 500
        