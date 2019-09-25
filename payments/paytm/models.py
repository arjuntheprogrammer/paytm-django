from django.db import models
from django.conf import settings

from django.utils import timezone
# Create your models here.

class PaytmHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_paytm')
    ORDERID = models.CharField('ORDERID', max_length=100)
    TXNDATE = models.DateTimeField('TXNDATE', default=timezone.now)
    STATUS = models.CharField('STATUS', max_length=50)
    RESPCODE = models.IntegerField('RESPCODE')
    BANKNAME = models.CharField('BANKNAME', max_length=500, null=True, blank=True)
    TXNID = models.CharField('TXNID', max_length=100, null=True, blank=True)
    BANKTXNID = models.CharField('BANKTXNID', max_length=100, null=True, blank=True)
    PAYMENTMODE = models.CharField('PAYMENTMODE', max_length=10, null=True, blank=True)
    MID = models.CharField(max_length=40)
    CURRENCY = models.CharField('CURRENCY', max_length=5, null=True, blank=True)
    RESPMSG = models.TextField('RESPMSG', max_length=500)
    TXNAMOUNT = models.FloatField('TXNAMOUNT')
    GATEWAYNAME = models.CharField("GATEWAYNAME", max_length=30, null=True, blank=True)
    CHECKSUMHASH = models.CharField("CHECKSUMHASH", max_length=110, null=True, blank=True)

    class Meta:
        app_label = 'paytm'

    def __unicode__(self):
        return self.STATUS
