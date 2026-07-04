from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["client_name", "painting_title", "amount", "notes"]
        labels = {
            "client_name": "Nombre del cliente",
            "painting_title": "Nombre del cuadro",
            "amount": "Monto",
            "notes": "Notas",
        }
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Ana López"}),
            "painting_title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Paisaje nocturno"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Ej. 2500"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Detalles adicionales de la venta"}),
        }
