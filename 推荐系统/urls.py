from django.contrib import admin
from django.urls import path
from main import text_classify_init, text_classify_reverse
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tci/', text_classify_init),       #文本分类初始化
    path('tcr/', text_classify_reverse)     #文本分类恢复初始状态
]
