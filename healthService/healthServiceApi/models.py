from django.db import models

# Create your models here.




import uuid
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'read'

    def db_for_write(self, model, **hints):

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):

        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        return True

class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255, verbose_name="Server Address")
    success_count = models.PositiveIntegerField(default=0, verbose_name="Success Count")
    failure_count = models.PositiveIntegerField(default=0, verbose_name="Failure Count")
    last_failure = models.DateTimeField(null=True, blank=True, verbose_name="Last Failure Time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")

    class Meta:
        verbose_name_plural = "Servers"
        ordering = ['-created_at']

    def __str__(self):
        return f"Server {self.address} - Success: {self.success_count}, Failures: {self.failure_count}"

