
def patch_widget():
    from plone.formwidget.datetime.base import AbstractDatetimeWidget
    AbstractDatetimeWidget.ampm = True
