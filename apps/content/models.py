from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .storage import fs


class Content(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    file = models.FileField(_('file'), max_length=255, upload_to='file', db_index=True)
    content_type = models.CharField(_('content type'), max_length=100, db_index=True, editable=False)
    upload_date = models.DateTimeField(_('upload date'), auto_now=True, db_index=True)
    size = models.IntegerField(_('size'), db_index=True, editable=False)

    class Meta:
        db_table = 'content'
        ordering = ('-upload_date',)
        verbose_name = _('content')
        verbose_name_plural = _('content')

    def __str__(self):
        return self.file.name

    def get_absolute_url(self):
        return self.file.url

    @property
    def is_image(self):
        return 'image' in self.content_type

    def save(self, *args, **kwargs):
        self.content_type = self.file.file.content_type
        self.size = self.file.size
        return super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Content)
def set_delete(sender, instance, **kwargs):
    fs.delete(instance.file.file.grid_id)
