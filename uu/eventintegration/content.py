from plone.dexterity.content import Container
from zope.interface import implements

from Solgema.fullcalendar.interfaces import ISolgemaFullcalendarProperties

from uu.eventintegration.interfaces import IEventCalendar


class EventCalendar(Container):
    """Event calendar folder type"""
    
    implements(IEventCalendar)


def on_calendar_create(context, event):
    calid, title = context.getId(), context.Title()
    # add a topic
    context.invokeFactory(
        id=calid,
        title=title,
        type_name='Topic',
        )
    topic = context.get(calid)
    # add criteria for type, path/location
    crit_type = topic.addCriterion('portal_type', 'ATPortalTypeCriterion')
    crit_type.setValue('plone.app.event.dx.event')
    crit_path = topic.addCriterion('path', 'ATRelativePathCriterion')
    crit_path.setRelativePath('..')
    crit_path.setRecurse(True)  # any subfolders, might as well include
    # topic is selected content item as front page for calendar folder:
    context.setDefaultPage(topic.getId())
    # finally, use calendar layout for the topic:
    topic.setLayout('solgemafullcalendar_view')
    # set the add-form FTI portal_type name for events:
    props = ISolgemaFullcalendarProperties(topic)
    props.eventType = u'plone.app.event.dx.event'
    props.firstHour = 6
    props.minTime = 8
    props.maxTime = 20
    props.disableAJAX = True
    props.caleditable = False
    props.disableDragging = True
    props.disableResizing = True

