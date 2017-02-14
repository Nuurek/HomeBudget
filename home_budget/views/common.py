from datetime import date, datetime, timedelta


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
