from flask import Flask, render_template, request, jsonify  
import dash
from dashboard.component import load_component
from callbacks import *
import os 
from dashboard import create_app


# ============================== back ============================== 
app = create_app()

# ========== 기본 라우터 ==========
# 인덱스 페이지
@app.route("/") 
def index(): 
    return render_template('index.html')

# ===== front ===== 
# Dash 애플리케이션 인스턴스 생성
dash_app1 = dash.Dash(__name__, server=app, url_base_pathname='/dashapp1/')

# 애플리케이션 레이아웃 
dash_app1.layout = load_component() 

# 콜백 
register_callbacks(dash_app1)
    

# 서버 실행
if __name__ == '__main__':
    app.debug = True 
    app.run() 
