// select 태그와 관련된 요소들을 가져옴
const categorySelect = document.querySelector('#category-select');
const categorySelect2 = document.querySelector('#category-select2');
const optionsContainer = document.querySelector('#options-container');
const optionsContainer2 = document.querySelector('#options-container2');
const quantitySelect = document.querySelector('#quantity-select');
const incrementButtons = document.querySelectorAll('.increment-quantity');
const decrementButtons = document.querySelectorAll('.decrement-quantity');
    
// 카테고리를 선택할 때마다 호출되는 함수
function handleCategorySelect() {
  const selectedCategory = categorySelect.value;
  const selectedCategory2 = categorySelect2.value;

  // 카테고리가 선택되지 않은 경우, 수량 선택 폼을 숨김
  if (selectedCategory === '' || selectedCategory2 === '') {
    optionsContainer.classList.add('hidden');
    optionsContainer2.classList.add('hidden');
    return;
  }
  
  // 카테고리가 선택된 경우, 수량 선택 폼을 보여줌
  optionsContainer.classList.remove('hidden');
  optionsContainer2.classList.remove('hidden');
  
  // 수량 선택 폼의 라벨을 변경
  const quantityLabel = document.querySelector('#options-container label[for="quantity-select"]');
  const quantityLabel2 = document.querySelector('#options-container2 label[for="quantity-select2"]');
  
  if (selectedCategory) {
    quantityLabel.textContent = `${selectedCategory} `;
    quantityLabel2.textContent = `${selectedCategory} `;
  } else if (selectedCategory2) {
    quantityLabel.textContent = `${selectedCategory2} `;
    quantityLabel2.textContent = `${selectedCategory2} `;
  }
}

const originPriceTag = document.getElementById('origin_price').children[0]
const originPriceTag2 = document.getElementById('origin_price2').children[0]
const originPrice = Number(originPriceTag.textContent)
const originPrice2 = Number(originPriceTag2.textContent)

function handleQuantityChange(e) {
  const button = e.target;
  const targetId = button.getAttribute('data-target');
  const target = document.getElementById('cnt');
  const target2 = document.getElementById('cnt2');
  const cntInputs = document.getElementsByName('cnt');
  const cntInputs2 = document.getElementsByName('cnt2');
  const cntPrice = document.querySelectorAll('.counted-price');
  let quantity = Number(target.value);
  // let price = document.getElementById('total_price');
  
  if (button.classList.contains('increment-quantity')) {
    quantity++;
    originPriceTag.textContent = Number(originPriceTag.textContent) + originPrice;
    originPriceTag2.textContent = Number(originPriceTag2.textContent) + originPrice2;
    cntPrice.forEach((price) => {
      price.textContent = Number(price.textContent) + originPrice;
    })
  } else if (button.classList.contains('decrement-quantity')) {
    if (quantity > 1) {
      quantity--;
      originPriceTag.textContent = Number(originPriceTag.textContent) - originPrice;
      originPriceTag2.textContent = Number(originPriceTag2.textContent) - originPrice2;
      cntPrice.forEach((price) => {
        price.textContent = Number(price.textContent) - originPrice;
      })
    }
  }

  target.value = quantity;
  target2.value = quantity;

  cntInputs.forEach((input) => {
    input.value = quantity;
  })

  cntInputs2.forEach((input) => {
    input.value = quantity;
  })
}

incrementButtons.forEach((button) => {
  button.addEventListener('click', handleQuantityChange);
});

decrementButtons.forEach((button) => {
  button.addEventListener('click', handleQuantityChange);
});

// 카테고리 선택 이벤트 리스너 등록
categorySelect.addEventListener('change', handleCategorySelect);
categorySelect2.addEventListener('change', handleCategorySelect);

// 장바구니 추가 버튼 클릭 이벤트 리스너 등록
// const addToCartButton = document.querySelector('#add-to-cart-button');
// addToCartButton.addEventListener('click', () => {
//   const selectedCategory = categorySelect.value;
//   const selectedQuantity = quantitySelect.value;
//   alert(`${selectedCategory} ${selectedQuantity}개를 장바구니에 추가했습니다.`);
// });