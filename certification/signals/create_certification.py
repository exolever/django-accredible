from ..models import CertificationGroup


def create_accredible_handler(*args, **kwargs):
    CertificationGroup.objects.create_group(
        **kwargs)


def delete_accredible_handler(instance, *args, **kwargs):
    group = instance.credentials.first()
    if group:
        CertificationGroup.objects.remove_group(group)


def create_credential_accredible_handler(certification_group, user_from, certification_credential, *args, **kwargs):
    CertificationGroup.objects.release_simple_credential(
        user_from=user_from,
        certification_group=certification_group,
        certification_credential=certification_credential)


def create_group_and_credentials_handler(user_from, course_name, issued_on, *args, **kwargs):
    CertificationGroup.objects.create_group_and_credentials(
        user_from=user_from,
        course_name=course_name,
        issued_on=issued_on,
        **kwargs)


def update_certification_group_handler(instance, user_from, *args, **kwargs):
    CertificationGroup.objects.update_group(
        user_from=user_from,
        certification_group=instance,
        **kwargs)
