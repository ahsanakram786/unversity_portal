import json

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from courses.models import Course, Module, StudentModuleRegistration
from courses.serializers import CourseSerializer, ModuleSerializer, StudentModuleRegistrationSerializer
from utils.handlers.request_handlers import DRHandler

DR_handler = DRHandler()


# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_courses_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Set the number of items per page
    courses = Course.objects.all()
    result_page = paginator.paginate_queryset(courses, request)
    serializer = CourseSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_course_modules(request):
    course_id = request.GET.get('id', None)
    if course_id and type(int(course_id)) == int:
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        course_ = Course.objects.filter(id=course_id)
        result_page = paginator.paginate_queryset(course_, request)
        serializer = CourseSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(data={
            'message': '`course_id` of type int be provided.'
        }, status=status.HTTP_400_BAD_REQUEST)


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_module_detail(request):
    try:
        pk = request.GET.get('id', None)
        if pk and type(int(pk)) is int:
            module = Module.objects.get(pk=pk)
            serializer = ModuleSerializer(module)
            return Response(data=serializer.data)
        else:
            raise KeyError('`id` of type `int` cannot be empty.')
    except Module.DoesNotExist:
        return Response(data={
            'message': 'Module does not exist.'
        }, status=status.HTTP_404_NOT_FOUND)
    except KeyError as ke:
        return Response(data={
            'message': str(ke)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(data={
            'message': str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@DR_handler.authenticate_rest_call(allowed_methods=['GET'])
def get_student_module_register(request):
    serialize = None
    if hasattr(request.user.role, 'name') and request.user.role.name == 'STUDENT':
        try:
            student_module_regis = StudentModuleRegistration.objects.filter(student=request.user)
            serialize = StudentModuleRegistrationSerializer(student_module_regis, many=True, context={'request': request})
            return Response(data=serialize.data)
        except Exception as ex:
            message = str(serialize.errors) if serialize else str(ex)
            return Response(data={
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={
            'message': 'Unauthorized access!'
        }, status=status.HTTP_401_UNAUTHORIZED)


@DR_handler.authenticate_rest_call(allowed_methods=['POST'])
def student_module_register(request):
    user = request.user
    module_id = request.GET.get('module_id', None)
    serializer_ = None
    if hasattr(request.user.role, 'name') and user.role.name == 'STUDENT':
        try:
            data = {
                'student': user.id,
                'module': module_id
            }
            serializer_ = StudentModuleRegistrationSerializer(data=data, many=False)
            if serializer_.is_valid(raise_exception=True):
                serializer_.save()
                module_model = Module.objects.get(id=serializer_.data.get('module', None)).name
                return Response(data={
                    'message': f'Enrolled for {Module.objects.get(id=serializer_.data.get("module", None))}.'
                })
        except Exception as ex:
            message = str(serializer_.errors) if serializer_ else str(ex)
            return Response(data={
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={
            'message': 'Unauthorized access!'
        }, status=status.HTTP_401_UNAUTHORIZED)


@DR_handler.authenticate_rest_call(allowed_methods=['DELETE'])
def student_module_unregister(request):
    module_id = request.GET.get('module_id', None)
    if hasattr(request.user.role, 'name') and request.user.role.name == 'STUDENT':
        try:
            if module_id:
                student_register_ = StudentModuleRegistration.objects.filter(module_id=module_id)
                if student_register_:
                    student_register_.delete()
                    return Response(data={
                        'message': f'Un-Register from module.'
                    })
            else:
                raise Exception("`module_id` is required.")
        except Exception as ex:
            message = str(ex)
            return Response(data={
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data={
            'message': 'Unauthorized access!'
        }, status=status.HTTP_401_UNAUTHORIZED)
