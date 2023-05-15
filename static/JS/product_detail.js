// select 태그와 관련된 요소들을 가져옴
const categorySelect = document.querySelector('#category-select');
const optionsContainer = document.querySelector('#options-container');
const quantitySelect = document.querySelector('#quantity-select');
const incrementButtons = document.querySelectorAll('.increment-quantity');
const decrementButtons = document.querySelectorAll('.decrement-quantity');
    
// 카테고리를 선택할 때마다 호출되는 함수
function handleCategorySelect() {
  const selectedCategory = categorySelect.value;

  // 카테고리가 선택되지 않은 경우, 수량 선택 폼을 숨김
  if (selectedCategory === '') {
    optionsContainer.classList.add('hidden');
    return;
  }
  
  // 카테고리가 선택된 경우, 수량 선택 폼을 보여줌
  optionsContainer.classList.remove('hidden');
  
  // 수량 선택 폼의 라벨을 변경
  const quantityLabel = document.querySelector('#options-container label[for="quantity-select"]');
  quantityLabel.textContent = `${selectedCategory} `;
}

function handleQuantityChange(e) {
  const button = e.target;
  const targetId = button.getAttribute('data-target');
  const target = document.getElementById(targetId);
  let quantity = Number(target.value);

  if (button.classList.contains('increment-quantity')) {
    quantity++;
  } else if (button.classList.contains('decrement-quantity')) {
    if (quantity > 1) {
      quantity--;
    }
  }
  target.value = quantity;
}

incrementButtons.forEach(button => {
  button.addEventListener('click', handleQuantityChange);
});

decrementButtons.forEach(button => {
  button.addEventListener('click', handleQuantityChange);
});

// 카테고리 선택 이벤트 리스너 등록
categorySelect.addEventListener('change', handleCategorySelect);

// 장바구니 추가 버튼 클릭 이벤트 리스너 등록
const addToCartButton = document.querySelector('#add-to-cart-button');
addToCartButton.addEventListener('click', () => {
  const selectedCategory = categorySelect.value;
  const selectedQuantity = quantitySelect.value;
  alert(`${selectedCategory} ${selectedQuantity}개를 장바구니에 추가했습니다.`);
});