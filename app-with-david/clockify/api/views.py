from rest_framework.response import Response
from rest_framework.decorators import api_view
from workspace.models import Project
from .serializers import ProjectSerializers


@api_view(['GET'])
def getData(request):
    # person = {'name':'Hanka'}
    projects = Project.objects.all()
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addProject(request):
    serializer = ProjectSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
