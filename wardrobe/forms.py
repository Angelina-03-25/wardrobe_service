from django import forms
from .models import Item
from catalog.models import Category, Season


class ItemFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.order_by("name"),
        required=False, label="Категория", empty_label="Все категории",
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.order_by("name"),
        required=False, label="Сезон", empty_label="Все сезоны",
    )
    max_temp = forms.IntegerField(required=False, label="Макс. температура", min_value=-50, max_value=50)
    sort = forms.ChoiceField(
        required=False, label="Сортировка",
        choices=[("name", "По названию (А-Я)"), ("temp", "По температуре (возр.)"), ("temp_desc", "По температуре (убыв.)")],
    )


class ItemForm(forms.ModelForm):
    category_name = forms.CharField(
        label="Категория",
        widget=forms.TextInput(attrs={"class": "form-control", "list": "category-list", "placeholder": "Введите или выберите", "autocomplete": "off"}),
    )
    season_name = forms.CharField(
        label="Сезон",
        widget=forms.TextInput(attrs={"class": "form-control", "list": "season-list", "placeholder": "Введите или выберите", "autocomplete": "off"}),
    )

    class Meta:
        model = Item
        fields = ["name", "min_temp"]
        labels = {"name": "Название вещи", "min_temp": "Мин. температура (°C)"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "min_temp": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.category: self.fields["category_name"].initial = self.instance.category.name
            if self.instance.season: self.fields["season_name"].initial = self.instance.season.name

    def clean_min_temp(self):
        temp = self.cleaned_data["min_temp"]
        if temp < -50: raise forms.ValidationError("Температура не может быть ниже -50°C.")
        return temp

    def save(self, commit=True):
        cat_name = self.cleaned_data.get("category_name", "").strip()
        seas_name = self.cleaned_data.get("season_name", "").strip()
        if cat_name:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            self.instance.category = cat
        if seas_name:
            seas, _ = Season.objects.get_or_create(name=seas_name)
            self.instance.season = seas
        return super().save(commit=commit)