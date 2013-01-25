from zope.component import getMultiAdapter, adapter
from zope.interface import Interface, implementer
from Solgema.fullcalendar.interfaces import ICriteriaItems

from uu.eventintegration.interfaces import IEventCalendar

@adapter(IEventCalendar, Interface)
@implementer(ICriteriaItems)
def criteria_items_proxy(context, request):
    if not IEventCalendar.providedBy(context):
        return None
    topic_id = context.getDefaultPage()
    if not topic_id:
        return None
    topic = context[topic_id]
    return getMultiAdapter((topic, request), ICriteriaItems)

