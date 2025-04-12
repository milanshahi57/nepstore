from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from nepmart.models import Order

@login_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')[:10]  # Get 10 most recent orders
    return render(request, 'custom_admin/dashboard.html', {'orders': orders})

@csrf_exempt
@require_POST
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.ORDER_STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
