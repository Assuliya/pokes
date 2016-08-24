from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from models import User, Poke
import bcrypt

def index(request):
    return render(request, 'user_poke/index.html')

def user_page(request, user_id):
    user = User.objects.get(id = user_id)
    pokes = Poke.objects.filter(user_id_to = user_id).values('user_id').annotate(count=Count('user_id')).order_by('-count')
    total = 0
    for x in pokes:
        total += 1
    other = User.objects.all()

    # other_count = []
    # for x in other:
    #     z = Poke.objects.filter(user_id_to = x.id).values('user_id').annotate(count=Count('user_id')).order_by('-count')
    #     other_total = 0
    #     for y in z:
    #         other_total += 1
    #     pack = {}
    #     pack.update({'id':x.id})
    #     pack.update({'count':other_total})
    #     other_count.append(pack)
    # print other_count

    other_count = Poke.objects.raw('SELECT "user_poke_poke"."id","user_poke_poke"."user_id_to_id","user_poke_poke"."user_id_id", COUNT("user_poke_poke"."user_id_id") AS "count" FROM "user_poke_poke" GROUP BY "user_poke_poke"."user_id_id" ORDER BY "count" DESC')


    context = {'user':user, 'total': total, 'pokes': pokes, 'other': other, 'other_count': other_count}
    return render(request, 'user_poke/user.html', context)

def register_process(request):
    result = User.manager.validateReg(request)
    resultPass = User.manager.validateRegPass(request)
    print result
    print resultPass
    if result[0] == False or resultPass[0] == False:
        errors = result[1]+resultPass[1]
        print errors
        print_messages(request, errors)
        return redirect(reverse('index'))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.manager.create(name=request.POST['name'], alias=request.POST['alias'], birth=request.POST['birth'], email=request.POST['email'], pw_hash=pw_hash)
    return log_user_in(request, user)

def login_process(request):
    result = User.manager.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('user_page', kwargs={'user_id':request.session['user']}))

def logout(request):
    user = User.manager.get(id=request.session['user'])
    request.session.pop('user')
    return redirect(reverse('index'))

def poke(request, user_id):
    poked = User.objects.get(id = user_id)
    poker = User.objects.get(id = request.session['user'])
    poke = Poke.objects.create(user_id_to = poked, user_id = poker)
    return redirect(reverse('user_page', kwargs={'user_id':request.session['user']}))
