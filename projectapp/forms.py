from django import forms
from projectapp.models import Post, Student

class   PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ["name", "body"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "matriculation_number", "email", "phone_number", "date_of_birth", "department"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
