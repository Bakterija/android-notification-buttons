from kivy.uix.scrollview import ScrollView

class ScrollView192(ScrollView):
    '''This is a scrolview that works properly in kivy 1.9.1'''

    def on_scroll_move(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return False

        touch.push()
        touch.apply_transform_2d(self.to_local)
        if self.dispatch_children('on_scroll_move', touch):
            touch.pop()
            return True
        touch.pop()

        rv = True

        # By default this touch can be used to defocus currently focused
        # widget, like any touch outside of ScrollView.
        touch.ud['sv.can_defocus'] = True

        uid = self._get_uid()
        if not uid in touch.ud:
            self._touch = False
            return self.on_scroll_start(touch, False)
        ud = touch.ud[uid]

        # check if the minimum distance has been travelled
        if ud['mode'] == 'unknown':
            if not self.do_scroll_x and not self.do_scroll_y:
                # touch is in parent, but _change expects window coords
                touch.push()
                touch.apply_transform_2d(self.to_local)
                touch.apply_transform_2d(self.to_window)
                self._change_touch_mode()
                touch.pop()
                return
            ud['dx'] += abs(touch.dx)
            ud['dy'] += abs(touch.dy)
            if ((ud['dx'] > self.scroll_distance and self.do_scroll_x) or
                    (ud['dy'] > self.scroll_distance and self.do_scroll_y)):
                ud['mode'] = 'scroll'

        if ud['mode'] == 'scroll':
            if not touch.ud['sv.handled']['x'] and self.do_scroll_x \
                    and self.effect_x:
                width = self.width
                if touch.ud.get('in_bar_x', False):
                    dx = touch.dx / float(width - width * self.hbar[1])
                    self.scroll_x = min(max(self.scroll_x + dx, 0.), 1.)
                    self._trigger_update_from_scroll()
                else:
                    if self.scroll_type != ['bars']:
                        self.effect_x.update(touch.x)
                if self.scroll_x < 0 or self.scroll_x > 1:
                    rv = False
                else:
                    touch.ud['sv.handled']['x'] = True
                # Touch resulted in scroll should not defocus focused widget
                touch.ud['sv.can_defocus'] = False
            if not touch.ud['sv.handled']['y'] and self.do_scroll_y \
                    and self.effect_y:
                height = self.height
                if touch.ud.get('in_bar_y', False):
                    dy = touch.dy / float(height - height * self.vbar[1])
                    self.scroll_y = min(max(self.scroll_y + dy, 0.), 1.)
                    self._trigger_update_from_scroll()
                else:
                    if self.scroll_type != ['bars']:
                        self.effect_y.update(touch.y)
                if self.scroll_y < 0 or self.scroll_y > 1:
                    rv = False
                else:
                    touch.ud['sv.handled']['y'] = True
                # Touch resulted in scroll should not defocus focused widget
                touch.ud['sv.can_defocus'] = False
            ud['dt'] = touch.time_update - ud['time']
            ud['time'] = touch.time_update
            ud['user_stopped'] = True
        return rv
