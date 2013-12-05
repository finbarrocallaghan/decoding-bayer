#!/usr/bin/env python
import re
import time
import usb


class USBComm(object):

  blocksize = 64
  
  def __init__(self, **kw):
    dev = usb.core.find(idVendor=0x1a79, idProduct=0x7410)
    self.dev = dev

    config = dev.get_active_configuration()
    interface = usb.util.find_descriptor(config, bInterfaceClass=usb.CLASS_HID)

    if dev.is_kernel_driver_active(interface.index):
        dev.detach_kernel_driver(interface.index)

    interface.set_altsetting()
    usb.util.claim_interface(dev, interface)
    self.interface = interface

    self.epin = usb.util.find_descriptor(interface, bEndpointAddress=0x83)
    self.epout = usb.util.find_descriptor(interface, bEndpointAddress=0x04)

  def close(self):
    usb.util.release_interface(self.dev, self.interface)
    usb.util.dispose_resources(self.dev)

  def read(self):
    result = []
    while True:
      data = self.epin.read(self.blocksize)
      dstr = data.tostring()
      assert dstr[:3] == 'ABC'
      #print '<<<', repr(dstr)
      result.append(dstr[4:data[3]+4])

      if data[3] != self.blocksize-4:
        #print "in here!!"
        break
    return ''.join(result)

  def write(self, data):
    remain = data
    while remain:
      now = remain[:self.blocksize-4]
      remain = remain[self.blocksize-4:]
      self.epout.write('\0\0\0' + chr(len(now)) + now) # + ('\0' * (self.blocksize - 4 - len(now))))

class FrameError(Exception):
  pass

class BayerCOMM(object):
  "Framing for Bayer meters"

  framere = re.compile('\x02(?P<check>(?P<recno>[0-7])(?P<text>[^\x0d]*)'
                       '\x0d(?P<end>[\x03\x17]))'
                       '(?P<checksum>[0-9A-F][0-9A-F])\x0d\x0a')

  mode_establish = object
  mode_data = object()
  mode_precommand = object()
  mode_command = object()

  def __init__(self, dev):
    self.dev = dev
    self.currecno = None
    self.state = self.mode_establish

  def checksum(self, text):
    checksum = hex(sum(ord(c) for c in text) % 256).upper().split('X')[1]
    return ('00' + checksum)[-2:]

  def checkframe(self, frame):
    match = self.framere.match(frame)

    if not match:
      raise FrameError("Couldn't parse frame", frame)

    recno = int(match.group('recno'))
    if self.currecno is None:
      self.currecno = recno
    
    if recno + 1 == self.currecno:
      return None
    
    if recno != self.currecno:
      raise FrameError("Bad recno, got %r expected %r" %
                       (recno, self.currecno),
                       frame)

    checksum = self.checksum(match.group('check'))
    if checksum != match.group('checksum'):
      raise FrameError("Checksum error: got %s expected %s" %
                       (match.group('checksum'), checksum),
                       frame)

    self.currecno = (self.currecno + 1) % 8
    #print 'text: %r' % match.group('text')

    return match.group('text')
    
  def sync(self):
    """
    Sync with meter and yield received data frames
    """
    tometer = '\x04'
    result = None
    foo = 0

    while True:
      print '>>>', repr(tometer)
      self.dev.write(tometer)

      if result is not None and self.state == self.mode_data:
        #print 'inhere\n\n'
        yield result

      result = None

      #print self.state

      data = self.dev.read()
      #print data

      #   #print self.state
      #   #print self.mode_establish

      #print '***', data
      #   #print 'data end!\n\n\n'

      #   if self.state == self.mode_establish:
      #     if data[-1] == '\x15':
      #         #got a <NAK>, send <EOT>
      #         tometer = chr(foo)
      #         foo += 1
      #         foo %= 256
      #         continue

      #     #print "\n"
      #     #print data[-1]
      #     #print "\n"
      #     
      #     if data[-1] == '\x05':
      #       # got an <ENQ>, send <ACK>
      #       tometer = '\x06'
      #       self.currecno = None
      #       continue

      if self.state == self.mode_data:
        if data[-1] == '\x04':
          # got an <EOT>, done
          self.state = self.mode_precommand
          print 'should break'
          break

      #print data
      stx = data.find('\x02')

      if stx != -1:
        # got <STX>, parse frame
        try:
          print data[stx:]
          result = self.checkframe(data[stx:])
          tometer = '\x06'
          self.state = self.mode_data
        except FrameError, e:
          #print e
          print "Couldn't parse, <NAK>'"
          tometer = '\x15'
      else:
        # Got something we don't understand, <NAK> it
        print 'no STX'
        tometer = '\x15'


#uc = USBComm(idVendor=0x1a79, idProduct=0x7410)

uc = USBComm()
bc = BayerCOMM(uc)

for rec in enumerate(bc.sync()):
  pass

uc.close()



