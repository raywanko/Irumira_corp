from django import forms
from django.core.validators import RegexValidator, EmailValidator, MaxLengthValidator, MinLengthValidator
import bleach

PHONE_RE = r'^\+?[0-9\-\s]{6,20}$'

class ContactForm(forms.Form):
    inquiry_type = forms.ChoiceField(choices=[
        ('サービスについて','サービスについて'),
        ('取引について','取引について'),
        ('その他','その他'),
    ], required=True)
    company_name = forms.CharField(required=False, max_length=100)
    last_name = forms.CharField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True, max_length=254, validators=[EmailValidator()])
    phone = forms.CharField(required=False, max_length=20, validators=[RegexValidator(regex=PHONE_RE)], widget=forms.TextInput(attrs={'placeholder':'090-1234-5678'}))
    message = forms.CharField(
        required=True,
        widget=forms.Textarea,
        validators=[MinLengthValidator(10), MaxLengthValidator(2000)]
    )
    hp_address = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    def clean_hp_address(self):
        val = self.cleaned_data.get('hp_address','')
        if val:
            raise forms.ValidationError("Spam detected.")
        return ''

    def clean_message(self):
        raw = self.cleaned_data.get('message','')
        # テキストとして扱い、全てのHTMLタグを削除する
        clean = bleach.clean(raw, tags=[], attributes={}, strip=True)
        if len(clean) < 10:
            raise forms.ValidationError("メッセージが短すぎます。")
        return clean.strip()

class RecruitForm(forms.Form):
    desired_position = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True, max_length=254)
    phone = forms.CharField(required=False, max_length=20, validators=[RegexValidator(regex=PHONE_RE)])
    work_experience = forms.CharField(required=False, widget=forms.Textarea, max_length=4000)
    motivation = forms.CharField(required=False, widget=forms.Textarea, max_length=2000)
    hp_address = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_hp_address(self):
        val = self.cleaned_data.get('hp_address','')
        if val:
            raise forms.ValidationError("Spam detected.")
        return ''
