from plone.event.utils import utc
from plone.app.event.interfaces import IEventSettings
from plone.app.event.dx import behaviors
from plone.memoize import ram
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone.app.textfield.value import RichTextValue
from plone.registry.interfaces import IRegistry
from Acquisition import aq_parent
from zope.component import getUtility
from zope.component.hooks import setSite


SITES = ['qiteamspace', 'opip']


_tz_cache_key = lambda fn,site: site.getPhysicalPath()


@ram.cache(_tz_cache_key)
def sitetz(site):
    registry = getUtility(IRegistry)
    cp = registry.forInterface(
        IEventSettings,
        prefix='plone.app.event',
        )
    return cp.portal_timezone or 'US/Mountain'


def migrate_event(source, site):
    parent_folder = aq_parent(source)
    evid = source.getId()
    newid = '%s-new' % evid
    if newid not in parent_folder.objectIds():
        timezone = sitetz(site)
        parent_folder.invokeFactory(
            id=newid,
            type_name='plone.app.event.dx.event',
            title=source.Title(),
            start=utc(source.start().asdatetime()),
            end=utc(source.start().asdatetime()),
            timezone=timezone,
            whole_day=False,
            )
        dest = parent_folder.get(newid)
        # behaviors:
        basic = behaviors.IEventBasic(dest)
        recur = behaviors.IEventRecurrence(dest)
        loc = behaviors.IEventLocation(dest)
        attendees =behaviors. IEventAttendees(dest)
        contact = behaviors.IEventContact(dest)
        summary = behaviors.IEventSummary(dest)
        # default values for fields we will not copy:
        basic.timezone = timezone
        basic.wholeday = False
        recur.recurrence = None  # default, no recurrence specified
        # start, end dates:
        basic.start = utc(source.start().asdatetime())
        basic.end = utc(source.start().asdatetime())
        # contact name, phone, email, event_url
        contact.contact_name = source.contact_name()
        contact.contact_email = source.contact_email()
        contact.contact_phone = source.contact_phone()
        contact.event_url = source.event_url()
        # location
        loc.location = source.getLocation()
        # modification date and Subject/tags metadata
        dest.modification_date = source.modification_date
        dest.setSubject(source.Subject())
        # Deal with body text.
        text = source.getText()
        if text:
            summary.text = RichTextValue(raw=text.decode('utf-8'))
        dest.reindexObject()
    try:
        parent_folder.manage_delObjects([evid,])
    except LinkIntegrityNotificationException:
        print 'skipped deleting %s for link integrity' % repr(source)


def migrate_events(site):
    catalog = site.portal_catalog
    result = catalog.search({'portal_type':'Event'})
    events = [b._unrestrictedGetObject() for b in result]
    for event in events:
        migrate_event(event, site)


def main(app):
    for sitename in SITES:
        site = app[sitename]
        setSite(site)
        migrate_events(site)


if 'app' in locals():
    main(app)

