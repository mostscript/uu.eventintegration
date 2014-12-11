from datetime import datetime, date
from DateTime import DateTime
from Products.CMFPlone import i18nl10n
from Products.CMFPlone.i18nl10n import ulocalized_time as orig_ulocalized_time


def DT2dt(v):
    dt = v
    if isinstance(v, date):
        dt = datetime(*v.timetuple()[:3])
    elif isinstance(v, DateTime):
        dt = v.asdatetime()
        tz = dt.tzinfo
        if not tz:
            return dt
    else:
        tz = dt.tzinfo
    return tz.localize(datetime(*dt.timetuple()[:7]))

_strftime = lambda v, fmt: DT2dt(v).strftime(fmt)


class PatchedDateTime(DateTime):
    
    def strftime(self, fmt):
        return _strftime(self, fmt)


def new_ulocalized_time(time, *args, **kwargs):
    wrapped_time = PatchedDateTime(time)
    return orig_ulocalized_time(wrapped_time, *args, **kwargs)


def patch_ulocalized_time():
    """Monkey patch ulocalized_time to work around DateTime bug(s)"""
    i18nl10n.ulocalized_time = new_ulocalized_time


def patch_widget():
    try:
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        AbstractDatetimeWidget.ampm = True
    except ImportError:
        pass


def patch_atct_topic_date_indices():
    from Products.ATContentTypes import criteria
    if 'DateRecurringIndex' not in criteria.DATE_INDICES:
        criteria.DATE_INDICES = tuple(
            list(criteria.DATE_INDICES) + ['DateRecurringIndex']
            )
        criteria.registerCriterion(
            criteria.date.ATDateCriteria,
            criteria.DATE_INDICES,
            )
    if 'DateRecurringIndex' not in criteria.SORT_INDICES:
        criteria.SORT_INDICES = tuple(
            list(criteria.SORT_INDICES) + ['DateRecurringIndex']
            )
        criteria.registerCriterion(
            criteria.sort.ATSortCriterion,
            criteria.SORT_INDICES,
            )

