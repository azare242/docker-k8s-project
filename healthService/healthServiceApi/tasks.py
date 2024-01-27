from celery import shared_task
import requests
from django.utils.timezone import now
from .models import Server

@shared_task
def check_server_health():
    for server in Server.objects.all():
        try:
            response = requests.get(server.address)
            if response.status_code == 200:
                server.success += 1
                server.save()
            else:
                server.failure += 1
                server.last_failure = now()
                server.save()
        except requests.RequestException:
            server.failure += 1
            server.last_failure = now()
            server.save()
            
            
            
@shared_task
def test():
    print("test completed")