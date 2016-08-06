# Android Notification Builder for Python

Provides a simple way of building
[Android notifications](https://developer.android.com/guide/topics/ui/notifiers/notifications.html) 
with buttons with callbacks, no java knowledge required.     
Buttons allow you to control your background services while using other apps

![screenshot](https://raw.githubusercontent.com/Bakterija/android-notification-buttons/master/other/Screenshot.png "Screenshot on android 4.4 KitKat")

## How to use (Python2.7)

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

#### Remove notification with
```python
nBuilder.remove_notification()
```

#### Access [android notification builder](https://developer.android.com/reference/android/app/Notification.Builder.html) directly with
```python
nBuilder.javaBuilder
### For example, nBuilder.javaBuilder.setOngoing(True) will make notification ongoing
### Remember that javaBuilder is reset when nBuilder.build is called
```

#### Remove buttons with
```python
nBuilder.remove_buttons()
```

#### Get BroadcastReceiver instance list with
```python
nBuilder.get_receivers()
```

#### Start/Stop BroadcastReceivers with
```python
nBuilder.start()
nBuilder.stop()
```

#### Make unremovable with
```python
nBuilder.set_ongoing(True)
```

#### Remove on touch with
```python
nBuilder.set_autocancel(True)
```
