from celery import shared_task
import requests
from django.utils.timezone import now
from .models import Server

@shared_task
def check_server_health():
    for server in Server.objects.all():
        _address = server.address if "http://" in server.address or "https://" in server.address else f"http://{server.address}"
        try:
            response = requests.get(_address)
            if response.status_code == 200:
                print(f"Server {_address} Is Alive")
                server.success_count += 1
                server.save()
            else:
                print(f"Server {_address} Is Dead [Status = {response.status_code}]")
                server.failure_count += 1
                server.last_failure = now() 
                server.save()
        except requests.RequestException as e:
            print(f"Server {_address} Is Dead [Error = {str(e)}]")
            server.failure_count += 1
            server.last_failure = now()
            server.save()
            