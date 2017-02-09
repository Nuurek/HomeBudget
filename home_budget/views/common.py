from datetime import date, datetime, timedelta
from collections import defaultdict
import json

from ..models import Shop


class BillView(object):

    def _get_shops(self):
        shops = Shop.objects.all() \
                        .values('brand__name', 'id', 'address') \
                        .order_by('brand__name', 'address')

        brands_shops = defaultdict(list)
        for shop in shops:
            brand = shop['brand__name']
            brands_shops[brand].append({
                'id': shop['id'],
                'address': shop['address']
            })

        return json.dumps(brands_shops)


class DateRangeView(object):

    def _get_date_range(self, request, start_date_id, end_date_id,
                        format, delta):
        try:
            end_date = datetime.strptime(
                request.GET.get(end_date_id),
                format
            )
        except:
            end_date = datetime.now()

        try:
            start_date = datetime.strptime(
                request.GET.get(start_date_id),
                format
            )
        except:
            start_date = end_date - timedelta(days=delta)

        return start_date, end_date
