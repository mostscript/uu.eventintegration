from datetime import datetime
from DateTime import DateTime
from Products.CMFPlone import i18nl10n
from Products.CMFPlone.i18nl10n import ulocalized_time as orig_ulocalized_time


def DT2dt(v):
    tz = dt.tzinfo
    dt = v
    if isinstance(v, date):
        dt = datetime(*v.timetuple()[:3])
    if isinstance(v, DateTime):
        dt = v.asdatetime()
        if not tz:
            return dt
    return tz.localize(datetime(*dt.timetuple()[:7]))

_strftime = lambda v, fmt: DT2dt(v).strftime(fmt)


class PatchedDateTime(DateTime):
    
    def strftime(self, fmt):
        return _strftime(self, fmt)


def new_ulocalized_time(time, *args, **kwargs):
    wrapped_time = PatchedDateTime(time)
    return orig_ulocalized_time(time, *args, **kwargs)


def patch_ulocalized_time():
    """Monkey patch ulocalized_time to work around DateTime bug(s)"""
    i18nl10n.ulocalized_time = new_ulocalized_time


def patch_widget():
    from plone.formwidget.datetime.base import AbstractDatetimeWidget
    AbstractDatetimeWidget.ampm = True
