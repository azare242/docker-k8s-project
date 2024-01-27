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
                print(f"Server {server.address} Is Alive")
                server.success_count += 1
                server.save()
            else:
                print(f"Server {server.address} Is Dead")
                server.failure_count += 1
                server.last_failure = now()
                server.save()
        except requests.RequestException:
            print(f"Server {server.address} Is Dead")
            
            server.failure_count += 1
            server.last_failure = now()
            server.save()
            