from django import forms
class CriarConta(forms.Form):
    username = forms.CharField(max_length=100, label="Nome de Usuário")
    nome = forms.CharField(label = 'Nome')
    email = forms.EmailField(label = 'Email')
    tipo = forms.ChoiceField(choices=[('F','Funcionário'),('C','Cliente'),('A','Cliente Associado')],widget = forms.RadioSelect,label="Tipo")
    password = forms.CharField(
        max_length=128, 
        widget=forms.PasswordInput, 
        label="Senha"
    )
    confirm_password = forms.CharField(
        max_length=128, 
        widget=forms.PasswordInput, 
        label="Confirme a Senha"
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            # Adiciona um erro ao campo de confirmação de senha se as senhas não coincidirem
            self.add_error('confirm_password', "As senhas não coincidem.")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")