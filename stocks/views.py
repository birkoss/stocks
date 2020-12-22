import json
import requests

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import ShareForm
from .models import Share, Stock, StockValue


def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/login.html")

    stocks = []

    # stocks = Stock.objects.all()(share__user=request.user).annotate(total_shares=Sum('share__amount'))

    for stock in Stock.objects.all():
        shares = Share.objects.filter(user=request.user, stock=stock)
        total_shares = 0
        total_buy = 0
        
        stock_value = StockValue.objects.filter(stock=stock).order_by("-date_added").first()

        last_value = 0
        if stock_value is not None:
            last_value = stock_value.value

        for share in shares:
            total_buy += share.amount * share.value
            total_shares += share.amount

        stocks.append({
            "stock": stock,
            "total_shares": total_shares,
            "total_buy": total_buy,
            "total_value": total_shares * last_value,
            "stock_value": stock_value,

            "shares": shares,
        })

    return render(request, "core/home.html", {
        "stocks": stocks
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def edit_share(request, share_id=None):
    share = None

    if share_id:
        share = get_object_or_404(Share, pk=share_id)

        if share.user != request.user:
            return redirect('share/archive')

    if request.method == "POST":
        form = ShareForm(request.POST)

        if form.is_valid():
            if share_id is None:
                share = Share(user=request.user)

            share.amount = form.cleaned_data['amount']
            share.value = form.cleaned_data['value']
            share.stock = form.cleaned_data['stock']
            share.save()

            return redirect(
                reverse(
                    'share/edit',
                    args=[share.id]) + "?status=" + ("updated" if share_id else "created")  # nopep8
            )

    elif share_id:
        form = ShareForm(initial={
            'amount': share.amount,
            'value': share.value,
            'stock': share.stock,
        })
    else:
        form = ShareForm()

    return render(request, 'stocks/share/edit.html', {
        'form': form,
        'button': ('Edit' if share_id else 'Create'),
        'title': ('Edit an existing share' if share_id else 'Create a new share'),  # nopep8
    })



def parse(request):

    stocks = Stock.objects.all()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    total_added = 0

    for stock in stocks:
        page = requests.get("https://query2.finance.yahoo.com/v7/finance/options/" + stock.code, headers=headers)
        
        data = json.loads(page.content)

        price = data['optionChain']['result'][0]['quote']['regularMarketPrice']

        # Compare with latest price
        stock_value = StockValue.objects.filter(stock=stock).order_by("-date_added").first()

        if stock_value is not None:
            if stock_value.value != price:
                stock_value = None

        if stock_value is None:
            stock_value = StockValue(stock=stock)
            stock_value.value = price
            stock_value.save()

            total_added = total_added + 1

    return JsonResponse({
        "total": len(stocks),
        "added": total_added
    })
