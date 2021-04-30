from orders.models import Order
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
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
    return render(request, 'payment/process.html', {'order': order, 'pk_public': settings.PAYSTACK_TEST_PUB_KEY, 'total_cost': total_cost})


def verify_payment(request, ref):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(ref)

    if response[0] == 200:  # Check status code is success

        # (response[3]['amount']/100) -> Removes trailing kobo zeros
        if (response[3]['amount']/100) == total_cost:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.paystack_ref_id = ref
            order.save()
            # Remove order_id from session
            del request.session['order_id']

            return redirect('payment:done')
    else:
        return redirect('payment:canceled')


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
