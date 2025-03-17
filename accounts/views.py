# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated  # Combined imports
# from rest_framework.response import Response
# from .models import UserProfile
# from .serializers import UserProfileLimitedSerializer
# from django.shortcuts import render
# from rest_framework import status
# from django.contrib.auth import authenticate, login
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings
# from .models import Group
# from .serializers import GroupSerializer
# from .models import Order
# from .serializers import OrderSerializer
# from .models import WithdrawalRequest
# from .serializers import WithdrawalRequestSerializer
# from django.db.models import Q



# @api_view(['GET'])
# def live_user_profiles(request):
#     """
#     Returns a JSON response of live UserProfile objects with limited fields.
#     """
#     live_profiles = UserProfile.objects.filter(user_type='live')
#     print("Live Profiles Count:", live_profiles.count())  # Check the count
#     for profile in live_profiles:
#         print(profile) # Print each profile object
#     serializer = UserProfileLimitedSerializer(live_profiles, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def demo_user_profiles(request):
#     """
#     Returns a JSON response of demo UserProfile objects with limited fields.
#     """

#     demo_profiles = UserProfile.objects.filter(user_type='demo')
#     serializer = UserProfileLimitedSerializer(demo_profiles, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def dashboard_view(request):
#     if request.user.is_superuser:
#         return Response({'message': 'Dashboard accessed successfully'}, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'You do not have permission to access this dashboard.'}, status=status.HTTP_403_FORBIDDEN)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(request, username=username, password=password)

#     if user is not None and user.is_superuser:
#         # login(request, user)
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)


#         response = Response({
#         'message': 'Login successful',
#         'access': access_token,
#         'refresh': str(refresh), #add this line
#     }, status=status.HTTP_200_OK)

#         response.set_cookie(
#             'refresh_token',
#             str(refresh),
#             httponly=True,
#             secure=settings.SESSION_COOKIE_SECURE,
#             samesite=settings.SESSION_COOKIE_SAMESITE,
#         )

#         return response
#     elif user is not None:
#         return Response({'message': 'User is not a superuser'}, status=status.HTTP_403_FORBIDDEN)
#     else:
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


# @api_view(['GET'])
# def group_list(request):
#     """
#     List all groups.
#     """
#     if request.method == 'GET':
#         groups = Group.objects.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response(serializer.data)
    

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.all().order_by('-created_at')  # Order by creation time (descending)
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)




# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from .models import WithdrawalRequest, UserProfile
# from .serializers import WithdrawalRequestSerializer, UserProfileWithdrawalRequestSerializer

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from .models import WithdrawalRequest, UserProfile
# from .serializers import WithdrawalRequestSerializer, UserProfileWithdrawalRequestSerializer

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def withdrawal_requests_list(request):
#     try:
#         search = request.query_params.get('search')
#         payment_type = request.query_params.get('payment_type')

#         if payment_type and payment_type.lower() != "na":
#             withdraw_requests = WithdrawalRequest.objects.filter(type__icontains=payment_type)
#         else:
#             withdraw_requests = WithdrawalRequest.objects.all()

#         data = []
#         for withdraw_request in withdraw_requests:
#             status_text = ""
#             if withdraw_request.status == "1":
#                 status_text = "Payment Proceed"
#             elif withdraw_request.status == "2":
#                 status_text = "Admin Cancel"
#             elif withdraw_request.status == "0":
#                 status_text = "Requested"
#             else:
#                 status_text = "Unknown"  # Handle unexpected status values

#             data.append({
#                 "request_details": WithdrawalRequestSerializer(withdraw_request).data,
#                 "user_details": UserProfileWithdrawalRequestSerializer(UserProfile.objects.get(id=withdraw_request.user_id)).data,
#                 "status_text": status_text
#             })

#         return Response({
#             'status': 'true',
#             'message': 'Data received successfully',
#             'data': data
#         })

#     except UserProfile.DoesNotExist:
#         return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, Group, Order, WithdrawalRequest
from .serializers import UserProfileLimitedSerializer, GroupSerializer, OrderSerializer, WithdrawalRequestSerializer, UserProfileWithdrawalRequestSerializer
from django.shortcuts import render
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Added JWT authentication
def live_user_profiles(request):
    """Returns a JSON response of live UserProfile objects with limited fields."""
    search = request.query_params.get('search')
    live_profiles = UserProfile.objects.filter(user_type='live')
    if search:
        live_profiles = live_profiles.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(account_number__icontains=search)
        )
    serializer = UserProfileLimitedSerializer(live_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Added JWT authentication
def demo_user_profiles(request):
    """Returns a JSON response of demo UserProfile objects with limited fields."""
    search = request.query_params.get('search')
    demo_profiles = UserProfile.objects.filter(user_type='demo')
    if search:
        demo_profiles = demo_profiles.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(account_number__icontains=search)
        )
    serializer = UserProfileLimitedSerializer(demo_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Added JWT authentication
def group_list(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Added JWT authentication
def order_list(request):
    search = request.query_params.get('search')
    orders = Order.objects.all().order_by('-created_at')
    if search:
        orders = orders.filter(
            Q(order_id__icontains=search) |
            Q(order_status__icontains=search) |
            Q(order_user_id__icontains=search) |
            Q(order_company_name__icontains=search) |
            Q(order_type__icontains=search)
        )
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    if request.user.is_superuser:
        return Response({'message': 'Dashboard accessed successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You do not have permission to access this dashboard.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_superuser:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response({
            'message': 'Login successful',
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
        response.set_cookie(
            'refresh_token',
            str(refresh),
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
        )
        return response
    elif user is not None:
        return Response({'message': 'User is not a superuser'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def withdrawal_requests_list(request):
    try:
        search = request.query_params.get('search')
        payment_type = request.query_params.get('payment_type')
        if payment_type and payment_type.lower() != "na":
            withdraw_requests = WithdrawalRequest.objects.filter(type__icontains=payment_type)
        else:
            withdraw_requests = WithdrawalRequest.objects.all()
        if search:
            withdraw_requests = withdraw_requests.filter(
                Q(user_id__userprofile__name__icontains=search) |
                Q(user_id__userprofile__email__icontains=search) |
                Q(user_id__userprofile__phone_number__icontains=search) |
                Q(amount__icontains=search) |
                Q(type__icontains=search) |
                Q(status__icontains=search)
            )
        data = []
        for withdraw_request in withdraw_requests:
            status_text = ""
            if withdraw_request.status == "1":
                status_text = "Payment Proceed"
            elif withdraw_request.status == "2":
                status_text = "Admin Cancel"
            elif withdraw_request.status == "0":
                status_text = "Requested"
            else:
                status_text = "Unknown"
            data.append({
                "request_details": WithdrawalRequestSerializer(withdraw_request).data,
                "user_details": UserProfileWithdrawalRequestSerializer(UserProfile.objects.get(id=withdraw_request.user_id)).data,
                "status_text": status_text
            })
        return Response({
            'status': 'true',
            'message': 'Data received successfully',
            'data': data
        })
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)