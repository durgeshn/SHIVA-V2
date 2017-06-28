# import shutil
# import os, sys
#
#
#
# a = r'D:\temp\ANIMATION TEST\01_SAISON_1\13_PRODUCTION\04_EPISODES\02_Fabrication_3D\BDG100'
#
# os.environ['PROD_SERVER'] = 'D:/temp/ANIMATION TEST'
#
# for root, dirs, files in os.walk(a):
#     for name in files:
#         filePath = (os.path.join(root, name))
#     # for name in dirs:
#     #     print(os.path.join(root, name))
#         print filePath, '<---------------------------'
#         with open(filePath, 'r') as mayaRead:
#             for eachLins in mayaRead.readlines():
#                 if eachLins.startswith('file -rdi'):
#
#                     assetFile = eachLins.strip().split(' ')[-1].replace(';', '').replace('"', '')
#                     if 'rosie' in assetFile:
#                         continue
#                     print assetFile, '<---------------------'
#
#                     actualFile = assetFile.replace('R:/', 'P:/badgers_and_foxes/')
#                     newAssetFile = assetFile.replace('R:/', 'D:/temp/ANIMATION TEST/')
#
#                     if os.path.isfile(newAssetFile):
#                         continue
#                     if not os.path.isdir(os.path.dirname(newAssetFile)):
#                         os.makedirs(os.path.dirname(newAssetFile))
#
#                     print 'copy source : %s\ncopy source : %s' % (actualFile, os.path.abspath(newAssetFile))
#
#                     shutil.copyfile(actualFile, os.path.abspath(newAssetFile))
#                     print '\t\t', assetFile