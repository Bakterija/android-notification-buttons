from jnius import autoclass
from plyer.facades import Notification
from plyer.platforms.android import activity, SDK_INT

def return_intent(text):
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    intent = Intent(text)
    return intent

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))

class AndroidNotification(Notification):
    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def _notify(self, **kwargs):
        PythonService = autoclass('org.renpy.android.PythonService')
        this = PythonService.mService

        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))

        noti = NotificationBuilder(activity)

        Pend = autoclass('android.app.PendingIntent')
        Intent = return_intent("com.example.app.ACTION_PLAY")
        Intent2 = return_intent("com.example.app.ACTION_STOP")

        pend = Pend.getBroadcast( this, 100, Intent, 0)
        pend2 = Pend.getBroadcast( this, 100, Intent2, 0)

        ## Icon integers are available at https://developer.android.com/reference/android/R.drawable.html
        noti.addAction(17301540, "Play", pend)
        noti.addAction(17301539, "Pause", pend2)

        noti.setContentTitle(AndroidString( kwargs.get('title').encode('utf-8')))
        noti.setContentText(AndroidString( kwargs.get('message').encode('utf-8')))
        noti.setTicker(AndroidString( kwargs.get('ticker').encode('utf-8')))

        noti.setSmallIcon(icon)
        noti.setAutoCancel(True)
        self.noti = noti

        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(0, noti)


def instance():
    return AndroidNotification()
