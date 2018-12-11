

from django.db import models


class locations(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    address1 = models.CharField(max_length=200, blank=False, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=True)
    province = models.CharField(max_length=60, blank=True, null=True)
    postalcode = models.CharField(max_length=20, blank=False, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    cust_type = models.CharField(max_length=50, blank=True, null=True)
    winbox = models.CharField(max_length=60, blank=True, null=True)
    lat = models.CharField(max_length=60, blank=True, null=True)
    lng = models.CharField(max_length=60, blank=True, null=True)
    sitesurvey_ok = models.CharField(max_length=50, blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    ap_id = models.CharField(max_length=50, blank=True, null=True)
    rssi = models.CharField(max_length=10, blank=True, null=True)
    snr = models.CharField(max_length=10, blank=True, null=True)
    ccq_tx = models.CharField(max_length=10, blank=True, null=True)
    ccq_rx = models.CharField(max_length=10, blank=True, null=True)
    neighbours = models.CharField(max_length=200, blank=True, null=True)
    

