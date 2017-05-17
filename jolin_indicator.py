import pygtk

APPINDICATOR_ID = 'myappindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, 'whatever', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(gtk.Menu())
    gtk.main()

if __name__ == "__main__":
    main()