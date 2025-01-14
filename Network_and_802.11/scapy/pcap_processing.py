#!/usr/bin/env python

__author__ = "bt3gl"


import re
import zlib
import cv2
from scapy.all import *

PIC_DIR = '/home/user/Desktop/pictures'
FACES_DIR = '/home/user/Desktop/faces'
PCAP = 'http_witp_jpegs.cap'

# split the headers using regular expression
def get_http_headers(http_payload):
    try:
        # split the headers off if it is HTTP traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]
        headers = dict(re.findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', headers_raw))
    except:
        return None
    if 'Content-Type' not in headers:
        return None

    return headers

# determine whether we received an image in the HTTP response
def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if 'image' in headers['Content-Type']:
            # grab the image type and image body
            image_type = headers['Content-Type'].split('/')[1]

            image = http_payload[http_payload.index('\r\n\r\n')+4:]

            # if we detect compression decompress the image
            # attempt to decompress it before returning the image
            # type and the raw image buffer
            try:
                if 'Content-Encoding' in headers.keys():
                    if headers['Content-Encoding'] == 'gzip':
                        image = zlib.decompress(image, 16+zlb.MAX_WBITS)
                    elif headers['Content-Encoding'] == 'deflate':
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None
    return image, image_type



# facial detection code
def face_detect(path, file_name):
    img = cv2.imread(path)
    # apply a classifier that is trained in advanced for detecting faces
    # in a front-facing orientation
    cascade = cv2.CascadeClassifier('/home/bytegirl/Desktop/haarcascade_upperbody.xml')
    # returns retangle coordinates that correspnd to where the face
    # was detected in the image.
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    if len(rects) == 0:
        return False
    rects[:, 2:] += rects[:, :2]
    # highlight the faces in the image
    # draw a green retangle over the area
    for x1, y1, x2, y2 in rects:
        cv2.retangle(img, (x1, y1), (x2, y2), (127, 255,0), 2)
        # write out the resulting image
        cv2.imwrite('%s/%s-%s' % (FACES_DIR, PCAP, file_name), img)
    return True


def http_assembler(PCAP):
    carved_images = 0
    faces_detected = 0
    a = rdpcap('/home/temp/' + PCAP)

    # scapy automatically separate each TCP session into a dictionay
    sessions = a.sessions()
    for session in sessions:
        http_payload = ''
        for packet in sessions[session]:
            try:
                # we use that wand then filter out only HTTP traffic and then concatenate
                # the payload of all the HTTP traffic into a single buffer
                # (the same as Wiresahk Follow TCP Stream)
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # reassemble the stream
                    http_payload += str(packet[TCP].payload)
            except:
                pass

            # after we have the HTTP data assembled we pass it off to our HTTP
            # header, parsing function, which will allow us to inspect the headers
            headers = get_http_headers(http_payload)
            if headers is None:
                continue

            # after we validade that, we receive an image back in an HTTP response, we
            # extract the raw image and return the image type and the binary body of
            # the image itself
            image, image_type = extract_image(headers, http_payload)
            if image is not None and image_type is not None:
                # store the images
                file_name = '%s-pic_carver_%d.%s' %(PCAP, carved_images, image_type)
                fd = open('%s/%s' % (PIC_DIR, file_name), 'wb')
                fd.write(image)
                fd.close()
                carved_images += 1

                # now attempt face detection
                try:
                    # path the file for the facial detection routine
                    result = face_detect('%s/%s' %(PIC_DIR, file_name), file_name)
                    if result is True:
                        faces_detected += 1
                except:
                    pass
    return carved_images, faces_detected


if __name__ == '__main__':
    carved_images, faces_detected = http_assembler(PCAP)
    print "Extracted: %d images" % carved_images
    print "Detected: %d faces" % faces_detected

