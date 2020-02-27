from rest_framework import routers, serializers, viewsets
from .models import Customer,Profession,Datesheet,Documents

class CustomerSerializer(serializers.ModelSerializer):
    date_sheet=serializers.StringRelatedField()
    class Meta:
        model = Customer
        fields = ['id','name', 'address', 'profession', 'date_sheet','active']
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','description']
class DatesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datesheet
        fields = ['id','description','historical_date']
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['id','dtype','doc_number','customer']
