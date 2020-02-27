from django.shortcuts import render
from .models import Customer,Profession,Datesheet,Documents
from .serializers import CustomerSerializer,ProfessionSerializer,DatesheetSerializer,DocumentSerializer
from rest_framework import viewsets
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['name', 'address']
    filterset_fields = ('name',)
    ordering_fields = '__all__'
    lookup_field='name'
    ordering=('-id')
    authentication_classes=[TokenAuthentication,]


    def get_queryset(self):
        address=self.request.query_params.get('address',None)
        if self.request.query_params.get('active')=='False':
            status=False
        else:
            status=True
        if address:
            customers=Customer.objects.filter(address__icontains=address,active=status)
        else:
            customers=Customer.objects.filter(active=status)
        return customers


    # def list(self,request,*args,**kwargs):
    #     customers=self.get_queryset()
    #     serlializer=CustomerSerializer(customers,many=True)
    #     return Response(serlializer.data)
    def retrieve(self,request,*args,**kwargs):
        obj=self.get_object()
        serializer=CustomerSerializer(obj)
        return Response(serializer.data)
    def create(self,request,*args,**kwargs):
        data=request.data
        customer=Customer.objects.created(name=data['name'],address=data['address'],data_sheet_id=data['date_shaeet'])
        profession=Profession.objects.get(id=data['profession'])

        customer.profession.add(profession)
        customer.save()

        serializer=CustomerSerializer(customer)
        return Response(serlializer.data)

    def update(self,request,*args,**kwargs):
        customer=self.get_object()
        data=request.data
        customer.name=data['name']
        customer.address=data['address']
        customer.date_sheet_id=data['datasheet']

        profession=Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    def partial_update(self,request,*args,**kwargs):
        customer=self.get_object()
        customer.name=request.data.get('name',customer.name)
        customer.address=request.data.get('address',customer.address)
        customer.date_sheet_id=request.data.get('date_sheet',customer.date_sheet)

        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self,request,*args,**kwargs):
        customer=self.get_object()
        customer.delete()

        return Response('Object removed')

    @action(detail=True)
    def deactivated(self,request,**kwargs):
        customer=self.get_object()
        customer.active=False
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    @action(detail=False)
    def deactivate_all(self,request,**kwargs):
        customers=self.get_queryset()
        customers.update(active=False)
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self,request,**kwargs):
        customers=self.get_queryset()
        customers.update(active=True)


        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)

    @action(detail=False,methods=['POST'])
    def change_status(self,request,**kwargs):
        status=True if request.data['active']=='True' else False
        customers=self.get_queryset()
        customers.update(active=status)

        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)



class ProfessionViewSet(viewsets.ModelViewSet):
    queryset=Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes=[TokenAuthentication,]
class DatesheetViewSet(viewsets.ModelViewSet):
    queryset=Datesheet.objects.all()
    serializer_class = DatesheetSerializer
    permission_classes=[AllowAny,]
class DocumentViewSet(viewsets.ModelViewSet):
    queryset=Documents.objects.all()
    serializer_class = DocumentSerializer
