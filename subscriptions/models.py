from django.db import models


class Subscriptions(models.Model):
    """ подписки по email """
    email = models.EmailField()
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписки по email'    
        verbose_name_plural = 'Подписки по email'    