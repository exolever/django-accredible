from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from model_utils.models import TimeStampedModel

from ..conf import settings


class CertificationCredential(TimeStampedModel):
    group = models.ForeignKey(
        'CertificationGroup', related_name='credentials',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='certifications',
        on_delete=models.CASCADE)
    accredible_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=settings.CERTIFICATION_CH_STATUS,
        default=settings.CERTIFICATION_CH_STATUS_DEFAULT)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    issued_on = models.DateField(blank=True, null=True)
    accredible_url = models.URLField(blank=True, null=True)
    seo_image = models.URLField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    badge = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        return self.group.name

    @property
    def description(self):
        return self.group.description

    @property
    def pdf(self):
        return '{}/{}.pdf'.format(settings.ACCREDIBLE_PDF_HOST, self.accredible_id)
