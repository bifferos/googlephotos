# googlephotos
Scripts for helping with google photos

## takeout.py

Google photos provides no way to know if a given photo has already been
uploaded.  You can only attempt to upload it again which often happens
faster if it's already there.  Takeout.py indexes a takeout and allows you
to quickly lookup whether individual files are present in the takeout (and
therefore in your google account) or not.


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
whos names it doesn't recognise.  You should then either fix the regexes or remove the files from the set of files to upload to Google Photos.

## pdf_to_webm.py

Google photos has no support for pdf files.  Converting them to webm can be done with this utility.


## wav_to_mp4.py

Google photos has no support for audio files.  The easiest way to deal with these is to create an mp4 from the audio file.  Just so you have something
to look at while the audio is playing you can add a screen with the original file name and the parent directory.  wav_to_mp4.py scans a directory 
for .wav files and when it finds them creates an mp4 using lossless audio (alac codec) that's playable on most players.


## nodts.py

My LG TV doesn't play any videos with DTS audio.  This removes the track and replaces it with ac3, renaming the filename appending _ac3 so I 
know what's what.

`./nodts.py myvideo.avi`

Will write out myvideo_ac3.avi


## photos.py

Attempt to use the API to recover metadata.  This is useless because google don't provide the checksum.

## oauth.py

Code to get the all important refresh_token entry in the credentials file.  When you create a set of API credentials you don't initially get this.
