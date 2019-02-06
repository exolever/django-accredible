from django.test import TestCase, override_settings
from django.conf import settings
from django.core.management import call_command

from unittest.mock import patch
from dateutil.parser import parse

from consultant.faker_factories import FakeConsultantFactory
from relation.faker_factories.faker_factory_consultant_role import FakeConsultantRoleFactory
from relation.faker_factories import FakeConsultantRoleGroupFactory
from test_utils.test_case_mixins import UserTestMixin
from test_utils.mock_mixins import MagicMockMixin

from .models import CertificationGroup


class CertificationTest(MagicMockMixin, UserTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        call_command('create_update_hub')
        self.create_user()

    @override_settings(ACCREDIBLE_ENABLED=True)
    @patch('certification.tasks.CreateAccredibleConsultantRoleGroupTask.apply_async')
    def test_certifications_credentials_consultant_role(self, mock_task):
        # PREPARE DATA
        consultant_role_group = FakeConsultantRoleGroupFactory.create(
            created_by=self.user,
            _type=settings.CERTIFICATION_CH_GROUP_CONSULTANT_ROLE_TRAINER,
            issued_on=parse('2010-10-10'))
        consultant = FakeConsultantFactory.create()
        FakeConsultantRoleFactory.create(
            consultant=consultant,
            certification_group=consultant_role_group,
        )

        # DO ACTION
        group = CertificationGroup.objects.create_consultant_role_group_and_credentials(
            user_from=consultant_role_group.created_by,
            consultant_role_group=consultant_role_group,
            course_name='ExO Certif')

        # ASSERTS
        consultant_role_group.refresh_from_db()
        self.assertTrue(mock_task.called)
        self.assertEqual(group.created_by, self.user)
        self.assertEqual(CertificationGroup.objects.count(), 1)
        self.assertEqual(consultant_role_group.certification_groups.count(), 1)
        self.assertEqual(self.get_mock_arg(mock_task, 'group_id'), group.pk)
        self.assertTrue(
            consultant.user.hubs.filter(
                hub___type=settings.EXO_HUB_CH_TRAINER).exists())
        self.assertTrue(
            consultant.user.has_perm(
                settings.WORKSHOP_FULL_PERMS_ADD_WORKSHOP))
