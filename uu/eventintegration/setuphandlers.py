
def hide_stock_plone_event(site):
    tt = site.portal_types
    fti = tt.getTypeInfo('Event')
    fti.global_allow = False

def replace_stock_site_events_folder(site):
    if 'events' not in site.contentIds():
        return
    orig = site.get('events')
    if orig.portal_type == 'uu.eventintegration.calendar':
        return
    if len(orig.contentIds()) > 1:
        return  # do not attempt to migrate content, only fixtures
    site.manage_delObjects(['events'])
    site.invokeFactory(
        id='events',
        title='Events',
        type_name='uu.eventintegration.calendar',
        )


def install_fixups(context):
    site = context.getSite()
    hide_stock_plone_event(site)
    replace_stock_site_events_folder(site)

