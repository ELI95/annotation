from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView as OriginAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .permissions import AnonPermissionOnly
from .serializers import UserRegisterSerializer, PhoneNumberOrEmailCheckSerializer
from utils.api import APIView, validate_serializer, CSRFExemptAPIView


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class LoginAPIView(OriginAPIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        qs = User.objects.filter(
                Q(email__iexact=email) |
                Q(phone_number__iexact=phone_number)
            ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)


class PhoneNumberOrEmailCheck(APIView):
    @validate_serializer(PhoneNumberOrEmailCheckSerializer)
    def post(self, request):
        """
        check phone number or email is duplicate
        """
        data = request.data
        result = {
            "phone_number": False,
            "email": False
        }
        if data.get("phone_number"):
            result["phone_number"] = User.objects.filter(phone_number=data["phone_number"]).exists()
        if data.get("email"):
            result["email"] = User.objects.filter(email=data["email"].lower()).exists()
        return self.success(result)
