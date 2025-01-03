from . import models
from django import forms
from django.utils.text import slugify
from unidecode import unidecode
from PIL import Image
from django.core.exceptions import ValidationError


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = models.ContactUs
        fields = ['message', 'subject']
        labels = {
            'message': 'Your Message',
            'subject': 'Subject'
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control py-3 mb-4',
                'placeholder': 'Type your message here...',
                'rows': 6
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control py-3 mb-4',
                'placeholder': 'Enter the subject...'
            })
        }


class CreateBlog(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body', 'category', 'image']
        labels = {
            'title': 'Title',
            'body': 'Body',
            'category': 'Category',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control py-3 mb-4',
                'placeholder': 'Enter the title...'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control py-3 mb-4',
                'placeholder': 'Type your message here...',
                'rows': 6
            }),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control py-3 mb-4'
            }),
            'image': forms.FileInput(attrs={
                'class': 'input-group form-control py-9 mb-1'
            })
        }
    def __init__(self, *args, **kwargs):
        super(CreateBlog, self).__init__(*args, **kwargs)
        self.fields['category'].widget.choices = models.Category.objects.filter(status=True).values_list('id', 'title')

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:

            if image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('The image size must not exceed 5MB.')

            img = Image.open(image)
            fix_width, fix_height = 1920, 1080
            width, height = img.size
            if not width == fix_width or not height == fix_height:
                raise ValidationError(f"The image must be {fix_width}x{fix_height} pixels.")

        return image

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')

        if not slug and title:
            slug = slugify(unidecode(title))

        if models.Article.objects.filter(slug=slug).exists():
            raise self.add_error('title', 'An article with this title already exists. Please choose another one.')

    def save(self, commit=True):
        instance = super(CreateBlog, self).save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
