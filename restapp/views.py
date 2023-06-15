from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from restapp.serializers import restseri
from .models import restmodel
from .serializers import restmodel
import math
from datetime import datetime

# Create your views here.
class restdetails(generics.GenericAPIView):
    queryset = restmodel.objects.all()
    serializer_class = restseri

    def get_details(self, pk):
        try:
            return restmodel.objects.get(pk=pk)
        except:
            return None


    def get(self, request, pk):
        details = self.get_details(pk=pk)
        if details == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(details)
        return Response({"status": "success", "data": {"details": serializer.data}})

    def delete(self, request, pk):
        details = self.get_details(pk)
        print(details)
        if details == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            details.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        details = self.get_details(pk)
        if details == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(
                details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data['updatedAt'] = datetime.now()
                serializer.save()
                return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Notes(generics.GenericAPIView):
    serializer_class = restseri
    queryset = restmodel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        notes = restmodel.objects.all()
        total_notes = notes.count()
        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
