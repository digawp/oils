from django.db import models
from mptt import models as mptt_models


class Subject(mptt_models.MPTTModel):
    name = models.CharField(max_length=128)
    parent = mptt_models.TreeForeignKey('self', null=True, blank=True,
            related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']
