#app.py
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from PillIdentifier import PillIdentifier
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import tempfile
from bs4 import BeautifulSoup
from waitress import serve

app = Flask(__name__)

# Gemini API 설정
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_schema": {
        "type": "object",
        "properties": {
            "shape": {"type": "string"},
            "color": {"type": "string"},
            "imprint": {"type": "string"}
        },
        "required": ["shape", "color", "imprint"]
    },
    "response_mime_type": "application/json"
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/identify', methods=['POST'])
def identify_pill():
    if 'image' not in request.files:
        return jsonify({'error': '이미지가 업로드되지 않았습니다.'}), 400
    
    image = request.files['image']
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, image.filename)
    image.save(temp_path)
    
    driver = webdriver.Chrome()
    
    try:
        # Gemini로 이미지 분석
        image_file = genai.upload_file(temp_path, mime_type="image/jpeg")
        chat_session = model.start_chat()
        prompt_text = "Analyze the image of the pill and extract its shape, color, and any imprint. The pill's shape should be one of the following: ['circular', 'oval', 'semicircular', 'triangular', 'square', 'rhombus', 'oblong', 'octagon', 'hexagon', 'pentagon']. If the shape is unclear or doesn't fall into these categories, classify it as 'all'. The pill's color should be one of the following: ['white', 'yellow', 'orange', 'pink', 'red', 'brown', 'ygreen', 'green', 'bgreen', 'blue', 'navy', 'wine', 'purple', 'grey', 'black', 'transp']. 'transp' indicates that the pill is transparent. If the color is unclear or doesn't fall into these categories, classify it as 'all'. Leave the identifying markings field blank if they are unclear."
        
        response = chat_session.send_message([image_file, prompt_text])
        pill_info = json.loads(response.text)
        
        # Selenium으로 약품 검색
        identifier = PillIdentifier(driver)
        identifier.IdentifyPill(
            shape=pill_info.get('shape'),
            color=pill_info.get('color'),
            imprint1=pill_info.get('imprint', ''),
            imprint2=''
        )
        identifier.result_html = identifier.result_html.replace('<img', '<img class="pill-image"')
        
         # Parse the HTML
        soup = BeautifulSoup(identifier.result_html, 'html.parser')
        table = soup.find('table', id='idfytotal0')  

        if table:
            # Find the "출력담기" header
            header_cells = table.find_all('th')
            target_header = None 
            for cell in header_cells:
                if "출력담기" in cell.text:
                    target_header = cell
                    break 

            if target_header: 
                header_index = header_cells.index(target_header)

                table_body = table.find('tbody')

                for row in table_body.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > header_index:
                        target_cell = cells[header_index]
                        target_cell.decompose()
                target_header.decompose()
            cleaned_html = str(table)

        else:
            cleaned_html = identifier.result_html
        
        return jsonify({
            'pill_info': pill_info,
            'identified_pills': identifier.result,
            'result_html': cleaned_html
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        os.remove(temp_path)
        os.rmdir(temp_dir)
        driver.quit()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8085)