from Xandar import settings
from core.models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_ordered=False)
            return {'count': len(cart.cartitems_set.all())}
        except Cart.DoesNotExist:
            return {'count': 0}
    else:
        request.session[settings.CART_SESSION_ID] = request.session.get(settings.CART_SESSION_ID, {})
        if request.session[settings.CART_SESSION_ID] is None:
            return {'count': 0}
        return {'count': len(request.session[settings.CART_SESSION_ID])}
