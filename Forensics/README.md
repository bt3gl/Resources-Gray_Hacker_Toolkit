# Forensics


## Disk Forensics

### Basic useful CLI tools:

#### ps
Show the processes for all users (a), displaying the process's user/ownser (u), and the processes that are not attached to a terminal (x):

```shell
$ ps aux
```

Display the full listing of all processes (useful for finding underisable processes):

```shell
$ ps ef
```

#### lsof

Display a specific pricess in more details, by displaying the files and ports associated with that process.
```shell
$ lsof -p
```

Display processes running form or acessing files that have been unlinked: 

```shell
$ lsof +L1
```

#### find

```shell
$ find / -uid 0
```

### arp

Display all MAC to IP address mapping of the system (useful for finding addresses of systems that are not part of the network.

```shell
$ arp -a
```


Others: uptime, free, df.


### dd

### strings

```shell
$ strings /tmp/mem.dump | grep BOOT_
$ BOOT_IMAGE=/vmlinuz-3.5.0-23-generic
```



### scalpel

### TrID

### binwalk

### foremost

### ExifTool

### dff

### CAINE

### The Sleuth Kit


----------

## Memory Forensics

### memdump



### Volatility: Analysing Dumps

* [Lots of material on Volatility and Memory Forensics here](volatility.md)
* [On OSX Memory Forensics](osx_memory_forensics.md)



## Scripts

#### PDFs
Tools to test a PDF file:

- pdfid
- pdf-parser



## References

* [File system analysis](http://wiki.sleuthkit.org/index.php?title=FS_Analysis)
* [TSK Tool Overview](http://wiki.sleuthkit.org/index.php?title=Mactime)
