from django import forms
from .models import FruitsModel,CommentsModel


class FruitsForm(forms.ModelForm):
    class Meta:
        model = FruitsModel
        fields = (
            'name',
            'fruit_image',
            'price',
            'short_info',
        )
        labels = {
            'name':"Meva nomi:",
            'fruit_image':'Meva rasmi:',
            'price':'Narxi:',
            'short_info':'Qisqacha ma`lumot',
        }

class FruitUpdateForm(forms.ModelForm):
    class Meta:
        model = FruitsModel
        fields = (
            'name',
            'fruit_image',
            'price',
            'short_info',
        )
        labels = {
            'name':"Meva nomi:",
            'fruit_image':'Meva rasmi:',
            'price':'Narxi:',
            'short_info':'Qisqacha ma`lumot',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = (
           'comment',
           'star_given', 
        )

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = (
           'comment',
           'star_given', 
        )