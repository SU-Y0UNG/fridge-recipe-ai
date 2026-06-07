# 🥗 냉장고 파먹기 — AI 식재료 인식 & 레시피 추천 웹 서비스

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/YOLOv8-00FFFF?style=flat&logo=yolo&logoColor=black"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat&logo=googlecolab&logoColor=white"/>
</p>

<p align="center">
  냉장고 속 식재료 사진을 업로드하면 YOLOv8이 재료를 자동 인식하고,<br/>
  보유 재료 기반으로 만들 수 있는 레시피를 일치율 순으로 추천해주는 웹 서비스입니다.
</p>

---

## 📌 프로젝트 개요

냉장고에 남은 재료로 무엇을 만들 수 있을지 고민하는 상황에서, 사진 한 장으로 재료를 인식하고 적합한 레시피를 추천받을 수 있도록 개발한 웹 서비스입니다.

YOLOv8 객체 인식 모델을 LVIS Fruits and Vegetables 데이터셋(8,200장, 63클래스)으로 Google Colab GPU 환경에서 학습시켰으며, 신뢰도 임계값을 0.25로 조정하여 다양한 촬영 환경에서도 안정적인 인식률을 확보하였습니다. 인식된 영어 클래스명은 NAME_MAP 매핑을 통해 한국어로 자동 변환됩니다.

레시피 데이터베이스에는 한식·양식·중식·일식 60개 레시피가 등록되어 있으며, 보유 재료와의 일치율을 계산하여 최적의 레시피를 추천합니다. 요리 종류별 탭 필터링, 조회수 추적, 수동 식재료 검색 기능을 함께 제공하여 다양한 방식으로 레시피를 탐색할 수 있습니다.

---

## ⚙️ 주요 기능

### 모델 학습 및 재료 인식

| 기능 | 설명 |
|------|------|
| **YOLOv8 학습** | LVIS Fruits and Vegetables 데이터셋(8,200장, 63클래스) 기반 학습 |
| **GPU 학습 환경** | Google Colab GPU를 활용한 모델 학습 |
| **식재료 인식** | 업로드된 이미지에서 YOLOv8 추론을 통한 재료 자동 인식 |
| **신뢰도 조정** | 임계값 0.25로 설정하여 다양한 환경에서 인식률 개선 |
| **한국어 매핑** | 영어 클래스명 → 한국어 식재료명 자동 변환 (NAME_MAP) |
| **시뮬레이션 모드** | 모델 없이도 랜덤 재료 생성으로 테스트 가능 |

### 레시피 추천

| 기능 | 설명 |
|------|------|
| **일치율 기반 추천** | 보유 재료와 레시피 필요 재료의 일치율을 계산하여 순위별 추천 |
| **요리 카테고리 필터** | 한식·양식·중식·일식 탭으로 요리 종류별 필터링 |
| **레시피 상세 정보** | 재료, 양념, 조리 순서, 꿀팁 등 상세 조리법 제공 |
| **조회수 추적** | 레시피별 조회수 기록 및 인기 레시피 확인 |

### UI/UX

| 기능 | 설명 |
|------|------|
| **이미지 업로드** | 드래그앤드롭 및 파일 선택 방식의 이미지 업로드 |
| **재료 선택/해제** | 인식된 재료를 체크박스로 선택·해제하여 추천 조건 조정 |
| **수동 검색** | 인식되지 않은 재료를 직접 입력하여 검색 |
| **반응형 디자인** | 모바일·데스크탑 환경 모두 지원 |

### API 설계

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | 메인 페이지 |
| `/detect` | POST | 이미지 업로드 → 재료 인식 결과 페이지 |
| `/recommend` | POST | 선택된 재료 기반 레시피 추천 페이지 |
| `/recipe/<id>` | GET | 레시피 상세 페이지 |
| `/api/detect` | POST | REST API — 재료 인식 (JSON 응답) |
| `/api/recommend` | POST | REST API — 레시피 추천 (JSON 응답) |

---

## 🔄 시스템 구조

```
[사용자]  ──→  [Flask 서버]  ──→  [YOLOv8 모델]
 이미지 업로드     웹 서버           재료 인식
                    │
                    ↓
              [레시피 추천 엔진]  ──→  [레시피 DB (JSON)]
               일치율 계산              60개 레시피
```

### 처리 흐름

> **재료 인식** : 사용자 이미지 업로드 → Flask 수신 → YOLOv8 추론 → 영어→한국어 매핑 → 인식 결과 표시

> **레시피 추천** : 재료 선택 → 추천 엔진 → 레시피별 일치율 계산 → 일치율 순 정렬 → 추천 결과 표시

---

## 📁 프로젝트 구조

```
fridge-recipe/
├── app.py                      # Flask 메인 앱 (라우팅 · API)
├── train.py                    # YOLOv8 학습 스크립트
├── organize_dataset.py         # 데이터셋 정리 스크립트 (YOLOv4 → v8 변환)
├── requirements.txt            # 패키지 목록
├── models/
│   └── best.pt                 # 학습된 YOLOv8 모델
├── datasets/
│   └── data.yaml               # 데이터셋 설정 파일
├── static/
│   ├── css/style.css           # 스타일시트
│   ├── js/main.js              # 프론트엔드 로직
│   └── uploads/                # 업로드 이미지 저장
├── templates/
│   ├── index.html              # 메인 페이지
│   ├── result.html             # 인식 결과
│   ├── recommend.html          # 레시피 추천
│   └── recipe_detail.html      # 레시피 상세
├── database/
│   └── recipes.json            # 레시피 DB (60개)
└── utils/
    ├── detector.py             # YOLOv8 추론 모듈
    └── recommender.py          # 레시피 추천 엔진
```

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| **AI 모델** | YOLOv8 (Ultralytics), LVIS Fruits and Vegetables 데이터셋 |
| **백엔드** | Python, Flask |
| **프론트엔드** | HTML, CSS, JavaScript (Vanilla) |
| **데이터베이스** | JSON 기반 레시피 DB |
| **학습 환경** | Google Colab (GPU) |
| **이미지 처리** | OpenCV, Pillow |

---

## 🚀 설치 및 실행

### 1. 환경 세팅

```bash
cd fridge-recipe

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 2. 실행 (시뮬레이션 모드)

```bash
python app.py
# 브라우저에서 http://127.0.0.1:5000 접속
```

모델 없이도 시뮬레이션 모드로 테스트할 수 있습니다.

### 3. YOLOv8 모델 학습 (선택)

```bash
# Kaggle에서 LVIS Fruits and Vegetables 데이터셋 다운로드 후 datasets/ 폴더에 배치
python organize_dataset.py     # 데이터셋 구조 정리
python train.py                # 모델 학습 시작
```

학습 완료 후 `models/best.pt`가 생성되면 실제 인식 모드로 전환됩니다.

---

## 📊 모델 학습 정보

| 항목 | 설정 |
|------|------|
| **데이터셋** | LVIS Fruits and Vegetables (Kaggle) |
| **이미지 수** | 8,200장 |
| **클래스 수** | 63개 |
| **모델** | YOLOv8n (nano) |
| **학습 에폭** | 50 (patience 10 조기 종료) |
| **이미지 크기** | 640 × 640 |
| **배치 크기** | 16 |
| **신뢰도 임계값** | 0.25 |
| **학습 환경** | Google Colab (GPU) |
