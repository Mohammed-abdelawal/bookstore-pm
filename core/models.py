from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='books/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews' 


class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review of {self.book.title} by {self.user.username}'
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews' 
        unique_together = [["user", "book"],]