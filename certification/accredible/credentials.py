import requests
import logging
import datetime

from django.conf import settings
from django.utils import timezone

from pyaccredible.client import AccredibleWrapper
from dateutil import parser

from ..signals_define import accredible_certification_created
logger = logging.getLogger('accredible')


BATCH_SIZE = 10


def convert_to_datetime(issued_on):
    issued_on_dt = None
    if isinstance(issued_on, datetime.date) or isinstance(issued_on, datetime.datetime):
        issued_on_dt = issued_on
    else:
        issued_on_dt = parser.parse(issued_on)
    return issued_on_dt


def parse_group_response(group, data, participants_by_email):
    for data_credential in data:
        email = data_credential['recipient']['email']
        user = participants_by_email.get(email)
        credential = group.credentials.filter(user_id=user).first()
        if credential:
            parse_simple_response(credential, data_credential)


def parse_simple_response(credential, data):
    credential.accredible_id = data['id']
    credential.status = settings.CERTIFICATION_CH_STATUS_GENERATED
    credential.issued_on = data['issued_on']
    credential.accredible_url = data['url']
    credential.image = data['certificate']['image']['preview']
    credential.badge = data['badge']['image']['preview']
    credential.seo_image = data['seo_image']
    credential.save()
    generate_pdf_credential(credential)
    accredible_certification_created.send(
        sender=credential.__class__,
        user=credential.user,
        course_name=credential.group.name,
        group=credential.group,
    )


def get_participants(credentials):
    return [(credential.user_name, credential.user_email) for credential in credentials]


def get_participants_by_email(credentials):
    return {credential.user_email: credential.user.pk for credential in credentials}


def create_group_credential(credentials, instructor_name=None, accredible_id=None, issued_on=None):
    client = AccredibleWrapper(key=settings.ACCREDIBLE_API_KEY, server=settings.ACCREDIBLE_SERVER_URL)
    group = credentials.first().group
    group_id = group.accredible_id if accredible_id is None else accredible_id
    issued_on = issued_on if issued_on is not None else timezone.now().date()

    participants = get_participants(credentials)
    participants_by_email = get_participants_by_email(credentials)

    total_credentials = len(participants)
    index = 0
    while(index < total_credentials):
        end_index = index + BATCH_SIZE
        if end_index >= total_credentials:
            end_index = total_credentials

        data = {
            'participants': participants[index:end_index],
            'group_id': group_id,
            'issued_on': convert_to_datetime(issued_on),
        }
        if instructor_name:
            data['custom_attrs'] = {
                'instructor_name': instructor_name,
            }

        response = client.credential_create_bulk(**data)
        index = end_index

        if response.status_code == requests.codes.ok:
            logger.info('Accredible.credentials.create_group_credential: {}'.format(group.name))

            if 'errors' in response.json().keys():
                logger.error('Accredible.credentials.create_group_credential: {}'.format(response.json()['errors']))
            else:
                parse_group_response(
                    group, response.json()['credentials'],
                    participants_by_email)
        else:
            logger.error('Accredible.credentials.create_group_credential: {}'.format(group.name))
            response.raise_for_status()


def create_simple_credential(credential, instructor_name):
    client = AccredibleWrapper(key=settings.ACCREDIBLE_API_KEY, server=settings.ACCREDIBLE_SERVER_URL)
    data = {
        'name': credential.user_name,
        'email': credential.user_email,
        'group_id': credential.group.accredible_id,
        'issued_on': timezone.now().date(),
        'custom_attrs': {
            'instructor_name': instructor_name,
        },
    }
    response = client.credential_create(**data)
    if response.status_code == requests.codes.ok:
        parse_simple_response(credential, response.json()['credential'])
    else:
        response.raise_for_status()


def generate_pdf_credential(credential):
    client = AccredibleWrapper(key=settings.ACCREDIBLE_API_KEY, server=settings.ACCREDIBLE_SERVER_URL)
    response = client.generate_pdf(credential.accredible_id)
    if response.status_code != requests.codes.ok:
        logger.error('Accredible.credentials.generate_pdf: {}'.format(credential))
        response.raise_for_status()
