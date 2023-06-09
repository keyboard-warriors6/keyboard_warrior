// 상품 필터
const checkboxes = document.querySelectorAll('.main-checkbox')
const nowUrl = window.location.href

checkboxes.forEach(btn => {
  const btnName = btn.getAttribute('name')
  let btnValue = btn.getAttribute('value')

  btnValue = encodeURIComponent(btnValue)
  
  if (nowUrl.includes(`${btnName}=${btnValue}`)) {
    btn.setAttribute('checked', '')
  } else {
    btn.removeAttribute('checked', false)
  }

  btn.addEventListener('click', (event) => {
    // 현재 url에 이미 필터가 선택되었다면
    if (nowUrl.includes(`&${btnName}=${btnValue}`)) {

      // 현재 url에서 선택된 필터 제거
      const newUrl = nowUrl.replace(`&${btnName}=${btnValue}`,'')

      window.location.href = newUrl

    } else {
      const newUrl = `${nowUrl}&${btnName}=${btnValue}`

      window.location.href = newUrl
    }

  })
})

// 상품 정렬
const filters = document.querySelectorAll('[name=filter]')

filters.forEach(filterBtn => {
  if (nowUrl.includes(`${filterBtn.value}`)) {
    filterBtn.classList.add('text-black')
  } else {
    filterBtn.classList.remove('text-black')
  }

  filterBtn.addEventListener('click', (event) => {
    const url = new URL(nowUrl).searchParams
    const filterTag = url.get('filter')
    let newUrl

    // 현재 url에서 선택된 필터 제거
    if (filterTag) {
      newUrl = nowUrl.replace(`${filterTag}`,`${filterBtn.value}`)
    } else {
      newUrl = `${nowUrl}?filter=${event.target.value}`
    }
    window.location.href = newUrl
  })
})

// 필터 초기화 버튼
const resetBtns = document.querySelectorAll('.reset-button')

resetBtns.forEach(resetBtn => {
  if (nowUrl.includes(`&`) || !nowUrl.includes('all')) {
      resetBtn.classList.remove('text-gray-400')
      resetBtn.removeAttribute('disabled')
    } else {
      resetBtn.classList.add('text-gray-400')
      resetBtn.setAttribute('disabled', '')
    }
    resetBtn.addEventListener('click', (event) => {
      window.location.href = '/products/category/?filter=all'
  })
})

// 북마크 기능
const bookmarkForms = document.querySelectorAll('.bookmark')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

bookmarkForms.forEach(function(form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault()
    const productId = event.target.dataset.productId
    
    axios({
      method: "post",
      url: `/products/${productId}/bookmark/`,
      headers:{'X-CSRFToken': csrftoken},
    })
    .then((response) => {
      const isBookmarked = response.data.bookmark
      console.log(response.data)
      const bookmarkIcon = form.children[1].children[0].children[0]
      if (isBookmarked) {
        bookmarkIcon.classList.add('fill-main')
        bookmarkIcon.classList.remove('fill-white')
      } else {
        bookmarkIcon.classList.add('fill-white')
        bookmarkIcon.classList.remove('fill-main')
      }
    })
  })
})