from django import forms


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "widgets/custom_checkbox.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["label"] = self.attrs.get("label", "")
        return context

    def __init__(self, attrs=None):
        default_attrs = {"class": "form-boolean-field"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
