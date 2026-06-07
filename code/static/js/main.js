/* =======================================
   🥗 AI 냉장고 요리사 - 메인 JS
   ======================================= */

document.addEventListener('DOMContentLoaded', () => {

    // ===== 파일 업로드 미리보기 =====
    const fileInput = document.getElementById('imageInput');
    const uploadSection = document.querySelector('.upload-section');
    const previewContainer = document.querySelector('.preview-container');
    const previewImg = document.getElementById('previewImg');
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.querySelector('.upload-btn');

    if (fileInput) {
        // 파일 선택 시 미리보기
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                showPreview(file);
            }
        });

        // 드래그 앤 드롭
        if (uploadSection) {
            uploadSection.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadSection.classList.add('drag-over');
            });

            uploadSection.addEventListener('dragleave', () => {
                uploadSection.classList.remove('drag-over');
            });

            uploadSection.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadSection.classList.remove('drag-over');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    // DataTransfer로 파일 입력에 설정
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    fileInput.files = dt.files;
                    showPreview(file);
                }
            });

            // 업로드 영역 클릭 시 파일 선택
            uploadSection.addEventListener('click', (e) => {
                if (e.target !== uploadBtn && !e.target.closest('.upload-btn')) {
                    fileInput.click();
                }
            });
        }

        // 폼 제출 시 로딩 표시
        if (uploadForm) {
            uploadForm.addEventListener('submit', (e) => {
                if (!fileInput.files.length) {
                    e.preventDefault();
                    alert('이미지를 선택해주세요!');
                    return;
                }

                const loading = document.querySelector('.loading');
                if (loading) loading.classList.add('show');
                if (uploadBtn) {
                    uploadBtn.textContent = '분석 중...';
                    uploadBtn.disabled = true;
                }
            });
        }
    }

    function showPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (previewImg) previewImg.src = e.target.result;
            if (previewContainer) previewContainer.classList.add('show');
        };
        reader.readAsDataURL(file);
    }

    // ===== 재료 카드 선택 =====
    const ingredientCards = document.querySelectorAll('.ingredient-card');
    const recommendBtn = document.getElementById('recommendBtn');
    const ingredientForm = document.getElementById('ingredientForm');

    ingredientCards.forEach(card => {
        card.addEventListener('click', () => {
            card.classList.toggle('selected');
            updateRecommendButton();
        });
    });

    function updateRecommendButton() {
        const selected = document.querySelectorAll('.ingredient-card.selected');
        if (recommendBtn) {
            if (selected.length > 0) {
                recommendBtn.disabled = false;
                recommendBtn.textContent = `선택한 ${selected.length}개 재료로 레시피 찾기 🔍`;
            } else {
                recommendBtn.disabled = true;
                recommendBtn.textContent = '재료를 선택해주세요';
            }
        }
    }

    // 폼 제출 시 선택된 재료를 hidden input으로 추가
    if (ingredientForm) {
        ingredientForm.addEventListener('submit', (e) => {
            // 기존 hidden input 제거
            ingredientForm.querySelectorAll('input[name="ingredients"]').forEach(el => el.remove());

            const selected = document.querySelectorAll('.ingredient-card.selected');
            if (selected.length === 0) {
                e.preventDefault();
                alert('재료를 1개 이상 선택해주세요!');
                return;
            }

            selected.forEach(card => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'ingredients';
                input.value = card.dataset.name;
                ingredientForm.appendChild(input);
            });
        });
    }

    // ===== 전체 선택 / 해제 =====
    const selectAllBtn = document.getElementById('selectAllBtn');
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', () => {
            const allSelected = document.querySelectorAll('.ingredient-card.selected').length === ingredientCards.length;

            ingredientCards.forEach(card => {
                if (allSelected) {
                    card.classList.remove('selected');
                } else {
                    card.classList.add('selected');
                }
            });

            selectAllBtn.textContent = allSelected ? '전체 선택' : '전체 해제';
            updateRecommendButton();
        });
    }

    // 초기 버튼 상태
    updateRecommendButton();
});
