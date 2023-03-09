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
        fields = ("first_name", "last_name", "profession", "city",
                  "comment", "image", "x", "y", "width", "height")

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
