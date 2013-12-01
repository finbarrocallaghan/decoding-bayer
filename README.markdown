replicating out.3.log on a ContourNext, but on second attempt.. have to plug out and back in again to get something sensible..

on first attempt I can get all the readings from the device, but it ends up getting stuck, and then 

    <<< 'ABC;\x024R|10|^^^Glucose|5.2|mmol/L^P||F/M0/T1||201302080218\r\x174B\r\n\x00'
    *** '\x024R|10|^^^Glucose|5.2|mmol/L^P||F/M0/T1||201302080218\r\x174B\r\n'
    >>> '\x06'
    <<< 'ABC<\x025R|11|^^^Glucose|10.9|mmol/L^P||F/M0/T1||201302081017\r\x177E\r\n'
    Traceback (most recent call last):
      File "main.py", line 28, in <module>
        for rec in bc.sync():
      File "/home/finn/diab_/glucodump/glucodump/contourusb.py", line 92, in sync
        data = self.dev.read()
      File "/home/finn/diab_/glucodump/glucodump/usbcomm.py", line 83, in read
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
| ACK           | x06


and after that, i'm not too sure.. :)
