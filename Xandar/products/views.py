from operations.views import add_to_cart
from django.shortcuts import render
from django.views.generic.list import ListView
from core.models import Product, ProductImage, Attribute, CATEGORY_CHOICES, SUB_CATEGORY_CHOICES
from django.db.models import Q
from django.views.generic import DetailView
#from operations.cart import add_cart
from operations.views import add_wishlist_item
from django.http import HttpResponse
from django.contrib import messages
from core.models import Wishlist
from core.get_data import *


class ProductListView(ListView):
	model = Product
	template_name = "products/product_list.html"


# paginate_by = 3


	def get_queryset(self, *args, **kwargs):


		qs = Product.objects.all()
		query = self.request.GET.get("name", None)
		query2 = self.request.GET.get("product_category", None)
		query3 = self.request.GET.get("sub_category", None)
		query4 = self.request.GET.get("price", None)
		# query5 = self.request.GET.get("description", None)

		if query is not None:
			qs = qs.filter(
				Q(name__icontains=query)
			)

		if query2 is not None:
			qs = qs.filter(
				Q(product_category__category__iexact=query2)
			)

		if query3 is not None:
			qs = qs.filter(
				Q(product_category__sub_category__iexact=query3)
			)

		if query4 is not None:
			qs = qs.filter(
				Q(price__lte=query4)
			)

		return qs


	def get_context_data(self, **kwargs):

		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		context['image'] = []
		context['values'] = self.request.GET
		context['categories'] = CATEGORY_CHOICES
		context['sub_categories'] = SUB_CATEGORY_CHOICES

		for object in context['object_list']:
			print(object)
			object.image = ProductImage.objects.filter(product=object).first().image

		return context

class ProductDetailView(DetailView):
	model = Product
	template_name = 'products/product_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['attributes'] = []
		context['images'] = []
		context['reviews'] = []
		try:
			product = Product.objects.get(slug=self.kwargs['slug'])
			product.count += 1
			product.save()
		except Product.DoesNotExist:
			pass
		attributes = get_dataset(Attribute, product=context['object'])
		for attribute in attributes:
			context['attributes'].append(attribute)
		for image in get_dataset(ProductImage, product_id=context['object']):
			context['images'].append(image)
		for review in get_dataset(Review, product=context['object']):
			context['reviews'].append(review)
		if self.request.user.is_authenticated:
			try:
				OrderedItems.objects.get(customer=self.request.user, title=context['object'].name)
				context['can_post_review'] = True
			except OrderedItems.DoesNotExist:
				context['can_post_review'] = False
		else:
			context['can_post_review'] = False
		return context


def product_add_wishlist_cart(request, pk):
	action_perfomed = request.GET.get('button')
	quantity = int(request.GET.get('quantity'))
	if action_perfomed == 'wishlist':
		return HttpResponse(add_wishlist_item(request, pk))
	else:
		return HttpResponse(add_to_cart(request, pk, quantity))


def filter_by(request):
	category = request.GET.get("category", None)
	price_min = request.GET.get("priceless", None)
	price_max = request.GET.get("pricegreat", None)

	try:
		category = ProductCategory.objects.get(category=category)
		product_filter = category.product_set.all()
		if not product_filter:
			messages.error(request, "No search results found")
		return render(request, "products/product_list.html", {'filtered_item': product_filter})

	except ProductCategory.DoesNotExist:
		product_filter = []
		messages.error(request, f"{category}Category is empty")

	if price_min and price_max:
		product_filter = Product.objects.filter(
			Q(price__lt=price_min) & Q(price__gt=price_max)
		)

	else:
		if not price_min:
			price_min = Product.objects.all().order_by('price')[0].price
		if not price_max:
			price_max = Product.objects.all().order_by('-price')[0].price

		product_filter = Product.objects.filter(
			Q(price__lt=price_min) | Q(price__gt=price_max)
		)

	#
	#
	# if category:
	#  request.session['category'] = category
	#  try:
	#     category = ProductCategory.objects.get(category=category)
	#     product_filter = category.product_set.all()
	#  except ProductCategory.DoesNotExist:
	#     messages.error(request, "Invalid Category Provided")
	#     return render(request, "products/product_list.html")
	#  if not product_filter:
	#     messages.error(request, f"{category} category is empty ")

	# if price_min and price_max:
	#  request.session['pricemin'] = price_min
	#  request.session['pricemax'] = price_max
	#  try:
	#     product_filter = Product.objects.filter(price__lte=price_min, price__gte=price_max)
	#  except Product.DoesNotExist:
	#     messages.error(request,f"No Product Found whose price less than {price_min} and price greater than {price_max}")
	#     return render(request, "products/product_list.html")
	# elif price_min:
	#  request.session['pricemin'] = price_min
	#  try:
	#     product_filter = Product.objects.filter(price__lte=price_min)
	#  except Product.DoesNotExist:
	#     messages.error(request, f"No Product Found whose price less than {price_min}")
	#     return render(request, "products/product_list.html")
	# elif price_max:
	#  request.session['pricemax'] = price_max
	#  try:
	#     product_filter = Product.objects.filter(price__gte=price_max)
	#  except Product.DoesNotExist:
	#     messages.error(request, f"No Product Found whose price greater than {price_max}")
	#     return render(request, "products/product_list.html")
	# else:
	#  HttpResponse("Invalid Option Given")

	return render(request, "products/product_list.html", {'filtered_item': product_filter})




