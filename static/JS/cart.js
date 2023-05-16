const allCheckbox = document.querySelector('#all-checkbox')
const itemCheckboxes = document.querySelectorAll('.item-checkbox')
const buyCntTag = document.querySelector('#buy-cnt')
let cnt = itemCheckboxes.length

// 모든 체크박스가 체크되면 전체 선택 체크박스를 체크
for (let i=0; i < itemCheckboxes.length; i++) {
  itemCheckboxes[i].addEventListener('click', function(event) {
    if (this.checked == false ) {
      allCheckbox.checked = false
      cnt -= 1
    } else {
      cnt += 1
    }

    buyCntTag.textContent = cnt

    if (cnt == itemCheckboxes.length) {
      allCheckbox.checked = true
    } else {
      allCheckbox.checked = false
    }
  })
}

// 전체 선택 체크박스를 클릭하면 모든 체크박스를 체크
allCheckbox.addEventListener('click', function (event) {
  itemCheckboxes.forEach(function(checkbox) {
    if (allCheckbox.checked == true) {
      cnt = itemCheckboxes.length
      buyCntTag.textContent = cnt
      checkbox.checked = true
    } else {
      cnt = 0
      buyCntTag.textContent = cnt
      checkbox.checked = false
    }
  })
})

// 수량 수정 비동기 처리
const counters = document.querySelectorAll('.counter')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

counters.forEach(function(counter) {
  const minusBtn = counter.children[0]
  const plusBtn = counter.children[2]
  const cntTag = counter.children[1]
  const cartId = counter.getAttribute('data-cart-id')
  const closeBtn = document.getElementById(`close-btn-${cartId}`)
  const priceTag = document.getElementById(`price-${cartId}`)
  const originPrice = Number(document.getElementById(`origin-price-${cartId}`).textContent)
  const totalPriceTag = document.getElementById('total-price')


  // 장바구니 아이템 개별 삭제
  closeBtn.addEventListener('click', function (event) {
    event.preventDefault()
    axios({
      method: 'post',
      url: `/products/cart/${cartId}/delete/`,
      headers: {'X-CSRFToken': csrftoken},
    })
    .then((response) => {
        location.reload()
      })
  })

  // 장바구니 아이템 수량 줄이기
  minusBtn.addEventListener('click', function(event) {    
    event.preventDefault()
    priceTag.textContent = Number(priceTag.textContent) - originPrice
    totalPriceTag.textContent = Number(totalPriceTag.textContent) - originPrice
    cntTag.textContent = Number(cntTag.textContent) - 1
    const form = document.getElementById(`form-${cartId}`)
    form.setAttribute('value', cntTag.textContent)
    const formData = new FormData()
    formData.append('cnt', cntTag.textContent)

    if (cntTag.textContent == 1) {
      minusBtn.classList.add('text-gray-400')
      minusBtn.classList.add('cursor-default')
      minusBtn.style.pointerEvents = 'none'
    }
    axios({
      method: 'post',
      url: `/products/cart/${cartId}/update/`,
      headers: {'X-CSRFToken': csrftoken},
      data: formData,
    })
  })

  // 장바구니 아이템 수량 늘리기
  plusBtn.addEventListener('click', function(event) {
    event.preventDefault()
    priceTag.textContent = Number(priceTag.textContent) + originPrice
    totalPriceTag.textContent = Number(totalPriceTag.textContent) + originPrice
    cntTag.textContent = Number(cntTag.textContent) + 1
    const form = document.getElementById(`form-${cartId}`)
    form.setAttribute('value', cntTag.textContent)
    const formData = new FormData()
    formData.append('cnt', cntTag.textContent)

    if (cntTag.textContent > 1) {
      minusBtn.classList.remove('text-gray-400')
      minusBtn.classList.remove('cursor-default')
      minusBtn.style.pointerEvents = 'auto'
    }
    axios({
      method: 'post',
      url: `/products/cart/${cartId}/update/`,
      headers: {'X-CSRFToken': csrftoken},
      data: formData,
    })
  })
})