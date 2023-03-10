from typing import Any, Dict
from django import forms
from canalroya.models import Testimonial
from PIL import Image


class TestimonialForm(forms.ModelForm):
    IMAGE_WIDTH = 654
    IMAGE_HEIGHT = 490

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Testimonial
        fields = ("first_name", "last_name", "profession", "city", "province",
                  "comment", "image", "x", "y", "width", "height")

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        crop_fields = ["x", "y", "width", "height"]
        for fieldname in crop_fields:
            if fieldname not in cleaned_data:
                self.add_error("image", "Por favor, recorta la imagen para ajustar su tamaño.")
                break
        return cleaned_data

    def save(self):
        instance = super().save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(instance.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((self.IMAGE_WIDTH, self.IMAGE_HEIGHT), Image.ANTIALIAS)
        resized_image.save(instance.image.path)

        return instance
