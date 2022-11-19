from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Bank, Branch

class AddForm(forms.ModelForm):

    class Meta:
        model = Bank
        fields = ('name', 'description', 'inst_num', 'swift_code')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("name", ) == "":
            self.add_error('name', "This field is required")
        if cleaned_data.get("description", ) == "":
            self.add_error('description', "This field is required")
        if cleaned_data.get("inst_num", ) == "":
            self.add_error('inst_num', "This field is required")
        if cleaned_data.get("swift_code", ) == "":
            self.add_error('swift_code', "This field is required")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['description'].required = False
        self.fields['inst_num'].required = False
        self.fields['swift_code'].required = False


class AddBranchForm(forms.ModelForm):

    class Meta:
        model = Branch
        fields = ('name', 'transit_num', 'address', 'email', 'capacity')

    def clean(self):
        cleaned_data = super().clean()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if cleaned_data.get("name", ) == "":
            self.add_error('name', "This field is required")
        if cleaned_data.get("transit_num", ) == "":
            self.add_error('transit_num', "This field is required")
        if cleaned_data.get("address", ) == "":
            self.add_error('address', "This field is required")
        if cleaned_data.get("email", ) == "":
            self.add_error('email', "This field is required")
        # elif not re.match(regex, cleaned_data.get("email", )):
        #     self.add_error('email', "Enter a valid email address")
        try:
            validate_email(cleaned_data.get("email", ))
        except ValidationError:
            print("Enter a valid email address")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['transit_num'].required = False
        self.fields['address'].required = False
        self.fields['email'].required = False
        self.fields['capacity'].required = False