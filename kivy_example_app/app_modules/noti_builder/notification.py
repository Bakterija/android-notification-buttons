from jnius import autoclass, detach
from plyer.platforms.android import activity, SDK_INT
from threading import Thread
from time import sleep

# try:
#     PythonActivity = autoclass('org.renpy.android.PythonActivity')
#     PythonService = autoclass('org.renpy.android.PythonService')
# print('DDDDDD, activity', PythonActivity)
Intent = autoclass('android.content.Intent')
aString = autoclass('java.lang.String')
aInt = autoclass('java.lang.Integer')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
Drawable = autoclass("{}.R$drawable".format(activity.getPackageName()))
Pend = autoclass('android.app.PendingIntent')
NotificationManager = autoclass('android.app.NotificationManager')
Vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
MediaPlayer = autoclass('android.media.MediaPlayer')
AudioManager = autoclass('android.media.AudioManager')

# this = PythonService.mService
this = activity
print('DDDDDD, activity', this)
if SDK_INT > 22:
    Action_Builder = autoclass('android.app.Notification$Action$Builder')

def return_intent(intentName):
    intent = Intent(intentName)
    return intent


class AndroidNotification:
    def __init__(self):
        self.noti = NotificationBuilder(activity)

    def _get_notification_service(self):
        if not hasattr(self, '_ns'):
            self._ns = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        return self._ns

    def notify(self, **kwargs):
        noti = self.noti
        icon = getattr(Drawable, kwargs.get('icon_android', 'icon'))

        ## Icon integers are available at https://developer.android.com/reference/android/R.drawable.html
        if SDK_INT >= 16:
            for bAction, bName, bIcon, bCallback in kwargs['buttons']:
                intent = return_intent(kwargs['intentName']+bAction)
                pend = Pend.getBroadcast( this, 100, intent, 0)
                if SDK_INT < 23:
                    noti.addAction(bIcon, aString(bName), pend)

                else:
                    action = Action_Builder(bIcon, aString(bName), pend)
                    action = action.build()
                    noti.addAction(action)

        noti.setContentTitle(aString( kwargs.get('title').encode('utf-8')))
        noti.setContentText(aString( kwargs.get('message').encode('utf-8')))
        noti.setTicker(aString( kwargs.get('ticker').encode('utf-8')))
        if kwargs['subtext']:
            noti.setSubText(aString( kwargs.get('subtext').encode('utf-8')))
        if kwargs['ongoing']:
            noti.setOngoing(True)
        if kwargs['autocancel']:
            noti.setAutoCancel(True)
        if kwargs['sound']:
            self.play_media(kwargs['sound'])
        if kwargs['vibrate']:
            if type(kwargs['vibrate']) in (int, float):
                Vibrator.vibrate(int(1000 * kwargs['vibrate']))
            else:
                for i,x in enumerate(kwargs['vibrate']):
                    kwargs['vibrate'][i] = x*1000
                Vibrator.vibrate(kwargs['vibrate'][i], -1)

        noti.setSmallIcon(icon)

        if SDK_INT >= 16:
            noti = noti.build()
        else:
            noti = noti.getNotification()

        self._get_notification_service().notify(kwargs['id'], noti)

    def remove(self, id):
        self._get_notification_service().cancel(id)

    def play_media(self,source):
        def releaser_thread(player,duration):
            sleep(duration)
            mPlayer.release()
            detach()
        mPlayer = MediaPlayer()
        mPlayer.setDataSource(source)
        mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
        mPlayer.prepare()
        duration = mPlayer.getDuration()/1000+1
        mPlayer.start()
        Thread(target=releaser_thread,args=(mPlayer,duration)).start()

def instance():
    return AndroidNotification()
