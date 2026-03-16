from django import forms


class OrderForm(forms.Form):
    shipping_name = forms.CharField(max_length=100, required=True, label="Ім'я отримувача")
    shipping_address = forms.CharField(max_length=255, required=True)
    shipping_city = forms.CharField(max_length=100, required=True)
    shipping_street = forms.CharField(max_length=255, required=True)
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(
        max_length=100,
        required=True,
        label="Ім'я отримувача",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ПІБ отримувача"}),
    )
    shipping_city = forms.CharField(
        max_length=100,
        required=True,
        label="Місто",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Місто"}),
    )
    shipping_street = forms.CharField(
        max_length=255,
        required=True,
        label="Вулиця",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Вулиця, будинок"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Телефон",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+380XXXXXXXXX"}),
    )
    comment = forms.CharField(
        required=False,
        label="Коментар",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Коментар до замовлення"}),
    )
