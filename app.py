from flask import Flask, render_template, request, jsonify
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/identify', methods=['POST'])
def identify_pill():
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다.'}), 400
    
    return jsonify({
        'pill_info': {
            'shape': '원형',
            'color': '흰색',
            'imprint': '테스트'
        },
        'identified_pills': ['테스트 약품'],
        'result_html': '<table id="idfytotal0"><tr><th>테스트</th></tr><tr><td>테스트 데이터</td></tr></table>'
    })

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8085)