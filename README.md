# ⌨ Keyboard Warrior 😉
![캡처](/static/img/logo_2.png)
## 👩‍👩‍👧‍👦팀원
- 프론트엔드
  - 박지환, 최은비, 박지현
- 백엔드
  - 김범서, 장하늬
<br>

## 🎉프로젝트 소개
- Keyboard-Warrior 프로젝트는 기계식 키보드를 좋아하는 사람들이 원하는 제품을 편리하게 검색하고 구매하기 위한 쇼핑몰입니다.
- 이 프로젝트는 기계식 키보드 판매를 위한 제품 목록, 제품 상세정보, 장바구니 및 주문 처리 등의 기능을 제공합니다. 

## 🚀주요 기능
- 제품 목록: 다양한 종류의 키보드를 제품 목록으로 제공합니다. 사용자는 제품을 검색하고 필터링하여 원하는 제품을 찾을 수 있습니다.
- 제품 상세 정보: 선택한 제품에 대한 상세 정보를 제공합니다. 제품 이미지, 스펙, 가격 등을 확인할 수 있습니다.
- 장바구니: 사용자는 원하는 제품을 장바구니에 담아 나중에 구매할 수 있습니다. 장바구니에서는 제품 수량 변경, 제품 삭제 등의 기능을 제공합니다.
- 주문 처리: 사용자가 장바구니에 담은 제품을 주문할 수 있습니다. 주문 정보와 배송 정보를 입력하고 주문을 진행합니다. 주문이 완료되면 주문 명세서가 메일로 발송됩니다.

## ✨주요 기능 캡쳐
### Index
![Index](/static/readme/index.png)
### Category
![Category](/static/readme/category.png)
### Detail
![Detail](/static/readme/detail_1.png)
![Detail](/static/readme/detail_2.png)
### Q&A
![Q&A](/static/readme/qna.png)
### Cart
![Cart](/static/readme/cart.png)
### Purchase
![Purcahse_create](/static/readme/purchase_create.png)
### Purchase_Complete
![Purchase_complete](/static/readme/purchase_complete.png)
### Email
![Email](/static/readme/email.png)

## 💻요구 사항
- Python 3.9X
- Django 3.2.18

## 😊대표 URL
- 상품
  - `/products/`: 상품을 개괄적으로 확인할 수 있는 대문페이지를 조회합니다.
  - `/porducts/create/`: 관리자가 상품을 등록합니다.
  - `/products/category/`: 상품을 정렬하고 카테고리별로 필터하여 조회합니다. 
  - `/products/<int:product_pk>/`: 상품 상세 페이지를 조회합니다.
- 후기
  - `/products/<int:product_pk>/review/`: 후기를 생성합니다.
- 구매
  - `/products/purchase_create/`: 장바구니를 통해 상품을 주문합니다.
  - `/products/<int:product_pk>/purchase/`: 상품 상세페이지에서 바로 상품을 주문합니다.
  - `/products/purchase_complete/<int:purchase_pk>/`: 구매 완료 페이지를 조회합니다.
- 장바구니
  - `/products/cart/`: 장바구니를 조회합니다.
  - `/products/<int:product_pk>/add-to-cart/`: 상품을 장바구니에 추가합니다.
- 문의 및 답변
  - `/products/<int:product_pk>/inquiry/create/`: 문의사항을 생성합니다.
  - `/products/<int:product_pk>/inquiry/<int:inquiry_pk>/create/`: 관리자의 답변을 생성합니다.
- 이스트 에그
  - `/products/keyboard_trend/`: 관리자가 네이버 쇼핑 인사이트 API를 이용하여 지정된 3개월동안 10개의 브랜드의 검색량을 조회하고 이를 wordCloud로 시각화합니다. 코드를 수정하여 원하는 키보드 브랜드의 검색량을 확인할 수 있습니다.
