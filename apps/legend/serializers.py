from rest_framework import serializers
from .models import legendSite
class legendSiteSerializers(serializers.ModelSerializer):
    class Meta:
        model = legendSite
        fields = "__all__"