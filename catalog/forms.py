from django import forms
from catalog.models import Product
import os
from PIL import Image as PImage


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    website = forms.URLField(
        required=False,
        widget=forms.HiddenInput,
        label='Оставьте это поле пустым'
    )

    class Meta:
        model = Product
        fields = ['name', 'text', 'image', 'category', 'price']

    def clean(self):
        cleaned_data = super().clean()

        # Защита от спама (если бот заполнил скрытое поле website)
        if cleaned_data.get('website'):
            raise forms.ValidationError('Обнаружена попытка автоматизированного ввода.')

        name = cleaned_data.get('name', '').lower()
        text = cleaned_data.get('text', '').lower()

        found_words = []
        for word in FORBIDDEN_WORDS:
            if word in name or word in text:
                found_words.append(word)

        if found_words:
            raise forms.ValidationError(
                f'В полях "Наименование" или "Описание" обнаружены запрещенные слова: {", ".join(found_words)}.'
            )

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_class = 'form-control styled-input'

        for field_name, field in self.fields.items():
            if field_name == 'website' or isinstance(field, forms.ImageField):
                continue

            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} {css_class}'.strip()

            if field.help_text and not isinstance(field, forms.CheckboxInput):
                field.widget.attrs['placeholder'] = field.help_text

            field.label = ""

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return None

        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = str(image.name).split('.')[-1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                f'Недопустимый формат изображения. Поддерживаются только файлы типа {", ".join(valid_extensions)}.'
            )

        max_size_mb = 5 * 1024 * 1024
        if image.size > max_size_mb:
            raise forms.ValidationError(f'Размер изображения превышает допустимые 5 МБ.')

        return image

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Проверяем, есть ли новое изображение
        new_image = self.cleaned_data.get('image')
        if new_image and hasattr(new_image, 'temporary_file_path'):
            img_temporary_path = new_image.temporary_file_path()

            with PImage.open(img_temporary_path) as im:
                im.thumbnail((800, 600))

                ext = os.path.splitext(instance.image.name)[1]
                output_format = 'JPEG' if ext.lower() == '.jpg' else 'PNG'

                im.save(img_temporary_path, format=output_format, quality=95)

        if commit:
            instance.save()
        return instance