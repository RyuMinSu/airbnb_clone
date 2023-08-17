from django.db import models

# Create your models here.
class CommonModel(models.Model):
    
    """ Common Model Definition"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # 장고의 모델에 올리는 것을 방지한다. 코드 재사용할때 이용한다.