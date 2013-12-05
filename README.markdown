On a ContourNext, trying to replicate:

![example dialogue](dialogue.png)


    >>> '\x04'
    1H|\^&||mLJsN1|Bayer7410^01.10\01.05\10.03^7425-3013732^00000|A=1^C=22^G=en,
    en\de\fr\it\nl\es\pt\sl\hr\da\no\fi\sv\el^I=0200^R=0^S=01^U=311^V=20600^X=05
    4070070E60180130180360070130^Y=360126099054120054252099^Z=1|490|||||P|1|2013
    1205221705
    >>> '\x06'
    no STX
    >>> '\x15'
    1H|\^&||FMmMiI|Bayer7410^01.10\01.05\10.03^7425-3013732^00000|A=1^C=22^G=en,
    en\de\fr\it\nl\es\pt\sl\hr\da\no\fi\sv\el^I=0200^R=0^S=01^U=311^V=20600^X=05
    4070070F00180130180360070130^Y=360126099054120054252099^Z=1|490|||||P|1|2013
    1205221705
    >>> '\x06'
    53|1
    >>> '\x06'
    9C|1|^^^Glucose|4.6|mmol/L^P||M0/T1||201302050040
    >>> '\x06'
    1C|2|^^^Glucose|7.1|mmol/L^P||F/M0/T1||201302050733
    >>> '\x06'
    18|3|^^^Glucose|8.2|mmol/L^P||F/M0/T1||201302051054
    >>> '\x06'
    54|4|^^^Glucose|7.9|mmol/L^P||A/M0/T1||201302060057
    >>> '\x06'
    53|5|^^^Glucose|10.5|mmol/L^P||F/M0/T1||201302060807
    >>> '\x06'
    26|6|^^^Glucose|4.9|mmol/L^P||B/M0/T1||201302061956
    >>> '\x06'
    4B|7|^^^Glucose|5.2|mmol/L^P||A/M0/T1||201302070049
    >>> '\x06'
    55|8|^^^Glucose|12.9|mmol/L^P||F/M0/T1||201302070723
    >>> '\x06'
    58|9|^^^Glucose|7.5|mmol/L^P||B/M0/T1||201302072148
    >>> '\x06'
    4B|10|^^^Glucose|5.8|mmol/L^P||F/M0/T1||201302080218
    >>> '\x06'
    Traceback (most recent call last):
      File "main.py", line 185, in <module>
        for rec in enumerate(bc.sync()):
      File "main.py", line 126, in sync
        data = self.dev.read()
      File "main.py", line 35, in read
        data = self.epin.read(self.blocksize)
      File "/usr/local/lib/python2.7/dist-packages/usb/core.py", line 300, in read
        return self.device.read(self.bEndpointAddress, size, self.interface, timeout)
      File "/usr/local/lib/python2.7/dist-packages/usb/core.py", line 670, in read
        self.__get_timeout(timeout)
      File "/usr/local/lib/python2.7/dist-packages/usb/backend/libusb1.py", line 798, in intr_read
        timeout)
      File "/usr/local/lib/python2.7/dist-packages/usb/backend/libusb1.py", line 889, in __read
        _check(retval)
      File "/usr/local/lib/python2.7/dist-packages/usb/backend/libusb1.py", line 571, in _check
        raise USBError(_str_error[ret], ret, _libusb_errno[ret])
    usb.core.USBError: [Errno 110] Operation timed out


| ASCII         | Hex
| ------------- |:-------------:
| ACK           | \x06
| NAK           | \x15
| EOT           | \x04
| Enq           | \x05


no idea why it's failing after the 10th reading is sent through.. 
