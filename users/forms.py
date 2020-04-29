from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    authenticate,
    UsernameField,
    PasswordChangeForm,
)
from mapwidgets.widgets import GooglePointFieldWidget

from users.models import DonorProfile, HospitalProfile, User


class MyDateInput(forms.DateInput):
    input_type = "date"


class DonorUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            is_active=False,
        )
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "DONOR"
        if commit:
            user.save()
        return user


class DonorProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = DonorProfile

        fields = ("mobile_number", "birth_date", "location", "report")
        widgets = {
            "birth_date": MyDateInput(
                attrs={"class": "textbox", "placeholder": "Date of Birth"}
            ),
            "location": GooglePointFieldWidget(
                attrs={"class": "button", "placeholder": "Location"}
            ),
        }


class HospitalUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = User(email=self.cleaned_data["email"], is_active=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "HOSPITAL"
        if commit:
            user.save()
        return user


class HospitalProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"

    class Meta:
        model = HospitalProfile
        fields = (
            "hospital_name",
            "hospital_address",
            "mobile_number",
            "mci_registeration_number",
            "location",
        )
        widgets = {
            "location": GooglePointFieldWidget(),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "placeholder": "Email", "class": "textbox"}
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
                "class": "textbox",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            if username is not None and password:
                self.user_cache = authenticate(
                    self.request, username=username, password=password
                )
                if self.user_cache is None:
                    try:
                        user_temp = User.objects.get(email=username)
                    except:
                        user_temp = None

                    if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                    else:
                        raise forms.ValidationError(
                            self.error_messages["invalid_login"],
                            code="invalid_login",
                            params={"username": self.username_field.verbose_name},
                        )
        except Exception as e:
            print(e)
            raise e
        return self.cleaned_data


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "textbox", "placeholder": "Email"}),
    )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "textbox", "placeholder": "Email"}),
    )


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs["placeholder"] = value.label
            if value.required:
                value.widget.attrs["placeholder"] = (
                    value.widget.attrs["placeholder"] + "*"
                )
            value.widget.attrs["class"] = "textbox"
