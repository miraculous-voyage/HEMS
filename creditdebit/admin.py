from django.contrib import admin

from .models import Creditdebit
from .models import Dashboard
from .models import Inv_equ

admin.site.register(Creditdebit)
admin.site.register(Dashboard)
admin.site.register(Inv_equ)
