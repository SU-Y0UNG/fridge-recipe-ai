"""
🥗 냉장고 파먹기 - 재료 기반 레시피 추천 서비스
Flask 메인 애플리케이션
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
from utils.detector import FoodDetector
from utils.recommender import RecipeRecommender

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

detector = FoodDetector()
recommender = RecipeRecommender()

# 선택 가능한 전체 재료 목록
ALL_INGREDIENTS = [
    '사과', '살구', '아스파라거스', '아보카도', '바나나', '파프리카',
    '블랙베리', '블루베리', '브로콜리', '멜론', '당근', '콜리플라워',
    '셀러리', '체리', '병아리콩', '고추', '코코넛', '옥수수',
    '오이', '대추', '가지', '무화과', '마늘', '생강', '포도',
    '키위', '레몬', '상추', '라임', '귤', '버섯', '양파',
    '오렌지', '파파야', '복숭아', '배', '감', '파인애플',
    '감자', '호박', '무', '라즈베리', '딸기', '고구마',
    '토마토', '순무', '수박', '애호박', '대파',
    # 추가 한국 식재료
    '계란', '두부', '김치', '돼지고기', '닭고기', '소고기',
    '쌀', '시금치', '배추', '콩나물', '어묵', '라면',
    '참치캔', '햄', '치즈', '우유', '양배추',
]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ingredients = detector.detect(filepath)

    return render_template('result.html',
                           ingredients=ingredients,
                           image_path=filepath,
                           all_ingredients=ALL_INGREDIENTS)


@app.route('/recommend', methods=['POST'])
def recommend():
    selected = request.form.getlist('ingredients')
    manual = request.form.getlist('manual_ingredients')
    all_selected = list(set(selected + manual))

    if not all_selected:
        return redirect(url_for('index'))

    cuisine = request.form.get('cuisine') or None
    recipes = recommender.recommend(all_selected, cuisine=cuisine)
    all_recipes = recommender.recommend(all_selected, top_n=100)
    cuisines = list(set(r['cuisine'] for r in all_recipes if r.get('cuisine')))

    return render_template('recommend.html',
                           ingredients=all_selected,
                           recipes=recipes,
                           cuisines=sorted(cuisines),
                           selected_cuisine=cuisine or '전체')


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = recommender.get_recipe(recipe_id)
    if recipe is None:
        return redirect(url_for('index'))

    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/popular')
def popular():
    """인기 레시피 페이지"""
    recipes = recommender.get_popular(top_n=20)
    return render_template('popular.html', recipes=recipes)


@app.route('/api/ingredients/search')
def search_ingredients():
    """재료 검색 API"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'results': []})

    results = [i for i in ALL_INGREDIENTS if query in i]
    return jsonify({'results': results[:10]})


@app.route('/api/detect', methods=['POST'])
def api_detect():
    if 'image' not in request.files:
        return jsonify({'error': '이미지를 업로드해주세요'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': '허용되지 않는 파일 형식입니다'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ingredients = detector.detect(filepath)
    return jsonify({'ingredients': ingredients})


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({'error': '재료 목록을 전달해주세요'}), 400

    recipes = recommender.recommend(data['ingredients'])
    return jsonify({'recipes': recipes})


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)