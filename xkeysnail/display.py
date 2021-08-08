# -*- coding: utf-8 -*-

import os
from i3ipc import Connection, Event
import threading

class Sway:
    def __init__(self):
        sway = Connection()
        sway.on(Event.WINDOW_FOCUS, self.on_window_focus)
        self.sway = sway
        self.class_name = ''
        t = threading.Thread(target = sway.main, args=())
        t.start()

    def get_active_window_wm_class(self):
        return self.class_name

    def on_window_focus(self, sway, event):
        class_name = event.ipc_data['container']['app_id']
        if class_name == None:
            class_name = event.ipc_data['container']['window_properties']['class']

        #TODO lock
        self.class_name = class_name

class Xorg:

    def __init__(self):
        import Xlib.display
        self.display = Xlib.display.Display()

    def get_active_window_wm_class(self):
        """Get active window's WM_CLASS"""
        current_window = self.display.get_input_focus().focus
        pair = self.get_class_name(current_window)
        if pair:
            # (process name, class name)
            return str(pair[1])
        else:
            return ""


    def get_class_name(self, window):
        """Get window's class name (recursively checks parents)"""
        try:
            wmname = window.get_wm_name()
            wmclass = window.get_wm_class()
            # workaround for Java app
            # https://github.com/JetBrains/jdk8u_jdk/blob/master/src/solaris/classes/sun/awt/X11/XFocusProxyWindow.java#L35
            if (wmclass is None and wmname is None) or "FocusProxy" in wmclass:
                parent_window = windaow.query_tree().parent
                if parent_window:
                    return self.get_class_name(parent_window)
                return None
            return wmclass
        except:
            return None

if os.getenv('XDG_SESSION_DESKTOP') == 'sway':
    _wm = Sway()
else:
    _wm = Xorg()

def get_active_window_wm_class():
    return _wm.get_active_window_wm_class()
