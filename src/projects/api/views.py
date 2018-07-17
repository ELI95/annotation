from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, status

from projects.models import Project
from .serializers import (
    ProjectSerializer,
    ProjectInlineUserSerializer,
    ProjectInlineVerifySerializer,
    ProjectTargetSerializer,
    ProjectReleaseSerializer,
    ProjectResultURLSerializer,
)
from tasks.api.serializers import TaskSerializer
from accounts.api.permissions import IsOwnerOrReadOnly, IsStaff
from accounts.api.users.serializers import UserInlineSerializer, EditContributorsSerializer


User = get_user_model()


class ProjectAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    """
    get:
        【任务管理】 获取所有状态为“进行中”的公有任务列表

    post:
        【任务管理】 新建任务
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProjectSerializer

    passed_id = None
    search_fields = ('project_type', 'founder__email')
    ordering_fields = ('project_type', 'timestamp')
    filter_fields = ('project_type',)

    def get_queryset(self, *args, **kwargs):
        project_id = [x.id for x in Project.objects.filter(private=False) if x.project_status == 'in progress']
        projects = Project.objects.filter(pk__in=project_id)
        return projects

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(founder=self.request.user)


class ProjectAPIDetailView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    """
    get:
        【任务管理】or【任务广场】 获取任务详情

    put:
        【任务管理】 编辑任务

    patch:
        【任务管理】 编辑任务

    delete:
        【任务管理】 删除任务
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProjectInlineUserSerializer
    queryset = Project.objects.all()
    lookup_field = 'id'

    def validate_status(self):
        project_id = self.kwargs.get("id", None)
        project = Project.objects.get(id=project_id)
        if project.verify_status in ['unreleased', 'verification failed']:
            return True

    def put(self, request, *args, **kwargs):
        if self.validate_status():
            return self.update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not allowed here"}, status=400)

    def patch(self, request, *args, **kwargs):
        if self.validate_status():
            return self.update(request, *args, **kwargs)
        else:
            return Response({"detail": "Not allowed here"}, status=400)

    def delete(self, request, *args, **kwargs):
        if self.validate_status():
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"detail": "Not allowed here"}, status=400)


class ProjectReleaseView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    """
    get:
        【任务管理】 获取任务详情

    put:
        【任务管理】 发布任务（只有状态为未发布和未通过的任务可以进行发布操作）
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProjectReleaseSerializer
    queryset = Project.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        project = Project.objects.get(id=project_id)
        if project.verify_status in ['unreleased', 'verification failed']:
            project.verify_status = 'verifying'
            project.save()
            return self.get(self, request, *args, **kwargs)
        else:
            return Response({"detail": "Not allowed here"}, status=400)


class ContributorsListView(generics.ListAPIView, mixins.UpdateModelMixin):
    """
    get:
        【参与任务】 获取当前任务的标注人列表

    put:
        【参与任务】 参与或退出任务
            若当前用户不在标注人列表中，通过put方法参与该任务；若当前用户在标注人列表中，通过put方法退出该任务
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserInlineSerializer

    search_fields = ('email', 'full_name')
    ordering_fields = ('email', 'full_name')

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        if project_id is None:
            return User.objects.none()
        project = Project.objects.get(id=project_id)
        return project.contributors.all()

    def put(self, request, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        project = Project.objects.get(id=project_id)
        user = request.user
        if user in project.contributors.all():
            project.contributors.remove(user)
            return Response({"message": "You have successfully exited the project!"}, status=200)
        else:
            project.contributors.add(user)
            return Response({"message": "You have successfully entered the project!"}, status=200)


class ProjectEditContributorsView(generics.ListAPIView, mixins.UpdateModelMixin):
    """
    get:
        【成员管理】 获取任务的标注人列表

    put:
        【成员管理】 添加或删除标注人
            获取用户id，若该用户不在标注人列表中，通过put方法在标注人列表在添加该用户；
            若该用户在标注人列表中，通过put方法从标注人列表中删除该用户
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = EditContributorsSerializer

    search_fields = ('email', 'full_name')
    ordering_fields = ('email', 'full_name')

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        if project_id is None:
            return User.objects.none()
        project = Project.objects.get(id=project_id)
        return project.contributors.all()

    def put(self, request, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        project = Project.objects.get(id=project_id)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        if user is None:
            return Response({"message": "User does not exist"}, status=400)
        if user in project.contributors.all():
            project.contributors.remove(user)
            return Response({"message": "User has successfully exited the project!"}, status=200)
        else:
            project.contributors.add(user)
            return Response({"message": "User has successfully entered the project!"}, status=200)


class ProjectVerifyListView(generics.ListAPIView):
    """
    get:
        【任务审核】 获取状态为“审核中”的任务列表
    """
    Permission_classes = [IsStaff]
    serializer_class = ProjectSerializer

    search_fields = ('project_type', 'founder__email')
    ordering_fields = ('project_type', 'timestamp')
    queryset = Project.objects.filter(verify_status='verifying')


class ProjectVerifyDetailView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    """
    get:
        【任务审核】 获取审核中的任务详情

    put:
        【任务审核】 修改审核状态为“通过”或“不通过”
    """
    Permission_classes = [IsStaff]
    serializer_class = ProjectInlineVerifySerializer

    def get_object(self, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        project = get_object_or_404(Project, id=project_id)
        return project

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.verify_status == 'verifying':
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        elif instance:
            return Response({"message": "Verification is not allowed"}, status=400)
        else:
            return Response({"message": "Project not exists"}, status=400)

    def perform_update(self, serializer):
        serializer.save(verify_staff=self.request.user)


class ProjectTargetDetailView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    """
    get:
        【任务管理】 获取任务目标

    put:
        【任务管理】 更改任务目标

    patch:
        【任务管理】 更改任务目标
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProjectTargetSerializer
    queryset = Project.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProjectResultView(generics.ListAPIView):
    """
    get:
        【任务管理】 获取任务结果详情
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer

    search_fields = ('contributor', 'label')
    ordering_fields = ('contributor', 'updated')

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("id", None)
        project = get_object_or_404(Project, id=project_id)
        return project.task_set.all().exclude(label='')
