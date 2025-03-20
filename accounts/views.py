
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, Group, Order, WithdrawalRequest
from .serializers import UserProfileLimitedSerializer, GroupSerializer, OrderSerializer, WithdrawalRequestSerializer, UserProfileWithdrawalRequestSerializer
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
from .serializers import UserKycDetailsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import UserProfile, Wallet  # Import the Wallet model
from django.db.models import F
from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    else: # Explicitly show all when search is empty
        pass # live_profiles already contains all live profiles
    serializer = UserProfileLimitedSerializer(live_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    else: # Explicitly show all when search is empty
        pass # demo_profiles already contains all demo profiles
    serializer = UserProfileLimitedSerializer(demo_profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):

    orders = Order.objects.all().order_by('-created_at')
    search= request.query_params.get('search')
    order_status = request.query_params.get('order_status')
    order_type = request.query_params.get('order_type')
    order_time_str = request.GET.get('order_time')
    if search:
        orders = orders.filter(
            Q(order_id__icontains=search) |
            Q(order_status__icontains=search) |
            Q(order_user_id__icontains=search) |
            Q(order_company_name__icontains=search) |
            Q(order_type__icontains=search)
        )
    else:
        pass
    if order_status:
        orders = orders.filter(order_status=order_status)

    if order_type:
        orders = orders.filter(order_type=order_type)

    if order_time_str:
        try:
            order_time = datetime.strptime(order_time_str, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date=order_time) # Filtering based on created_at__date
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=400)
    
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_customer_details(request, customer_id):  # Updated function name
    """Updates the wallet_total_amount and group for a UserProfile."""
    try:
        customer = UserProfile.objects.get(pk=customer_id)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileLimitedSerializer(customer, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def withdrawal_requests_list(request):
    try:
        search = request.query_params.get('search')
        payment_type = request.query_params.get('payment_type')
        withdraw_requests = WithdrawalRequest.objects.all() # Get all requests first

        if payment_type and payment_type.lower() != "na":
            withdraw_requests = withdraw_requests.filter(type__icontains=payment_type)

        if search:
            withdraw_requests = withdraw_requests.filter(
                # Q(user_id__userprofile__name__icontains=search) |
                # Q(user_id__userprofile__email__icontains=search) |
                # Q(user_id__userprofile__phone_number__icontains=search) |
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
    



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def group_list_create(request):
    if request.method == 'GET':
        groups = Group.objects.all()

        # Filtering logic
        name = request.query_params.get('name')
        symbol = request.query_params.get('symbol')

        if name:
            groups = groups.filter(name__icontains=name)  # Case-insensitive contains
        if symbol:
            groups = groups.filter(symbol__icontains=symbol)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    if request.user.is_superuser:
        return Response({'message': 'Dashboard accessed successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You do not have permission to access this dashboard.'}, status=status.HTTP_403_FORBIDDEN)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_superuser:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh) #getting the refresh token

        response = Response({
            'message': 'Login successful',
            'access': access_token,
            'refresh': refresh_token, #sending the refresh token
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=settings.SESSION_COOKIE_SAMESITE,
        )

        return response
    elif user is not None:
        return Response({'message': 'User is not a superuser'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
import logging
logger = logging.getLogger(__name__)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_kyc_details(request, user_id):
    """Fetches user KYC details by user ID."""

    logger.info(f"Attempting to fetch KYC details for user ID: {user_id}")
    logger.info(f"User ID data type : {type(user_id)}")

    try:
        logger.info(f"Checking if UserProfile with ID {user_id} exists...")
        user_profile = UserProfile.objects.get(id=user_id)
        logger.info(f"UserProfile with ID {user_id} found.")

        serializer = UserKycDetailsSerializer(user_profile)
        logger.info(f"Serializer data: {serializer.data}")

        return Response(serializer.data)

    except UserProfile.DoesNotExist:
        logger.warning(f"UserProfile with ID {user_id} not found.")
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching user KYC details: {e}", exc_info=True)  # Log exception details
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_customer_funds(request):
    customer_id = request.data.get('customer_id')
    amount = request.data.get('amount')
    transaction_type = request.data.get('transaction_type')

    try:
        customer = UserProfile.objects.get(id=customer_id)

        if transaction_type == 'credit':
            customer.wallet_total_amount = F('wallet_total_amount') + amount
        elif transaction_type == 'debit':
            customer.wallet_total_amount = F('wallet_total_amount') - amount

        customer.save()

        # Create a new Wallet record
        Wallet.objects.create(
            user_id=customer_id,
            transaction_type=transaction_type,
            transaction_amount=amount,
            transaction_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Format the current time
            # Add other fields as needed
        )

        return Response({'message': 'Funds updated successfully.'})

    except UserProfile.DoesNotExist:
        return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wallet, UserProfile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet_transactions(request, user_id):
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        transactions = Wallet.objects.filter(user_id=user_id).order_by('-created_at')
        data = [{
            'name': user_profile.name,
            'email': user_profile.email,
            'phone_number': user_profile.phone_number,
            'wallet_total_amount': user_profile.wallet_total_amount,
            'transaction_id': transaction.trasaction_id,  
            'transaction_type': transaction.transaction_type,
            'transaction_amount': transaction.transaction_amount,
            'transaction_time': transaction.transaction_time,
        } for transaction in transactions]
        return Response(data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_trades(request, user_id): # Added user_id parameter
    """
    Retrieve trades for a specific user, joining UserProfile and Order tables.
    """

    try:
        user_profile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        orders = Order.objects.filter(order_user_id=user_profile.id)
        order_serializer = OrderSerializer(orders, many=True)
        user_serializer = UserProfileWithdrawalRequestSerializer(user_profile)

        response_data = {
            'user': user_serializer.data,
            'orders': order_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_unblock_user(request):
    user_id = request.data.get('id') 
    new_status = request.data.get('status')

    if not user_id or new_status is None:
        return Response({'message': 'Missing id or status'}, status=status.HTTP_400_BAD_REQUEST)

    user_profile = get_object_or_404(UserProfile, pk=user_id)

    if new_status not in [0, 1]:
        return Response({'message': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

    user_profile.status = new_status
    user_profile.save()

    return Response({'message': 'User status updated successfully'}, status=status.HTTP_200_OK)