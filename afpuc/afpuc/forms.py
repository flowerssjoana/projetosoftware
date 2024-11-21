from django import forms
class CriarConta(forms.Form):
    matricula = forms.IntegerField(label = 'Matrícula')
    nome = forms.CharField(label = 'Nome')
    email = forms.EmailField(label = 'Email')
