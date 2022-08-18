from django.shortcuts import render, redirect
from django.views import View
from .forms import CourseForm
from .models import Course
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.mixins import IsCreatorMixin
from rest_framework import viewsets
from .serializers import CourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CourseCreateView(LoginRequiredMixin, View):
    template_name = 'courses/courses.html'
    form = CourseForm

    def get(self, request):
        context = {
            "form": self.form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid:
            course = form.save(commit=False)
            course.created_by = self.request.user
            course.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class CourseListView(LoginRequiredMixin, View):
    model = Course
    template_name = 'courses/course_list.html'

    def get(self, request):
        context = {
            "courses": Course.objects.filter(created_by=self.request.user),
        }
        return render(request, self.template_name, context=context)


class CourseUpdateView(LoginRequiredMixin, IsCreatorMixin, View):
    template_name = "courses/course_update.html"

    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        form = CourseForm(instance=course)
        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = CourseForm(request.POST)
        course = Course.objects.get(id=pk)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid:
            form.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class CourseDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = "courses/course_del.html"

    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        course.delete()
        return redirect('courses:course_list')


class SearchView(View):
    template_name = "courses/course_list.html"

    def get(self, request):
        query = request.GET.get("query")

        courses = Course.objects.filter(title__icontains=query)
        context = {
            "courses": courses,

        }
        return render(request, self.template_name, context=context)


class CourseDetailView(View):
    Model = Course
    template_name = "courses/course_detail.html"

    def get(self, request, pk):
        context = {
            "course": Course.objects.get(id=pk)
        }
        return render(request, self.template_name, context=context)


class CourseListView(APIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        print(Course.objects.all())
        serializer = CourseSerializer(Course.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailsView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)

        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
