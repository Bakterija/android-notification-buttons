# Android Notification Builder for Python
#### Requires [Kivy](https://kivy.org) and [Plyer](https://github.com/kivy/plyer), use [Buildozer](https://github.com/kivy/buildozer) to build android apks

Provides a simple way of building
[Android notifications](https://developer.android.com/guide/topics/ui/notifiers/notifications.html) 
with buttons with callbacks, no java knowledge required.     
Buttons allow you to control your background services while using other apps

![screenshot](https://raw.githubusercontent.com/Bakterija/android-notification-buttons/master/other/Screenshot.png "Screenshot on android 4.4 KitKat")

## How to use

#### Copy "noti_builder" folder to "service/" folder

#### Import
```python
from noti_builder.noti_builder import Notification_Builder
```
#### Instantiate
```python
nBuilder = Notification_Builder()
```

#### Set title, message, ticker
```python
nBuilder.set_title('myTitle')
nBuilder.set_message('myMessage')
nBuilder.set_ticker('Button example')
```

#### Add subtext, if required
```python
nBuilder.set_subtext(str)
```

#### Add buttons, if required
```python
## 0. Displayed button name
## 1. icon integer available at https://developer.android.com/reference/android/R.drawable.html
## 2. callback
## action= android PendingIntent action, button name will be used if not provided
nBuilder.add_button('Play', 17301540 , callback, action='Play')
```

#### Build
```python
nBuilder.build()
```

### More functions, use before .build()

#### Add vibration (seconds)
```python
nBuilder.set_vibrate(float)
```

#### Add sound (path)
```python
nBuilder.set_sound(str)
```

#### Change intent name
```python
### Default is "org.renpy.android.ACTION_"
### Buttons broadcast "intent name"+"button action",
### for example, Play button broadcasts "org.renpy.android.ACTION_Play"
nBuilder.set_intentName(str)
```

#### Remove notification
```python
nBuilder.remove_notification()
```

#### Access [android notification builder](https://developer.android.com/reference/android/app/Notification.Builder.html) directly
```python
nBuilder.javaBuilder
### For example, nBuilder.javaBuilder.setOngoing(True) will make notification ongoing
### Remember that javaBuilder is reset when nBuilder.build is called
```

#### Remove buttons
```python
nBuilder.remove_buttons()
```

#### Make unremovable
```python
nBuilder.set_ongoing(True)
```

#### Remove on touch
```python
nBuilder.set_autocancel(True)
```

### BroadcastReceivers
nBuilder creates BroadcastReceivers when buttons are added to listen for touches,     
Start/stop and get object list with
```python
nBuilder.start()
nBuilder.stop()

nBuilder.get_receivers()
### BroadcastReceivers have start/stop methods,
### control them directly by getting the list and running BroadcastReceiver methods
```
