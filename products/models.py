from django.conf import settings
from django.db import models
# from embed_video.fields import EmbedVideoField


class Category(models.Model):
    """
    brand: 브랜드명
    bluetooth: True일 때 무선, False일 때 유선
    switch: 스위치의 종류
    pressure: 키압
    tenkey: True일 때 텐키리스, False일 때 풀배열
    """
    brand = models.CharField(max_length=50)
    bluetooth = models.BooleanField(default=False)
    switch = models.CharField(max_length=10)
    pressure = models.IntegerField()
    tenkey = models.BooleanField(default=False)


    # '브랜드명 - 제품명'으로 출력된다
    def __str__(self):
        return f'{self.brand} - {self.product.name}'


class Product(models.Model):
    # 제품 이미지가 저장되는 경로
    def image_path(instance, filename):
        return f'products/{filename}'


    """
    name: 제품명
    content: 제품 설명
    category: 제품의 특성에 따른 분류 모음
    product_img: 제품 사진
    price: 제품 가격
    discount_rate: 할인률
    """
    name = models.CharField(max_length=100)
    content = models.TextField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    product_img = models.ImageField(blank=True, upload_to=image_path)
    price = models.IntegerField()
    discount_rate = models.FloatField()
    bookmark = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmark')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.name)


class Review(models.Model):
    # 별점을 1에서 5로 제한하기 위해 만듦
    point = zip(range(1, 6), range(1, 6))

    """
    content: 리뷰 내용. 입력하지 않아도 된다
    rating: 별점. 필수
    likes: '이 리뷰가 도움이 되었어요'
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_written')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices = point)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # '제품명 - 작성자'로 출력된다
    def __str__(self):
        return f'{self.product.name} - {self.user.username}'


class ReviewImages(models.Model):
    # 리뷰에 첨부하는 사진이 저장되는 경로
    def image_path(instance, filename):
        return f'reviews/{instance.review.pk}/{filename}'


    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    # img 선택요소로 수정함
    img = models.ImageField(upload_to=image_path, blank=True, null=True)


# class Review_video(models.Model):
#     review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='videos')
#     video = EmbedVideoField()


class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.product.name} - {self.user}'


class Answer(models.Model):
    inquiry = models.OneToOneField(Inquiry, on_delete=models.CASCADE, related_name='answer')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Answer: {self.inquiry}'


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Product, through='PurchaseItem')
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=10)


    @property
    def total_price(self):
        return sum(product.price for product in self.products.all())


# 구매-상품 중계테이블
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cnt = models.PositiveIntegerField(default=1)


    @property
    def price(self):
        return self.product.price * self.cnt * (1 - self.product.discount_rate)
    
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cnt = models.PositiveIntegerField(default=1)

