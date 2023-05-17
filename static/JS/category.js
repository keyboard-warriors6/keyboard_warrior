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

// const resetBtn = document.getElementById('reset-button')

// resetBtn.addEventListener('click', (event) => {
//   window.location.href = '/products/category/'
// })
