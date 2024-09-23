import pandas as pd 
from datetime import datetime
import holidays
from tqdm import tqdm 


# ===== 기록일 시간 관련 함수 =====
def parse_date(df):
  df['date'] = pd.to_datetime(df['date'])

  # 분기, 요일 컬럼 추가
  df['year'] = df['date'].dt.year.astype('str') # 년
  df['month'] = df['date'].dt.month.astype('str') # 월
  df['day2'] = df['date'].dt.day.astype('str') # 일
  df['week_of_month'] = df['date'].apply(lambda x: (x.day - 1) // 7 + 1).astype('str')  # 주
  df['weekday'] = df['date'].dt.weekday.astype('str') # 요일
  df['quarter'] = df['date'].dt.quarter.astype('str') # 분기
  df['day_of_year'] = df['date'].dt.dayofyear.astype('str') # 일 (년 기준)
  df['week_of_year'] = df['date'].dt.isocalendar().week.astype('str') # 주 (년 기준)

  return df

def parse_holidays(df):
  df['date'] = pd.to_datetime(df['date'])

  kr_holidays = holidays.KR(years=range(2020, 2025))
  lst_holidays = [d.strftime('%Y-%m-%d') for d in kr_holidays.keys()]

  df['is_holiday'] = df['date'].apply(lambda x: 'yes' if x.strftime('%Y-%m-%d') in lst_holidays else "no")

  df[df['date']=='2023-12-25'][['date', 'is_holiday']]

  return df

def determine_vacation(row):
    date = pd.to_datetime(row['date'])

    # 기준 변수
    is_school_vacation = False
    is_univ_vacation = False

    # 방학 기간 판단
    if (date.month == 7 and 20 <= date.day <= 31) or (date.month == 8 and date.day <= 20) or \
       (date.month == 12 and date.day >= 30) or (date.month == 1) or (date.month == 2):
        is_school_vacation = True

    if (date.month == 6 and date.day >= 20) or (date.month in [7, 8]) or \
       (date.month == 9 and date.day <= 5) or (date.month == 12 and date.day >= 20) or \
       (date.month == 1) or (date.month == 2) or (date.month == 3 and date.day <= 5):
        is_univ_vacation = True

    # 조건에 따라 결과 반환
    if is_school_vacation and is_univ_vacation:
        return 'each'
    elif is_school_vacation:
        return 'school'
    elif is_univ_vacation:
        return 'univ'
    else:
        return 'no'
    
# 시험 기간 필터링 함수
def determine_exam(row):
    date = pd.to_datetime(row['date'])

    # 기준 변수
    is_school_exam = False
    is_univ_exam = False

    # 시험 기간 판단
    if (date.month == 4 and 20 <= date.day <= 30) or (date.month == 6 and 20 <= date.day <= 30) or \
       (date.month == 7 and date.day <= 10) or (date.month == 9 and 20 <= date.day <= 30) or \
       (date.month == 10 and date.day <= 10) or (date.month == 11 and 20 <= date.day <= 30) or \
       (date.month == 12 and date.day <= 10):
        is_school_exam = True

    if (date.month == 4 and 15 <= date.day <= 30) or (date.month == 6 and 10 <= date.day <= 25) or \
       (date.month == 10 and 15 <= date.day <= 30) or (date.month == 12 and 10 <= date.day <= 23):
        is_univ_exam = True

    # 조건에 따라 결과 반환
    if is_school_exam and is_univ_exam:
        return 'each'
    elif is_school_exam:
        return 'school'
    elif is_univ_exam:
        return 'univ'
    else:
        return 'no'



# 'olympic' 또는 'no' 값을 지정하는 함수
def classify_period(date):
    # 올림픽 기간 정의
    olympic_periods = [
        (datetime(2021, 7, 23), datetime(2021, 8, 8)),  # 2021 도쿄 여름 올림픽
        (datetime(2022, 2, 4), datetime(2022, 2, 20)),  # 2022 베이징 겨울 올림픽
        (datetime(2024, 7, 26), datetime(2024, 8, 11))   # 2024 파리 여름 올림픽
    ]
    for start_date, end_date in olympic_periods:
        if start_date <= date <= end_date:
            return 'yes'
    return 'no'


def parse_season(x):
  if x in ['3', '4', '5']:
    return 'spring'

  elif x in ['6', '7', '8']:
    return 'summer'

  elif x in ['9', '10', '11']:
    return 'fall'

  elif x in ['12', '1', '2']:
    return 'winter'
  

# ===== 발매일 시간 관련 함수 =====
def parse_release(df):
  df['release'] = pd.to_datetime(df['release'])

  df['release_year'] = df['release'].dt.year.astype("str") # 년
  df['release_month'] = df['release'].dt.month.astype("str") # 월
  df['release_day'] = df['release'].dt.day.astype("str") # 일
  df['release_weekday'] = df['release'].dt.weekday.astype("str") # 요일
  df['release_quarter'] = df['release'].dt.quarter.astype("str") # 분기

  return df


  
# ===== 가수 생일, 발매일 관련 함수 =====
def parse_birth_year(df): 
    df['birth'] = pd.to_datetime(df['birth'], errors='coerce')
    df['birth_year'] = df['birth'].dt.year.astype('str')

    return df


def parse_debut(df):
  df['debut'] = pd.to_datetime(df['debut'], errors='coerce')

  df['debut_year'] = df['debut'].dt.year.astype("str") # 년
  df['debut_month'] = df['debut'].dt.month.astype("str") # 월
  df['debut_day'] = df['debut'].dt.day.astype("str") # 일

  return df

def parse_age(df):  
    return df.apply(lambda row: int(row['release_year']) - int(row['birth_year']) if row['birth_year'] != 'nan' else 0, axis=1)


# ===== 유니크 값 계산 함수 =====
def get_unique(df, var, new_var):
  # streaming_u 초기화
  df[new_var] = 0

  # 최적화된 diff 계산 함수
  def calculate_diff(group):
      group[new_var] = group[var].diff().fillna(group[var])
      return group

  # groupby와 apply를 사용하여 최적화된 diff 계산
  return df.groupby(["song_id", 'artist_id']).apply(calculate_diff).reset_index(drop=True)


# ===== 컬럼 추가 함수 =====
def add_camulative_avg(df):
    for col in ['activaeUser']:
        df.loc[:, f'{col}_camulative_avg'] = df[f'{col}'].expanding().mean().shift(1).fillna(0)
    return df

def add_diff_camulative_avg(df):
  for col in ['activaeUser']:
    df[f'{col}_diff_camulative_avg'] = df[f'{col}'] - df[f'{col}_camulative_avg']

  return df

def add_column(df):
  df = add_camulative_avg(df)
  df = add_diff_camulative_avg(df)

  return df


# 라벨 인코더 적용
def label_encoding(df):
    import joblib
    # import sklearn
    # from sklearn.preprocessing import LabelEncoder
    label_encoders = joblib.load('models/label_encoder.pkl')
    for column, encoder in label_encoders.items():
        df[column] = encoder.transform(df[column])
    
    return df 