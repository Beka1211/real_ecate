from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from user.choices import MyUserRoleEnum

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        user = self.model(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class MyUser(AbstractBaseUser):
    username=models.CharField(max_length=20, verbose_name='введите ваш никнейм')
    email=models.EmailField(unique=True, verbose_name='введите ваш емаил')
    avatar = models.ImageField(
        upload_to='media/user_image',
        blank=True,
        null=True,
        )
    role= models.CharField(
        max_length = 20,
        choices = MyUserRoleEnum.choices,
        default = MyUserRoleEnum.STANDARD_USER,
        verbose_name = 'Роль',
        )
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Баланс')
    is_admin = models.BooleanField(
        default=False
        )
    created_date = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class OPT(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)