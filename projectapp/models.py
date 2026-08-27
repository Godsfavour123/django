from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=50)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Title: {self.name}, last edited: {self.last_edited.date}, Published:{self.is_published}"


class Student(models.Model):
    # Existing student records may not yet have a matriculation number. The form
    # requires this field for every new or updated student.
    matriculation_number = models.CharField(max_length=30, unique=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
