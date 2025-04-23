from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    
    path('', views.login_page, name='login_page'),
    path('login/', views.login_page, name='login_page'),
    path('dashboard/', views.dashboard_html_view, name='dashboard_html'),

    path('api/login/', views.login_view, name='login'),
    path('api/dashboard/', views.dashboard_view, name='dashboard'),

    path('api/live-user-profiles/', views.live_user_profiles, name='live_user_profiles'),
    path('api/demo-user-profiles/', views.demo_user_profiles, name='demo_user_profiles'),
    path('api/groups/', views.group_list_create, name='group-list-create'),
    path('api/orders/', views.order_list, name='order-list'),
    path('api/withdrawal-requests/', views.withdrawal_requests_list, name='withdrawal-request-list'),
    path('api/customers/<int:customer_id>/update_customer_details/', views.update_customer_details, name='update_customer_details'),
    path('api/user-kyc/<int:user_id>/', views.get_user_kyc_details, name='get_user_kyc_details'),
    path('api/update-customer-funds/', views.update_customer_funds, name='update_customer_funds'),
    path('api/wallet-transactions/<str:user_id>/', views.get_wallet_transactions, name='get_wallet_transactions'),
    path('api/user-trades/<int:user_id>/', views.user_trades, name='user_trades'),
    path('api/block-unblock/', views.block_unblock_user, name='block_unblock_user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/groups/<int:group_id>/', views.update_group, name='update_group'), 
    path('api/groups/<int:group_id>/delete/', views.delete_group, name='delete_group'), 

]

# public function closePositionFunction($orderId, $closePrice)
# {
#     $tempData = DjangoUserOrder::where("order_id", $orderId)->get();
#     $orderId1 = count($tempData) > 0 ? $tempData[0]->id : $orderId;

#     $userOrder = DjangoUserOrder::find($orderId1);
#     if ($userOrder->order_status == 'close') return false;

#     $symbol = $userOrder->order_company_name;
#     $orderType = $userOrder->order_type;
#     $margin = floatval($userOrder->margin);
#     $orderQty = floatval($userOrder->order_quantity);
#     $marginPerLot = $orderQty > 0 ? $margin / $orderQty : 0.0;

#     // Fetch open orders
#     $openBuyOrders = DjangoUserOrder::where("order_user_id", $userOrder->order_user_id)
#         ->where("order_type", 'BUY')
#         ->where("order_status", 'open')
#         ->where("order_company_name", $symbol)
#         ->get();

#     $openSellOrders = DjangoUserOrder::where("order_user_id", $userOrder->order_user_id)
#         ->where("order_type", 'SELL')
#         ->where("order_status", 'open')
#         ->where("order_company_name", $symbol)
#         ->get();

#     // Total Buy/Sell Quantity
#     $totalBuyQty = $openBuyOrders->sum(function ($o) {
#         return floatval($o->order_quantity);
#     });

#     $totalSellQty = $openSellOrders->sum(function ($o) {
#         return floatval($o->order_quantity);
#     });

#     // Determine unhedged lots of this order
#     $hedgedQty = min($totalBuyQty, $totalSellQty);
#     $unhedgedQty = 0.0;

#     if ($orderType === 'BUY') {
#         $unhedgedQty = max(0, $totalBuyQty - $hedgedQty);
#     } elseif ($orderType === 'SELL') {
#         $unhedgedQty = max(0, $totalSellQty - $hedgedQty);
#     }

#     $thisOrderUnhedged = min($orderQty, $unhedgedQty);
#     $marginToRelease = $marginPerLot * $thisOrderUnhedged;

#     $userProfile = UserProfile::find($userOrder->order_user_id);

#     // 💸 Add Profit/Loss
#     $commonController = new CommonController;
#     $netProfit = $commonController->calculateNetProfit(
#         floatval($closePrice),
#         $orderQty,
#         floatval($userOrder->order_price),
#         $symbol,
#         $orderType
#     );

#     $userProfile->wallet_total_amount = strval(floatval($userProfile->wallet_total_amount) + $netProfit);
#     $userProfile->margin = strval(round(floatval($userProfile->margin) - $marginToRelease, 4));
#     $userProfile->save();

#     // 💼 Log Profit/Loss
#     Wallet::create([
#         'transaction_amount' => $netProfit,
#         'symbol' => $symbol,
#         'transaction_type' => "Profit/Loss",
#         'order_quanity' => $userOrder->order_quantity,
#         'transaction_time' => now(),
#         'order_type' => $orderType,
#         'user_id' => $userOrder->order_user_id,
#         'trasaction_id' => random_int(10000000000, 99999999999),
#     ]);

#     // 💸 Subtract swap if needed
#     if (floatval($userOrder->swap) != 0) {
#         $commonController->subtractWalletAmt($userOrder->order_user_id, $userOrder->swap);
#         Wallet::create([
#             'transaction_amount' => $userOrder->swap,
#             'symbol' => $symbol,
#             'order_quanity' => $userOrder->order_quantity,
#             'transaction_type' => "Swap Charges",
#             'transaction_time' => now(),
#             'order_type' => $orderType,
#             'user_id' => $userOrder->order_user_id,
#             'trasaction_id' => random_int(10000000000, 99999999999),
#         ]);
#     }

#     // 💰 Handle commission
#     $userGroup = $userProfile->group;
#     $stockDetails = Group::where("symbol", $symbol)->where("name", $userGroup)->first();

#     if ($stockDetails && ($stockDetails->commision_type == "0" || $stockDetails->commision_type == "2")) {
#         $commissionAmt = 0.0;
#         if ($stockDetails->commision_value_type == "1") {
#             $calculatedAmt = ($stockDetails->commision * floatval($userOrder->order_price)) / 100;
#             $commissionAmt = $calculatedAmt * $orderQty;
#         } else {
#             $commissionAmt = $stockDetails->commision * $orderQty;
#         }

#         $userOrder->commission += $commissionAmt;
#         $commonController->subtractWalletAmt($userOrder->order_user_id, $userOrder->commission);

#         Wallet::create([
#             'transaction_type' => "Commission",
#             'symbol' => $symbol,
#             'order_type' => $orderType,
#             'order_quanity' => $orderQty,
#             'transaction_amount' => $userOrder->commission,
#             'transaction_time' => now(),
#             'user_id' => $userOrder->order_user_id,
#             'trasaction_id' => random_int(10000000000, 99999999999),
#         ]);
#     }

#     // 🔐 Finalize order
#     $userOrder->net_profit = strval($netProfit + floatval($userOrder->swap) - floatval($userOrder->commission));
#     $userOrder->order_status = "close";
#     $userOrder->close_price = $closePrice;
#     $userOrder->save();

#     // 🧹 Reset margin if no open positions left
#     $remainingOpen = DjangoUserOrder::where("order_user_id", $userProfile->id)
#         ->where("order_status", "open")
#         ->count();

#     if ($remainingOpen == 0) {
#         $userProfile->margin = "0.0";
#         $userProfile->save();
#     }

#     return true;
# }
