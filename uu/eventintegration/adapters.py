from Acquisition import aq_inner

from zope.component import getMultiAdapter, adapter
from zope.interface import Interface, implementer
from Solgema.fullcalendar.interfaces import ICriteriaItems
from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarProperties


from uu.eventintegration.interfaces import IEventCalendar


def default_page(context):
    item_id = context.getDefaultPage()
    if not item_id:
        return None
    return context[item_id]


@adapter(IEventCalendar, Interface)
@implementer(ICriteriaItems)
def criteria_items_proxy(context, request):
    if not IEventCalendar.providedBy(context):
        return None
    topic = default_page(context)
    return getMultiAdapter((topic, request), ICriteriaItems)


@adapter(IEventCalendar)
@implementer(ISolgemaFullcalendarProperties)
def fullcalendar_properties_proxy(context):
    if not IEventCalendar.providedBy(context):
        return None
    topic = default_page(context)
    return ISolgemaFullcalendarProperties(aq_inner(topic), None)

