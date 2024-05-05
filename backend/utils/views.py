from rest_framework import status
from rest_framework.response import Response
from utils.handlers.request_handlers import DRHandler
from utils.models import ContactUs

# Create your views here.
DR_handler = DRHandler()


@DR_handler.public_rest_call(allowed_methods=['POST'])
def contact_us(request):
    data = request.data
    try:
        if data:
            is_created = ContactUs.objects.create(**data)
            if is_created:
                return Response(data={
                    'message': "Enquiry has been submitted. Our support will get back to you on this, shortly."
                })
    except Exception as ex:
        return Response(data={
            'message': str(ex)
        }, status=status.HTTP_400_BAD_REQUEST)
