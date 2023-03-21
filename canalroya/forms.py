from typing import Any, Dict

from django import forms
from django.urls import reverse_lazy
from django.utils.html import format_html
from PIL import Image

from canalroya.models import Testimonial


class TestimonialForm(forms.ModelForm):
    IMAGE_WIDTH = 654
    IMAGE_HEIGHT = 490

    comment = forms.CharField(max_length=400, label="Comentario", widget=forms.widgets.Textarea, help_text="Máximo 400 carácteres")
    privacy_policy = forms.BooleanField(required=True, label="Política de privacidad (overrided on __init__)")

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Testimonial
        fields = ("first_name", "last_name", "email", "profession", "city", "province",
                  "comment", "image", "x", "y", "width", "height")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['privacy_policy'].label = format_html(
            ("He leído y acepto la <a target='_blank' href='{}'>política de privacidad</a> "
             "y declaro que aporto mi testimonio por voluntad propia y con total libertad."),
            reverse_lazy("canalroya:privacy-policy")
        )

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
