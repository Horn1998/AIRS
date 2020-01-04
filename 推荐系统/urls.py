from django.contrib import admin
from django.urls import path
from main import text_classify_init, text_classify_reverse
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tci/', text_classify_init),       #�ı������ʼ��
    path('tcr/', text_classify_reverse)     #�ı�����ָ���ʼ״̬
]
