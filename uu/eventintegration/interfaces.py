from plone.directives import form
from zope.interface import Interface
from plone.app.textfield import RichText


class IUUEventIntegrationLayer(Interface):
    """Marker interface for installed product as browser layer"""


class IEventCalendar(form.Schema):
    """Folderish event calendar type"""


class IEventText(form.Schema):
    """Text for event"""
   
    text = RichText(
        title=u'Body text',
        description=u'Rich text description and information about event.',
        required=False
    )

