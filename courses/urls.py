from django.urls import path
from .views import CourseCreateView, CourseDetailView, CourseListView, CourseUpdateView, CourseDeleteView, SearchView, CourseListView, CourseDetailsView


app_name = 'courses'

urlpatterns = [

    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('update/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
    path('search/', SearchView.as_view(), name='search'),
    path('detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('apicourselist/', CourseListView.as_view()),
    path('apicoursedetail/<int:pk>/', CourseDetailsView.as_view())


]
