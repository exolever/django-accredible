from celery import Task
from django.apps import apps

from ..accredible import groups


class DeleteAccredibleGroupTask(Task):
    ignore_result = True

    def run(self, group_id):
        CertificationGroup = apps.get_model('certification', 'CertificationGroup')
        group = CertificationGroup.objects.get(pk=group_id)
        groups.delete_group(group)
        group.delete()
