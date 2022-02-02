import ftplib
import os
import shutil

"""
Created by kaha on 25 Jun 2018
Last edited by oew on 10 Mar 2021
"""
def sentinelsat_ftp_upload(output_plots_to_upload, output_plots_uploaded):
    ftp = ftplib.FTP('ftpserver.dmi.dk')
    print(ftp.getwelcome());

    # Credentials are stored in txt file not shared in the public repo.
    with open('../username_password.txt', 'r') as file:
        data = file.readlines()
        data = [d.replace('\n', '') for d in data]
    USERNAME = data[2]
    PASSWORD = data[3]

    ftpResponse = ftp.login(USERNAME, PASSWORD)
    print(ftpResponse)
    ftpResponse = ftp.cwd('upload')
    print(ftpResponse)

    upload_list = [i for i in os.listdir(output_plots_to_upload) if i.endswith('.png')]
    for upload_filename in upload_list:
        file = open(os.path.join(output_plots_to_upload, upload_filename), 'rb')
        ftpCommand = "STOR {}".format(upload_filename);
        ftpResponse = ftp.storbinary(ftpCommand, file)
        print(ftpResponse)
        print('Uploaded {}'.format(upload_filename))
        shutil.move(os.path.join(output_plots_to_upload, upload_filename), os.path.join(output_plots_uploaded, upload_filename))
    ftp.quit()