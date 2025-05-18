from django.db import models

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} on {self.visit_date.strftime('%Y-%m-%d %H:%M')}"
