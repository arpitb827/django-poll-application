from django import forms
# from common.utils import send_email
# from . import errors

from django.forms import ModelForm

from .models import Promise

class EntityActionForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    send_email = forms.BooleanField(
        required=False,
    )

    @property
    def email_subject_template(self):
        return 'Entities/notification_subject.txt'

    @property
    def email_body_template(self):
        raise NotImplementedError()
    def form_action(self, account, user):
        raise NotImplementedError()
    def save(self, account, user):
        try:
            account, action = self.form_action(account, user)
        except errors.Error as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise
        if self.cleaned_data.get('send_email', False):
            send_email(
                to=[account.user.email],
                subject_template=False,#self.email_subject_template,
                body_template=self.email_body_template,
                context={
                    "account": account,
                    "action": action,
                }
            )
        return account, action

class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class PromiseForm(ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'description', 'made_on']
        widgets = {
            'made_on': DateTimeInput(),
        }