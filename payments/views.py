from django.shortcuts import render
from django.http import HttpResponse

import razorpay
client = razorpay.Client(auth=("rzp_test_p860XxWC2yFrgd", "4IQsjv5J0RffPvEbdZG0iYsl"))


def testing(request):

    return render(request, 'order.html',{})


def create_order(request):

    context = {}
    if request.method == 'POST':
        print("INSIDE Create Order!!!")
        name = request.POST.get('name')
        


        order_amount = int(request.POST.get('fees'))
        order_amount *=100

       
        print(order_amount)
        order_currency = 'INR'

        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']

        if order_status=='created':

            # Server data for user convinience
            
            context['fees'] = order_amount
            context['name'] = name
            

            # data that'll be send to the razorpay for
            context['order_id'] = order_id


            return render(request, 'confirm_order.html', context)
    return HttpResponse('<h1>Error in  create order function</h1>')



def payment_status(request):

    response = request.POST

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    try:
        status = client.utility.verify_payment_signature(params_dict)
        return render(request, 'order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'order_summary.html', {'status': 'Payment Faliure!!!'})

