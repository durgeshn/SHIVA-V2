@echo off
net use I: \\stor\py /PERSISTENT:YES
cd I:\
I:

I:\Python27\python.exe D:\user\durgesh.n\workspace\SHIVA-V2\farmUtils\autoPublishOnFarm.py

cd D:\
D:
mountvol I: /D
net use I: /DELETE