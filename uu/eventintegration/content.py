from plone.dexterity.content import Container
from zope.interface import implements

from uu.eventintegration.interfaces import IEventCalendar


class EventCalendar(Container):
    """Event calendar folder type"""
    
    implements(IEventCalendar)

