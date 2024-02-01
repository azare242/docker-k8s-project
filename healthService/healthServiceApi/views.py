from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Server
from .serializers import ServerSerializer
# Create your views here.


from prometheus_client import Counter, Histogram, Gauge
from django.db import OperationalError


http_requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
http_requests_failed = Counter('http_requests_failed', 'Failed HTTP Requests', ['method', 'endpoint', 'status'])

http_request_duration_seconds = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds', ['endpoint'])

servers_total = Gauge('servers_total', 'Total number of server objects in the database')


def track_metrics(endpoint):
    def decorator(func):
        def wrapper(*args, **kwargs):
            http_requests_total.labels(method=request.method, endpoint=endpoint).inc()
            with http_request_duration_seconds.labels(endpoint=endpoint).time():
                try:
                    response = func(*args, **kwargs)
                    if response.status_code >= 400:
                        http_requests_failed.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
                    return response
                except OperationalError:
                    http_requests_failed.labels(method=request.method, endpoint=endpoint, status=500).inc()
                    return Response(status=500)
        return wrapper
    return decorator

@api_view(["GET"])
@track_metrics('ping')
def ping(request):
    return Response(status=200)

@api_view(["GET"])
@track_metrics('ready')
def ready(request):
    try:
        servers = Server.objects.all()
        servers_total.set(servers.count())
        return Response(status=200)
    except OperationalError:
        servers_total.set(0)
        return Response(status=500)




@api_view(["GET"])
def ping(request):
    return Response(status=200)


@api_view(["GET"])
def ready(request):
    try:
        _ = Server.objects.all()
        return Response(status=200)
    except:
        http_requests_failed.inc(1)
        return Response(status=500)

@api_view(["GET"])
def start(request):
    return Response(status=200)




@api_view(["POST", "GET"])
def submit_server_or_check_server(request):
    http_requests_total.inc(1)
    if request.method == "GET":
        server_id = request.query_params.get('id')
        try:
            server = Server.objects.get(id=server_id)
            serializer = ServerSerializer(server)
            return Response(serializer.data)
        except Server.DoesNotExist:
            http_requests_failed.inc(1)
            return Response(status=404)
    else:
        try:
           
            address = request.data['address']
            server = Server(address=address)
            server.save()
            servers_total.inc(1)
            return Response(status=201)
        except:
            http_requests_failed.inc(1)
            return Response(status=400)
            
    

@api_view(["GET"])
def check_all_servers(request):
    http_requests_total.inc(1)
    try:
        servers = Server.objects.all()
        serializer = ServerSerializer(servers, many=True)
        return Response(serializer.data)
    except:
        http_requests_failed.inc(1)
        return Response(status=500)