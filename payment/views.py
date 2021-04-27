from orders.models import Order
from django.conf import settings
from django.shortcuts import render
# from django.http import JsonResponse
from pypaystack import Transaction
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect, get_object_or_404

load_dotenv()

# Create your views here.


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        transaction = Transaction(
            authorization_key=settings.PAYSTACK_SECRET_KEY)
        # Charge a customer N100.
        response = transaction.charge(
            order.email, "KDBB_"+order_id, (total_cost*100))
        response = transaction.verify("KDBB_"+order_id)

        # data = JsonResponse(response, safe=False)

        if response[0] == 200:  # Transaction is a success
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.paystack_ref_id = "KDBB_"+order_id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
