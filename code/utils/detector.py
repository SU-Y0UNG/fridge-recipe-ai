"""
YOLOv8 기반 식재료 감지 모듈
- 학습된 모델이 있으면 실제 추론
- 없으면 시뮬레이션 모드로 동작 (개발/테스트용)
- 영어 클래스명 → 한국어 자동 변환
"""
import os
import random

# YOLOv8 모델 경로
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'best.pt')

# 영어 → 한국어 변환 맵 (LVIS 데이터셋 클래스 기준)
NAME_MAP = {
    'apple': '사과',
    'apricot': '살구',
    'asparagus': '아스파라거스',
    'avocado': '아보카도',
    'banana': '바나나',
    'bell pepper': '파프리카',
    'blackberry': '블랙베리',
    'blueberry': '블루베리',
    'broccoli': '브로콜리',
    'cantaloupe': '멜론',
    'carrot': '당근',
    'cauliflower': '콜리플라워',
    'celery': '셀러리',
    'cherry': '체리',
    'chickpea': '병아리콩',
    'chili pepper': '고추',
    'clementine': '클레멘타인',
    'coconut': '코코넛',
    'corn': '옥수수',
    'cucumber': '오이',
    'date': '대추',
    'eggplant': '가지',
    'fig': '무화과',
    'garlic': '마늘',
    'ginger': '생강',
    'grape': '포도',
    'grapes': '포도',
    'green bean': '녹두',
    'green onion': '대파',
    'kiwi': '키위',
    'kiwi fruit': '키위',
    'lemon': '레몬',
    'lettuce': '상추',
    'lime': '라임',
    'mandarin orange': '귤',
    'melon': '멜론',
    'mushroom': '버섯',
    'onion': '양파',
    'orange': '오렌지',
    'papaya': '파파야',
    'peach': '복숭아',
    'pear': '배',
    'persimmon': '감',
    'pickle': '피클',
    'pineapple': '파인애플',
    'potato': '감자',
    'pumpkin': '호박',
    'radish': '무',
    'raspberry': '라즈베리',
    'strawberry': '딸기',
    'sweet potato': '고구마',
    'tomato': '토마토',
    'turnip': '순무',
    'watermelon': '수박',
    'zucchini': '애호박',
    # 기존 15종 데이터셋 호환
    'capsicum': '파프리카',
    'chilli': '고추',
    'jalepeno': '할라피뇨',
    'both': '혼합',
    'orange/orange fruit': '오렌지',
}

# 시뮬레이션용 식재료 목록 (한국어)
SIMULATED_INGREDIENTS = [
    '사과', '바나나', '당근', '감자', '토마토',
    '양파', '마늘', '브로콜리', '오이', '가지',
    '레몬', '파프리카', '고추', '버섯', '호박',
    '고구마', '포도', '대파', '상추', '옥수수',
]


class FoodDetector:
    def __init__(self):
        """모델 로드 (없으면 시뮬레이션 모드)"""
        self.model = None
        self.simulation_mode = True

        if os.path.exists(MODEL_PATH):
            try:
                from ultralytics import YOLO
                self.model = YOLO(MODEL_PATH)
                self.simulation_mode = False
                print("[INFO] YOLOv8 모델 로드 완료")
            except Exception as e:
                print(f"[WARN] 모델 로드 실패, 시뮬레이션 모드: {e}")
        else:
            print("[INFO] 모델 파일 없음 → 시뮬레이션 모드로 실행")

    def detect(self, image_path: str) -> list:
        """
        이미지에서 식재료 감지

        Args:
            image_path: 이미지 파일 경로

        Returns:
            [{'name': '당근', 'confidence': 95.2}, ...] 형태의 리스트
        """
        if self.simulation_mode:
            return self._simulate_detection()
        else:
            return self._real_detection(image_path)

    def _real_detection(self, image_path: str) -> list:
        """실제 YOLOv8 추론"""
        results = self.model(image_path)
        ingredients = []
        seen = set()

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                name_en = self.model.names[class_id]

                # 영어 → 한국어 변환
                name_ko = NAME_MAP.get(name_en, name_en)

                if confidence > 0.25 and name_ko not in seen:
                    seen.add(name_ko)
                    ingredients.append({
                        'name': name_ko,
                        'confidence': round(confidence * 100, 1)
                    })

        # 신뢰도 높은 순 정렬
        ingredients.sort(key=lambda x: x['confidence'], reverse=True)
        return ingredients

    def _simulate_detection(self) -> list:
        """시뮬레이션 모드 - 랜덤 재료 생성 (개발용)"""
        count = random.randint(3, 7)
        selected = random.sample(SIMULATED_INGREDIENTS, count)

        ingredients = []
        for name in selected:
            confidence = round(random.uniform(70, 99), 1)
            ingredients.append({
                'name': name,
                'confidence': confidence
            })

        ingredients.sort(key=lambda x: x['confidence'], reverse=True)
        return ingredients