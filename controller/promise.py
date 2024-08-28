from flask import Blueprint, request, jsonify, send_file

import pdftotext
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

bp = Blueprint('promise', __name__, url_prefix='/promise')

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def getCandidates():
    with open('promises/candidates.json', 'r') as file:
        candidates = json.load(file)
    
    return candidates

def getRegion(name):
    candidates = getCandidates()

    for candidate in candidates['candidates']:
        if candidate['name'] == name:
            return candidate['region']

@bp.route('/candidates', methods=['GET'])
def candidates():
    candidates = getCandidates()
    candidateNames = []

    for candidate in candidates['candidates']:
        name = candidate['name']
        candidateNames.append(name)

    return candidateNames


@bp.route('/summary', methods=['POST'])
def summary():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400

    # code = data.code
    # region = data["region"]
    name = data["name"]
    region = getRegion(name)
    

    if os.path.isfile(f'promises/20240410_{region}_{name}_선거공보_summary.txt'): # 이미 요약된 파일이 존재하는 경우
        with open(f'promises/20240410_{region}_{name}_선거공보_summary.txt', 'r', encoding='utf-8') as file:
            result = file.read()
            return result

    # 요약된 파일이 없는 경우 openai로 요약한 후 txt 파일을 만든다.
    with open(f'promises/20240410_{region}_{name}_선거공보.pdf', 'rb') as f:
        pdf = pdftotext.PDF(f)
        text = "\n\n".join(pdf)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Korean documents."},
                {"role": "user", "content": f"다음 한글 텍스트 문서를 10문장으로 요약해줘:\n{text}"}
            ],
            max_tokens=4000
        )
        result = response.choices[0].message.content

        # 요약 파일 생성
        file = open(f'promises/20240410_{region}_{name}_선거공보_summary.txt', 'w')
        file.write(result)
        file.close()

        print(result)
    return result


@bp.route('/keywords', methods=['POST'])
def keywords():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # region = data["region"]
    name = data["name"]
    region = getRegion(name)

    if os.path.isfile(f'promises/20240410_{region}_{name}_선거공보_keywords.txt'): # 이미 키워드 파일이 존재하는 경우
        with open(f'promises/20240410_{region}_{name}_선거공보_keywords.txt', 'r', encoding='utf-8') as file:
            result = file.read()
            return result

    with open(f'promises/20240410_{region}_{name}_선거공보.pdf', 'rb') as f:
        pdf = pdftotext.PDF(f)
        text = "\n\n".join(pdf)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes keywords in Korean documents."},
                {"role": "user", "content": f'다음 한글 텍스트 문서의 키워드를 분석하고 {name}, {region}을 제외한 상위 키워드 10개를 다음과 같은 json 데이터를 반환해줘.' + '\n [{"text": "text1", "value": cnt1}, {"text": "text2", "value": cnt2}]' + '\n json 이외의 답변은 하지 말아줘. + 'f"\n{text}"}
            ],
            max_tokens=1000
        )
        result = response.choices[0].message.content

        # 키워드 파일 생성
        file = open(f'promises/20240410_{region}_{name}_선거공보_keywords.txt', 'w')
        file.write(result)
        file.close()

        print(result)
    return result

@bp.route('/detail', methods=['POST'])
def detail():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # code = data.code
    # region = data["region"]
    name = data["name"]
    region = getRegion(name)

    if os.path.isfile(f'promises/20240410_{region}_{name}_선거공보.pdf'):
        return send_file(f'promises/20240410_{region}_{name}_선거공보.pdf', as_attachment=True, download_name='file.pdf')

