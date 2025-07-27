from django.db.models import TextChoices

class MyUserRoleEnum(TextChoices):
    STANDARD_USER= 'standard_user','Обычный_пользовотель'
    MANAGER = 'manager', 'Менеджер'
    ACCOUNTANT = 'accountant', 'Бухалтер'
