# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from . import views

# urlpatterns =[
#     path('blog/', views.BlogList.as_view()),
#     path('blog/<int:pk>/', views.BlogDetail.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)


from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'blog', views.BlogViewSet)

urlpatterns =[
    path('', views.BlogView.as_view()),
    path('<int:pk>/', views.BlogDetailView.as_view()),
    path('statistic/', views.BlogStatisticsView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)