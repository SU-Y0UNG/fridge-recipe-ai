"""
레시피 추천 엔진
- 규칙 기반 재료 매칭
- 일치율 계산 + 부족 재료 표시
- cuisine 필터 (한식/양식/중식/일식)
- 조회수 기능
"""
import json
import os

RECIPE_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'recipes.json')


class RecipeRecommender:
    def __init__(self):
        self.recipes = self._load_recipes()

    def _load_recipes(self) -> list:
        if os.path.exists(RECIPE_DB_PATH):
            with open(RECIPE_DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("[WARN] 레시피 DB 없음 → 기본 레시피 사용")
            return []

    def _save_recipes(self):
        """레시피 DB 저장 (조회수 업데이트용)"""
        if os.path.exists(RECIPE_DB_PATH):
            with open(RECIPE_DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.recipes, f, ensure_ascii=False, indent=2)

    def recommend(self, user_ingredients: list, top_n: int = 10, cuisine: str = None) -> list:
        """
        사용자 재료 기반 레시피 추천

        Args:
            user_ingredients: 사용자가 보유한 재료 목록
            top_n: 추천할 최대 레시피 수
            cuisine: 음식 종류 필터 (한식/양식/중식/일식/None=전체)
        """
        user_set = set(user_ingredients)
        results = []

        for recipe in self.recipes:
            # cuisine 필터
            if cuisine and recipe.get('cuisine') != cuisine:
                continue

            recipe_set = set(recipe['ingredients'])
            matched = user_set & recipe_set
            missing = recipe_set - user_set

            if len(matched) == 0:
                continue

            match_rate = len(matched) / len(recipe_set) * 100

            results.append({
                'id': recipe['id'],
                'name': recipe['name'],
                'cuisine': recipe.get('cuisine', ''),
                'category': recipe['category'],
                'difficulty': recipe['difficulty'],
                'time': recipe['time'],
                'description': recipe['description'],
                'image_emoji': recipe.get('image_emoji', '🍽️'),
                'views': recipe.get('views', 0),
                'matched': list(matched),
                'missing': list(missing),
                'match_rate': round(match_rate, 1),
                'total_ingredients': len(recipe_set)
            })

        results.sort(key=lambda x: x['match_rate'], reverse=True)
        return results[:top_n]

    def get_recipe(self, recipe_id: int) -> dict:
        """레시피 상세 정보 + 조회수 증가"""
        for recipe in self.recipes:
            if recipe['id'] == recipe_id:
                recipe['views'] = recipe.get('views', 0) + 1
                self._save_recipes()
                return recipe
        return None

    def get_popular(self, top_n: int = 10) -> list:
        """인기 레시피 (조회수 순)"""
        sorted_recipes = sorted(self.recipes, key=lambda x: x.get('views', 0), reverse=True)
        return sorted_recipes[:top_n]

    def get_cuisines(self) -> list:
        """사용 가능한 cuisine 목록"""
        cuisines = set()
        for recipe in self.recipes:
            c = recipe.get('cuisine')
            if c:
                cuisines.add(c)
        return sorted(list(cuisines))