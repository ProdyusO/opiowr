from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].label="Коментар (Шановні покупці, у разі обрання послуги доставка, просимо додатково зазначити у цьому полі назву кур'єрської служби та номер відділення)"



    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'mail', 'buying_type', 'comment'
        )
