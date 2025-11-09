from django.db import models


class Site(models.Model):
    """
    Represents a physical location/datacenter
    """
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sites'
        ordering = ['name']

    def __str__(self):
        return self.name


class RackConfiguration(models.Model):
    """
    Stores complete rack layouts for a site
    """
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='rack_configurations',
        db_column='site_id'
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    config_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rack_configurations'
        unique_together = [['site', 'name']]
        ordering = ['name']
        indexes = [
            models.Index(fields=['site']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.site.name} - {self.name}"
