// // select 태그와 관련된 요소들을 가져옴
// const categorySelect = document.querySelector('#category-select');
// const categorySelect2 = document.querySelector('#category-select2');
// const optionsContainer = document.querySelector('#options-container');
// const optionsContainer2 = document.querySelector('#options-container2');
// const quantitySelect = document.querySelector('#quantity-select');
// const incrementButtons = document.querySelectorAll('.increment-quantity');
// const decrementButtons = document.querySelectorAll('.decrement-quantity');

// // 가격 관련된 요소를 가져옴
// const originPriceTag = document.getElementById('origin_price').children[0]
// const originPriceTags2 = document.querySelectorAll('.origin-price2')
// const originPrice = Number(originPriceTag.textContent)

// // 수량 관련된 요소를 가져옴
// const target = document.getElementById('cnt');
// const target2 = document.getElementById('cnt2');
// const cntInputs = document.getElementsByName('cnt');
// const cntInputs2 = document.getElementsByName('cnt2');
    

// // 카테고리를 선택할 때마다 호출되는 함수
// function handleCategorySelect() {
//   const selectedCategory = categorySelect.value;
//   const selectedCategory2 = categorySelect2.value;

//   // 카테고리가 선택되지 않은 경우, 수량 선택 폼을 숨김
//   if (selectedCategory === '' || selectedCategory2 === '') {
//     optionsContainer.classList.add('hidden');
//     optionsContainer2.classList.add('hidden');
//     return;
//   }
  
//   // 카테고리가 선택된 경우, 수량 선택 폼을 보여줌
//   optionsContainer.classList.remove('hidden');
//   optionsContainer2.classList.remove('hidden');
  
//   // 수량 선택 폼의 라벨을 변경
//   const quantityLabel = document.querySelector('#options-container label[for="quantity-select"]');
//   const quantityLabel2 = document.querySelector('#options-container2 label[for="quantity-select2"]');
  
//   if (selectedCategory) {
//     quantityLabel.textContent = `${selectedCategory} `;
//     quantityLabel2.textContent = `${selectedCategory} `;
//   } else if (selectedCategory2) {
//     quantityLabel.textContent = `${selectedCategory2} `;
//     quantityLabel2.textContent = `${selectedCategory2} `;
//   }

//   originPriceTags2.forEach((tag) => {
//     tag.textContent = originPrice
//   })

//   cntInputs.forEach(input => {
//     input.value = 1
//   })
// }

// function handleQuantityChange(e) {
//   const button = e.target;
//   const targetId = button.getAttribute('data-target');
  
//   const cntPrice = document.querySelectorAll('.counted-price');
//   let quantity = Number(target.value);
//   // let price = document.getElementById('total_price');
  
//   if (button.classList.contains('increment-quantity')) {
//     quantity++;
//     originPriceTag.textContent = Number(originPriceTag.textContent) + originPrice;
//     console.log(originPriceTag)
   
//     originPriceTags2.forEach(tag => {
//       tag.textContent = Number(originPriceTag.textContent)
//     });

//     cntPrice.forEach((price) => {
//       price.textContent = Number(price.textContent) + originPrice;
//     })
//   } else if (button.classList.contains('decrement-quantity')) {
//     if (quantity > 1) {
//       quantity--;
//       originPriceTag.textContent = Number(originPriceTag.textContent) - originPrice;

//       originPriceTags2.forEach(tag => {
//         tag.textContent = Number(originPriceTag.textContent)
//       });

//       cntPrice.forEach((price) => {
//         price.textContent = Number(price.textContent) - originPrice;
//       })
//     }
//   }

//   target.value = quantity;
//   target2.value = quantity;

//   cntInputs.forEach((input) => {
//     input.value = quantity;
//   })

//   cntInputs2.forEach((input) => {
//     input.value = quantity;
//   })
// }

// incrementButtons.forEach((button) => {
//   button.addEventListener('click', handleQuantityChange);
// });

// decrementButtons.forEach((button) => {
//   button.addEventListener('click', handleQuantityChange);
// });

// // 카테고리 선택 이벤트 리스너 등록
// categorySelect.addEventListener('change', handleCategorySelect);
// categorySelect2.addEventListener('change', handleCategorySelect);

// 장바구니 추가 버튼 클릭 이벤트 리스너 등록
// const addToCartButton = document.querySelector('#add-to-cart-button');
// addToCartButton.addEventListener('click', () => {
//   const selectedCategory = categorySelect.value;
//   const selectedQuantity = quantitySelect.value;
//   alert(`${selectedCategory} ${selectedQuantity}개를 장바구니에 추가했습니다.`);
// });


const optionsContainer = document.querySelector('#options-container');
const optionsContainer2 = document.querySelector('#options-container2');
const incrementButtons = document.querySelectorAll('.increment-quantity');
const decrementButtons = document.querySelectorAll('.decrement-quantity');
const originPriceTag = document.getElementById('origin_price').children[0];
const originPriceTag2 = document.getElementById('origin_price2').children[0];
const originPrice = Number(originPriceTag.textContent);
const originPrice2 = Number(originPriceTag2.textContent);
const target = document.getElementById('cnt');
const target2 = document.getElementById('cnt2');
const cntInputs = document.getElementsByName('cnt');
const cntInputs2 = document.getElementsByName('cnt2');

