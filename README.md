# googlephotos
Scripts for helping with google photos


## set_mtime.py

Google photos needs to know the date a picture was taken in order to upload it to the correct time on your google photos account.
Unfortunately not all digital cameras support adding EXIF data to pictures with the creation time.  Not all video formats support the time either.
The modified time is not always reliable, since that could just be the date your data was copied off a memory card.  

Google Photos seems to know about and use the mtime as part of the upload process if EXIF data is missing.  It's much more convenient working with 
modified time because it requires no special tooling (exiftool) to set in the file, and you can just use touch to set it:

`touch -m -t YYYYMMDDHHMM.SS <filename>`

I have owned several cameras and mobiles in the time before I enabled automatic uploads to Google Photos.  Most devices have consistent ways of 
naming the data files, and many of them incorporate the date in the file name.  Forms encountered include:

IMG_YYYYMMDD_HHMMSS.jpg  
PXL_YYYYMMDD_HHMMSS.jpg  
VID_YYYYMMDD_HHMMSS.AVI  
YYYY-MM-DD_HH.MM.SS.jpg  
etc...

and so on.  set_mtime is an attempt to capture all these formats, and apply a touch on the mtime of each file to make the mtime match the time
in the name.

You can use this script to walk a series of directories, find media files and change their modified times.  The script will abort if it finds files
whos names it doesn't recognise.  You should then either fix the regexes or remove the files from the set of files to upload to Google Photos 
somehow.


