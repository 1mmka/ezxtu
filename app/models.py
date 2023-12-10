from django.db import models
from django.contrib.auth.models import User 
from django.core import validators

class Rubric(models.Model):
    name = models.CharField(max_length=255, verbose_name='Раздел')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subrubric')
    image = models.ImageField(upload_to='rubric',validators=[validators.FileExtensionValidator(
        allowed_extensions=('jpeg','png','jpg','bmp','tiff','ico','webp')
    )], blank=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Раздел') # раздел объявлении
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=1000, decimal_places=2)
    contact = models.CharField(max_length=32,verbose_name='Контакты')
    image = models.ImageField(verbose_name='Картинка', upload_to='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор') # автор объявления
    
    def __str__(self):
        return f'{self.title} опубликовано {self.created_at} | {self.author}'
    
class FavoriteUserAnnouncements(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username