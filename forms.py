from django import forms
from django.forms import ModelForm
from .models import locations


class locationsForm(ModelForm):

    class Meta:
        model = locations

        fields=['name','address1','address2','city','province','postalcode','country','cust_type','winbox','lat','lng','comments','sitesurvey_ok','ap_id','rssi','ccq_tx','ccq_rx','snr']
