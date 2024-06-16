from django.db import models

# Create your models here.


class User(models.Model):
    """注册"""
    email = models.EmailField("邮箱",max_length=50, unique=True)
    password = models.CharField(max_length=10)

    class Meta:
        verbose_name = ""
        db_table = "user"
