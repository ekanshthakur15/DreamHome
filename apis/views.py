from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.

class StaffView(APIView):
    
    def post(self, request):
        serializer = StaffSerializer(data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def get(self, request, staffno):
        staff = Staff.objects.filter(staffno = staffno).first()
        serializer = StaffSerializer(staff)
        return Response(serializer.data)
    
class BranchCreateView(APIView):
    def post(self, request):
        serializer = BranchSerializer(data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnerCreateView(APIView):
    def post(self, request):
        serializer = OwnerManageSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCreateView(APIView):
    def post(self, request):
        serializer = ClientRentalSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyCreateView(APIView):
    def post(self, request):
        serializer = PropertySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaseCreateView(APIView):
    def post(self, request):
        serializer = LeaseSerializer(data = request.data)
        if serializer.is_valid():
            pno = serializer.validated_data['pno']
            cno = serializer.validated_data.get('cno')
            rdate = serializer.validated_data.get('rdate')
            fdate = serializer.validated_data.get('fdate')
            if rdate >= fdate:
                return Response({"error":"rdate should be before "}, status= status.HTTP_400_BAD_REQUEST)

            try:
                property = Property.objects.get(pnumber = request.data['pno'])
            except Property.DoesNotExist:
                return Response(status= status.HTTP_404_NOT_FOUND)

            if property.isavailable == 1:
                property.isavailable = 0
                property.save()
                invoice = Invoice.objects.create(pno = pno, cno = cno)
                invoice.save()
                serializer.save()
            else:
                return Response({"error": "property not available"},status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BranchDetailView(APIView):
    def get(self, request, br_id):
        list = []
        branch = Branches.objects.get(bnumber = br_id)
        queryset = Staff.objects.filter(brno = br_id)
        for staff in queryset:
            staff_data = {
                "staff_no": staff.staffno,
                "staff_name": staff.fname,
                "position": staff.sposition
            }
            list.append(staff_data)
        data = {
            "branch_no":br_id,
            "branch_address": branch.baddress,
            "mobile1": branch.mobileno1,
            "mobile2": branch.mobileno2,
            "mobile3": branch.mobileno3,
            "staff": list
        }
        return Response(data, status= status.HTTP_200_OK)
    

class PropertyListView(APIView):

    def post(self, request, format=None):

        ptype = request.data.get('ptype', None)
        city = request.data.get('city', None)
        rent = request.data.get('rent', None)
        rooms = request.data.get('rooms', None)
        address = request.data.get('paddress', None)
        pin = request.data.get('pin', None)
        pnumber = request.data.get('pnumber', None)

        q_filters = Q(isavailable = 1)
        if ptype:
            q_filters &= Q(ptype__icontains=ptype)
        if city:
            q_filters &= Q(city__icontains=city)
        if rent:
            q_filters &= Q(rent__lte=rent)
        if rooms:
            q_filters &= Q(rooms =rooms)
        if address:
            q_filters &= Q(paddress_icontains = address)
        if pin:
            q_filters &= Q(paddress_icontains = pin)
        if pnumber:
            q_filters &= Q(paddress_icontains = pnumber)
        
        properties = Property.objects.filter(q_filters)

        list = []
        for property in properties:
            data = {
                "pnumber":property.pnumber,
                "ptype": property.ptype,
                "rent": property.rent,
                "address": property.paddress,
                "isavailable": property.isavailable,
                "rooms": property.rooms
            }
            list.append(data)
        return Response(list, status= status.HTTP_200_OK)


class PropertyDetailView(APIView):
    def get(self, request, pnum):
        property = Property.objects.get(pnumber = pnum)
        try:
            clients = Invoice.objects.filter(pno = pnum)
        except Invoice.DoesNotExist:
            print('No clients so far')
        
        clients_info = []
        if clients:
            for client in clients:
                cinfo = Clientrental.objects.get(cnumber = client.cno)
                info = {
                    "cnumber": client.cno.cnumber,
                    "cname":cinfo.cname,
                    "comment": client.comments
                }
                clients_info.append(info)
        data = {
            "pnumber" : property.pnumber,
            "ptype": property.ptype,
            "paddress": property.paddress,
            "rent": property.rent,
            "clients" : clients_info,
        }
        return Response(data)
    

class BranchListView(APIView):
    def get(self, request):
        try:
            queryset = Branches.objects.all()
        except Branches.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        branch_names = []
        for branch in queryset:
            data = {
                "bnumber": branch.bnumber,
                "baddress": branch.baddress,
                "city": branch.city
            }
            branch_names.append(data)

        return Response(branch_names, status=status.HTTP_200_OK)
    
class CommentView(APIView):
    def put(self, request):
        try:
            invoice = Invoice.objects.get(pno = request.data['pno'], cno = request.data['cno'])
        except Invoice.DoesNotExist:
            return Response({"error": "no invoice found"}, status= status.HTTP_404_NOT_FOUND)
        invoice.update(comment = request.data["comment"])
        invoice.save()
        return Response(status= status.HTTP_200_OK)