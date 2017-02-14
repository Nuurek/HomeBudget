from django.views.generic import TemplateView, ListView
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from collections import defaultdict
import json

from home_budget.views.common import DateRangeView
from brands.models import Shop
from .models import Receipt, Purchase
from .forms import BillForm, PurchaseFormSet


class ReceiptView(object):

    @staticmethod
    def _get_shops():
        shops = Shop.objects.all() \
                        .values('brand', 'id', 'address') \
                        .order_by('address')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['brand']
            brands_shops[brand].append({
                'id': shop['id'],
                'address': shop['address'],
            })

        return json.dumps(brands_shops)


class ReceiptCreateView(TemplateView, ReceiptView):

    template_name = "receipt.html"

    def __init__(self, *args, **kwargs):
        super(ReceiptCreateView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 1

    def get(self, request, bill=None, initial_bill_data=None, *args, **kwargs):
        bill_form = BillForm(instance=bill, initial=initial_bill_data)

        PurchaseFormSet.extra = self.initial_number_of_rows

        purchase_formset = PurchaseFormSet(
            instance=bill,
            queryset=Purchase.objects.filter(receipt=bill)
        )

        return self.render_context(bill_form, purchase_formset)

    def post(self, request, bill=None, *args, **kwargs):
        bill_form = BillForm(data=request.POST, instance=bill)
        purchase_formset = PurchaseFormSet(
            data=request.POST,
            instance=bill,
            queryset=Purchase.objects.filter(receipt=bill)
        )

        if bill_form.is_valid() and purchase_formset.is_valid():
            bill = bill_form.save()

            purchases = purchase_formset.save(commit=False)
            for purchase_for_deletion in purchase_formset.deleted_objects:
                purchase_for_deletion.delete()
            for purchase in purchases:
                purchase.receipt = bill
                purchase.save()

            purchases = Purchase.objects.filter(receipt=bill)

            if len(purchases) > 0:
                messages.success(
                    request,
                    "Paragon zapisany."
                )

                pk = bill.id
                return HttpResponseRedirect(reverse('bill_detail', args=[pk]))
            else:
                messages.error(
                    request,
                    "Paragon musi zawierać co najmniej jeden zakup."
                )

                bill.delete()
                return self.render_context(bill_form, purchase_formset)

        return self.render_context(bill_form, purchase_formset)

    def render_context(self, bill_form, purchase_formset):
        context = {
            'form': bill_form,
            'purchase_formset': purchase_formset,
            'shops': self._get_shops(),
        }

        return self.render_to_response(context)


class ReceiptDetailView(ReceiptCreateView):

    template_name = "receipt_create.html"

    def __init__(self, *args, **kwargs):
        super(ReceiptDetailView, self).__init__(*args, **kwargs)
        self.initial_number_of_rows = 0

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Receipt.objects.get(id=pk)
        shop = Shop.objects.get(id=bill.shop_id)
        brand = shop.address
        initial_bill_data = {}
        initial_bill_data['brand'] = shop.brand
        initial_bill_data['address'] = shop.address

        return super(ReceiptDetailView, self).get(
            request, bill=bill, initial_bill_data=initial_bill_data,
            *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        bill = Receipt.objects.get(id=pk)

        return super(ReceiptDetailView, self).post(
            request, bill=bill, *args, **kwargs
        )


class ReceiptListView(ListView, DateRangeView, ReceiptView):
    template_name = "receipt_list.html"

    paginate_by = 10

    is_form = True

    def get_context_data(self, **kwargs):
        context = super(ReceiptListView, self).get_context_data(**kwargs)

        context['start_date'] = self.start_date.strftime("%d.%m.%Y")
        context['end_date'] = self.end_date.strftime("%d.%m.%Y")
        context['is_form'] = self.is_form
        if (self.is_form):
            context['query'] = '&start-date=' + context['start_date'] + \
                '&end-date=' + context['end_date']
        return context

    def get_queryset(self):
        self.start_date, self.end_date = self._get_date_range(
            self.request, "start-date", "end-date", "%d.%m.%Y", 30
        )

        queryset = Receipt.objects.all().values(
            'id',
            'shop__address',
            'time_of_purchase',
            'shop__brand__name'
            ).filter(time_of_purchase__range=(
                self.start_date, self.end_date
            )).annotate(total=Sum(
                F('purchase__unit_price')*F('purchase__amount')
            )).order_by('-time_of_purchase')

        return queryset
