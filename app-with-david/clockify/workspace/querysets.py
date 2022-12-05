from django.db.models import QuerySet


class TimeRecordQuerySet(QuerySet):
    def filter_running_timers(self, user=None):
        qs = self.filter(end_time__isnull=True)

        if user:
            qs.filter(user=user)

        return qs
