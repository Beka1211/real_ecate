from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    image_first = models.ImageField(upload_to='media/estate_image')

    parent_category = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        ancestors = []
        category = self
        while category:
            ancestors.append(category.title)
            category = category.parent_category
        return ' > '.join(reversed(ancestors))


class City(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Image(models.Model):
    product=models.ForeignKey('Estate',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='media/additional_image')

class Estate(models.Model):
    title = models.CharField(max_length=100, verbose_name = 'Название')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image_first = models.ImageField(upload_to='media/estate_image')
    area = models.DecimalField(decimal_places=1,max_digits=12,verbose_name='km.2')
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    geo = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    promo_video = models.FileField(upload_to='media/estate_video')
    is_active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
