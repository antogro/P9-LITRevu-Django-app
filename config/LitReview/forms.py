from django import forms
from .models import Ticket, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "headline", "body")


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
