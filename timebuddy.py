#!/usr/bin/env python
__author__ = 'Aldrin Navarro'

from gi.repository import Gtk
try:
    from gi.repository import AppIndicator3 as AppIndicator
except:
    from gi.repository import AppIndicator

import timelog

APPINDICATORID = 'timelogbuddy'


class TimeLogBuddyIndicator(object):

    def __init__(self, *args, **kwargs):
        self.ind = AppIndicator.Indicator.new(
            APPINDICATORID, Gtk.STOCK_INFO,
            AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
        # need to set this for indicator to be shown
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.activated = False
        self.menu = Gtk.Menu()
        last_log = timelog.get_last_log()
        label = 'Time out' if last_log['type'] == 'time in' else 'Time in'
        self.ind1, self.ind2 = ('indicator-messages-new', 'indicator-messages')
        icon = self.ind1 if last_log['type'] == 'time in' else self.ind2

        self.log_toggle_item = Gtk.MenuItem()
        self.log_toggle_item.set_label(label)
        self.log_toggle_item.connect("activate", self.handler_menu_log_toggle)
        self.log_toggle_item.show()
        self.menu.append(self.log_toggle_item)

        sep = Gtk.MenuItem()
        # sep.set_label("-----")
        sep.show()
        self.menu.append(sep)

        item = Gtk.MenuItem()
        item.set_label("Time in")
        item.connect("activate", self.handler_menu_log_in)
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Time out")
        item.connect("activate", self.handler_menu_log_out)
        item.show()
        self.menu.append(item)

        # exit app
        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_icon(icon)
        self.ind.set_menu(self.menu)

    def handler_menu_exit(self, evt):
        Gtk.main_quit()

    def handler_menu_log_toggle(self, evt):
        timelog.log()

        last_log = timelog.get_last_log()
        label = 'Time out' if last_log['type'] == 'time in' else 'Time in'
        icon = self.ind1 if last_log['type'] == 'time in' else self.ind2
        self.ind.set_icon(icon)
        self.log_toggle_item.set_label(label)

    def handler_menu_log_in(self, evt):
        timelog.log_time_in()

    def handler_menu_log_out(self, evt):
        timelog.log_time_out()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    ind = TimeLogBuddyIndicator()
    ind.main()
