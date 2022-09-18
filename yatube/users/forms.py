from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# это тоже по сути модель со своими полями , но я не знаю какими
# насколько я понимаю это та модель которая есть у нас в posts
User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm

#  наследуется класс UserCreationForm:
class CreationForm(UserCreationForm):
    #  наследуется класс Meta, вложенный в класс UserCreationForm:
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("first_name", "last_name", "username", "email")