### running process 
1. 가상 환경 셋팅
```
$ cd {your directory}
$ python3 -m venv ./{your venv name}
$ source {your venv name}/bin/activate # mac os
$ {your venv name}\Scripts\activate # window 
```
   
2. download packages
```python
$ pip install -r requirements.txt
```

3. mf_dashboard/models 안에 xgb, encoder 모델 파일 넣기   

4. mf_dashboard/.env 파일 작성

5. 앱 실행
```
$ python app.py
``` 
 
