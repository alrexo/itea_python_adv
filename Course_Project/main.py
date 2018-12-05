import logging
import smtplib
import sys

import boto3
import requests
import time
from bs4 import BeautifulSoup

from peewee_orm import *


def get_file_url_list(url):
    current_unix_time = int(round(time.time() * 1000))
    payload = {'_': current_unix_time}
    response = requests.get(url=url, params=payload)
    soup = BeautifulSoup(response.text, features='html.parser')
    items = soup.find_all('a')
    return [item.get('href') for item in items]


def get_filename_from_url(file_url):
    return file_url.split('/')[-1]


def upload_s3_from_url(file_url, bucket_name, s3_folder):
    filename = get_filename_from_url(file_url)
    object_key = s3_folder + filename
    s3_object = boto3.resource('s3').Object(bucket_name, object_key)
    with requests.get(file_url, stream=True) as r:
        s3_object.put(Body=r.content)


def process_url(file_url, bucket_name, s3_folder):
    filename = get_filename_from_url(file_url)
    with db.atomic() as transaction:
        try:
            if not ENV.FM_DEBUG:
                """Register in DB. Registration and upload are executed as one transaction. If upload fails, 
                db registration is rolled back. There is no sense to update storage_url separately."""
                File.create(dmjl_data_source='DTCC_COMMODITIES',
                            dmjl_filename=filename,
                            dmjl_download_url=file_url,
                            dmjl_storage_url=bucket_name + '/' + s3_folder + filename)
                """Upload to S3"""
                upload_s3_from_url(file_url=file_url, bucket_name=bucket_name, s3_folder=s3_folder)
            else:
                pass
        except Exception as e:
            transaction.rollback()
            logger.info('Failed to upload {}.\n{}'.format(filename, repr(e)))
            return {'failed_file': filename}
        else:
            return {'uploaded_file': filename}


def send_email(sender, sender_pwd, recipients_string, subject, body):
    email_text = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(sender, recipients_string, subject, body)
    recipients_list = recipients_string.split(', ')
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender, sender_pwd)
        server.sendmail(sender, recipients_list, email_text)
        server.close()
    except Exception as e:
        logger.info('Failed to send email.\n{}'.format(repr(e)))


def run(**kwargs):
    file_url_list = get_file_url_list(url=kwargs.get('url'))
    db.connect()
    create_tables()
    db_files = File.select(File.dmjl_filename).tuples()
    uploaded_files = []
    failed_files = []

    for file_url in file_url_list:
        filename = get_filename_from_url(file_url)
        if (filename,) not in db_files:
            result = process_url(file_url=file_url, bucket_name=kwargs.get('bucket_name'),
                                 s3_folder=kwargs.get('s3_folder'))
            if 'uploaded_file' in result:
                uploaded_files.append(result['uploaded_file'])
            else:
                failed_files.append(result['failed_file'])
    db.close()

    if uploaded_files:
        subject = 'Notification: Files Upload'
        body = 'The files listed below have been uploaded:\n\n' + '\n'.join(uploaded_files)
        if not ENV.FM_DEBUG:
            send_email(sender=kwargs.get('sender'),
                       sender_pwd=kwargs.get('sender_pwd'),
                       recipients_string=kwargs.get('recipient'),
                       subject=subject,
                       body=body)
        logger.info(body)
    else:
        logger.info('No files to upload.')


def get_cli_params():
    if len(sys.argv) == 1:
        return True
    if len(sys.argv) == 2:
        value = sys.argv[1]
        _BOOL = {'True': True, 'False': False}
        if sys.argv[1] in _BOOL:
            return _BOOL[value]
        else:
            print("Wrong debug parameter! Must be 'True' or 'False'.")
            exit(0)
    else:
        print("Only 1 debug parameter allowed! Must be 'True' or 'False'.")
        exit(0)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(ENV.FM_LOGFILE)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    ENV.FM_DEBUG = get_cli_params()
    if not ENV.FM_DEBUG:
        logger.setLevel(logging.INFO)
        stream_handler.setLevel(logging.WARNING)

    params = dict()
    params['url'] = ENV.FM_WEBPAGE_URL
    params['bucket_name'] = ENV.FM_S3_BUCKET_NAME
    params['s3_folder'] = ENV.FM_S3_FOLDER
    params['sender'] = ENV.FM_EMAIL_SENDER
    params['sender_pwd'] = ENV.FM_EMAIL_SENDER_PWD
    params['recipient'] = ENV.FM_EMAIL_RECIPIENT
    logger.debug('Parameters are set. Starting while cycle.')
    logger.info('Run started.')
    while True:
        try:
            run(**params)
            logger.debug('Run cycle completed')
            time.sleep(10)
        except KeyboardInterrupt:
            inp = input('Quit program? (Y/N): ')
            if inp.upper() in ['Y', 'YES']:
                logger.info('Run finished.')
                print('Program exit')
                exit(1)
            else:
                continue
        except Exception as e:
            logger.info(repr(e))
