from django.contrib import admin

# Register your models here.
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
  list_display = ('title', 'featured_product')

admin.site.register(Collection)