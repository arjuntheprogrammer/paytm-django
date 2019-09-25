from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import Checksum
from django.http import JsonResponse, HttpResponse
import json


from paytm.models import PaytmHistory
# Create your views here.

@login_required
def home(request):
    return HttpResponse("<html><a href='"+ settings.HOST_URL +"/paytm/payment'>PayNow</html>")


def payment(request):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    # get_lang = "/" + get_language() if get_language() else ''
    get_lang = ""
    CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
    print("CALLBACK_URL", CALLBACK_URL)
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()

    bill_amount = 100
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID':'harish@pickrr.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        print("data_dict", str(data_dict))
        print("param_dict", str(param_dict['CHECKSUMHASH']))
        return render(request,"payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
            print("key, request.POST[key] = ", key, request.POST[key])

        CHECKSUMHASH = data_dict['CHECKSUMHASH']
        
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            print("Checksum verification passed!!!")
            for key in data_dict:
                if data_dict[key] == "":
                    data_dict[key] = None
            data_dict['CHECKSUMHASH'] = CHECKSUMHASH
            PaytmHistory.objects.create(user=request.user, **data_dict)
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)




#################################################################
@csrf_exempt
def getChecksum(request):
    if request.method == 'POST':
        order_id = Checksum.__id_generator__()
        data = json.loads(request.body)
        data["ORDER_ID"] = order_id
        print("data=", data)
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        CHECKSUMHASH = Checksum.generate_checksum(data, MERCHANT_KEY)
        print("CHECKSUMHASH = ", CHECKSUMHASH)
        return JsonResponse({"checksum": CHECKSUMHASH, 'order_id': order_id}, status=200, safe=False)

@csrf_exempt
def verifyChecksum(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}

        for key in request.POST:
            data_dict[key] = request.POST[key]
            print("key, request.POST[key] = ", key, request.POST[key])

        CHECKSUMHASH = data_dict['CHECKSUMHASH']
        
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        print("verify=", verify)
        if verify:
            print("Checksum verification passed!!!")
            for key in data_dict:
                if data_dict[key] == "":
                    data_dict[key] = None
            data_dict['CHECKSUMHASH'] = CHECKSUMHASH
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)
