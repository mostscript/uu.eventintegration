from plone.directives import form
from zope.interface import Interface


class IUUEventIntegrationLayer(Interface):
    """Marker interface for installed product as browser layer"""


class IEventCalendar(form.Schema):
    """Folderish event calendar type"""