function handleQuantityChange(e) {
  const button = e.target;
  let quantity = Number(target.value);
  const cntPrice = document.querySelectorAll('.counted-price');
  const cntPrice2 = document.querySelectorAll('.counted-price2');
  
  if (button.classList.contains('increment-quantity')) {
    quantity++;
    originPriceTag.textContent = Number(originPriceTag.textContent) + originPrice;
    originPriceTag2.textContent = Number(originPriceTag2.textContent) + originPrice2;
    
    // console.log(originPriceTag2)
    cntPrice.forEach((price) => {
      price.textContent = Number(price.textContent) + originPrice;
    })
    cntPrice2.forEach((price) => {
      price.textContent = Number(price.textContent) + originPrice2;
    })
    console.log(cntPrice)
    // console.log(cntPrice2)
  } else if (button.classList.contains('decrement-quantity')) {
    if (quantity > 1) {
      quantity--;
      originPriceTag.textContent = Number(originPriceTag.textContent) - originPrice;
      originPriceTag2.textContent = Number(originPriceTag2.textContent) - originPrice2;
      
      // console.log(originPriceTag2)
      cntPrice.forEach((price) => {
        price.textContent = Number(price.textContent) - originPrice;
      })
      cntPrice2.forEach((price) => {
        price.textContent = Number(price.textContent) - originPrice2;
      })
    }
  }

  target.value = quantity;
  target2.value = quantity;

  cntInputs.forEach((input) => {
    input.value = quantity;
  });
  cntInputs2.forEach((input) => {
    input.value = quantity;
  });
}

incrementButtons.forEach((button) => {
  button.addEventListener('click', handleQuantityChange);
});

decrementButtons.forEach((button) => {
  button.addEventListener('click', handleQuantityChange);
});

optionsContainer.classList.remove('hidden');




// 리뷰 수정
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
// const reviewUpdate = document.querySelectorAll('.review-edit-btn')

// reviewUpdate.forEach((review) => {
//   review.addEventListener('click', (event) => {
//     const reviewId = event.target.dataset.reviewId
//     // console.log(reviewId)
//     const reviewUpdateDiv = document.querySelector(`#review-edit-form-${reviewId}`)
//     // console.log(reviewUpdateDiv)
//     if (reviewUpdateDiv.hidden == true) {
//       reviewUpdateDiv.hidden = false
//     } else {
//       reviewUpdateDiv.hidden = true
//     }
//   })
// })

// const reviewUpdateConfirm = document.querySelectorAll('.review-edit-form')

// reviewUpdateConfirm.forEach((updateBtn) => {
//   updateBtn.addEventListener('submit', (event) => {
//     event.preventDefault()
//     const productId = event.target.dataset.productId
//     console.log(productId)
//     const reviewId = event.target.dataset.reviewId
//     console.log(reviewId)


//     const reviewContentTag = document.getElementById(`review-content-${reviewId}`)

//     const reviewContent = reviewContentTag.children[0].children[1].value

//     const reviewRating = reviewContentTag.children[1].children[1].value

//     console.log(reviewRating)

//     const form = new FormData()
//     form.append('content', reviewContent)
//     form.append('rating', reviewRating)
    

//     axios({
//       method: 'post',
//       url: `http://127.0.0.1:8000/products/${productId}/review/${reviewId}/update/`,
//       headers:{'X-CSRFToken': csrftoken},   
//       data: form,
//     })
//     .then((response) => {
//       updateBtn.hidden = true
//       location.reload()

//     })
//     .catch((error) => {
//       console.log(error.response)
//     })
//   })
// })

// 리뷰 수정
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const reviewUpdate = document.querySelectorAll('.review-edit-btn')

reviewUpdate.forEach((review) => {
  review.addEventListener('click', (event) => {
    const reviewId = event.target.dataset.reviewId
    // console.log(reviewId)
    const reviewUpdateDiv = document.querySelector(`#review-edit-form-${reviewId}`)
    // console.log(reviewUpdateDiv)
    if (reviewUpdateDiv.hidden == true) {
      reviewUpdateDiv.hidden = false
    } else {
      reviewUpdateDiv.hidden = true
    }
  })
})

const reviewUpdateConfirm = document.querySelectorAll('.review-edit-form')

reviewUpdateConfirm.forEach((updateBtn) => {
  updateBtn.addEventListener('submit', (event) => {
    event.preventDefault()
    const productId = event.target.dataset.productId
    // console.log(productId)
    const reviewId = event.target.dataset.reviewId
    // console.log(reviewId)

    const reviewContentTag = document.getElementById(`review-content-${reviewId}`)
    console.log(reviewContentTag);
    // console.log(reviewContentTag.parentNode);
    // console.log(reviewContentTag.parentNode.children);
    const reviewContent = reviewContentTag.children[1].value
    const reviewRating = reviewContentTag.children[3].value
    const reviewImg = event.target.img.files[0]

    const formData = new FormData()
    formData.append('content', reviewContent)
    formData.append('rating', reviewRating)
    formData.append('img', reviewImg)

    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/products/${productId}/review/${reviewId}/update/`,
      headers:{
        'X-CSRFToken': csrftoken,
        "Content-Type": "multipart/form-data",
      },
      data: formData,
    })
    .then((response) => {
      updateBtn.hidden = true
      location.reload()
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})


const button1 = document.getElementById('button1');
const section1 = document.getElementById('section1');

button1.addEventListener('click', () => {
  window.scrollBy({top: section1.getBoundingClientRect().top-180, behavior: 'smooth'});
});

const button2 = document.getElementById('button2');
const section2 = document.getElementById('section2');

button2.addEventListener('click', () => {
  window.scrollBy({top: section2.getBoundingClientRect().top-180, behavior: 'smooth'});
});

const button3 = document.getElementById('button3');
const section3 = document.getElementById('section3');

button3.addEventListener('click', () => {
  window.scrollBy({top: section3.getBoundingClientRect().top-180, behavior: 'smooth'});
});