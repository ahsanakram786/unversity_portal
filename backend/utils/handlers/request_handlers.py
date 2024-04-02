from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class DRHandler:

    def authenticate_rest_call(self, allowed_methods):
        def decorator(view):
            @api_view(allowed_methods)
            @permission_classes([IsAuthenticated])
            def wrapper(request, *args, **kwargs):
                try:
                    response = view(request, *args, **kwargs)
                except Exception as ex:
                    response = Response(data={
                        'error': str(ex)
                    })
                return response

            return wrapper

        return decorator

    def public_rest_call(self, allowed_methods):
        def decorator(view):
            @api_view(allowed_methods)
            @permission_classes([AllowAny])
            def wrapper(request, *args, **kwargs):
                try:
                    response = view(request, *args, **kwargs)
                except Exception as ex:
                    response = Response(data={
                        'error': str(ex)
                    })
                return response
            return wrapper
        return decorator


class FailureResponse:
    pass


# class DecoratorHandler:
#
#     @staticmethod
#     def return_http_response(response):
#         return response
#
#     def authenticated_rest_call(self, allowed_method_list):
#         def decorator(view):
#             @api_view(allowed_method_list)
#             @permission_classes([IsAuthenticated])
#             def wrapper(request, *args, **kwargs):
#                 try:
#                     response = view(request, *args, **kwargs)
#                 except Exception as e:
#                     print(e)
#                     response = self.return_http_response(
#                         {
#                             'error': str(ex)
#                         }
#                     )
#                 return response
#
#             return wrapper
#
#         return decorator
#
#     def public_rest_call(self, allowed_method_list):
#         def decorator(view):
#             @api_view(allowed_method_list)
#             @permission_classes([AllowAny])
#             def wrapper(request, *args, **kwargs):
#                 try:
#                     response = view(request, *args, **kwargs)
#                 except Exception as e:
#                     print(e)
#                     response = self.return_http_response(
#                         FailureResponse(str(e)).return_response_object())
#                 return response
#             return wrapper
#         return decorator