from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Server
from .serializers import ServerSerializer
# Create your views here.




@api_view(["GET"])
def ping(request):
    return Response(status=200)





@api_view(["POST", "GET"])
def submit_server_or_check_server(request):
    if request.method == "GET":
        server_id = request.query_params.get('id')
        try:
            server = Server.objects.get(id=server_id)
            serializer = ServerSerializer(server)
            return Response(serializer.data)
        except Server.DoesNotExist:
            return Response(status=404)
    else:
        try:
            address = request.data['address']
            server = Server(address=address)
            server.save()
            return Response(status=201)
        except:
            return Response(status=400)
            
    

@api_view(["GET"])
def check_all_servers(request):
    servers = Server.objects.all()
    serializer = ServerSerializer(servers, many=True)
    return Response(serializer.data)