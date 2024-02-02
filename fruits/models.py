from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from register.models import CustomUser
# Create your models here.


class FruitsModel(models.Model):
    name = models.CharField(max_length=15)
    fruit_image = models.ImageField(default='default_fruit_image.jpg',upload_to='media/')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    short_info = models.TextField()

    def __str__(self):
        return self.name
    
    
class CommentsModel(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    fruit = models.ForeignKey(FruitsModel,on_delete=models.CASCADE,blank=True,null=True)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ]
    )
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.fruit.name