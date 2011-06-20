from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Import the Django helpers
import facebook.djangofb as facebook

from models import User
from models import Business
from models import Event

# Helper funcs

# API funcs

@facebook.require_login()
def canvas(request):
    return direct_to_template(request, 'canvas.fbml')

@facebook.require_login()
def create(request):
    if 'bname' in request.POST:
        buis_list = Business.objects.filter(name=request.POST['bname'][:28])
        if len(buis_list) > 0:
            return direct_to_template(request, 'create.fbml', extra_context={'iserror': 1})
        else:
            buis = Business.objects.get_bid(request.POST['bname'][:28], int(request.POST['badmodel']))
            buis.purpose = request.POST['bpurpose'][:300]
            buis.chair = request.facebook.uid
            buis.board = request.facebook.uid
            buis.members = request.facebook.uid
            buis.save()
            user = User.objects.get_current()
            if user.rep is None:
                user.rep = str(buis.id) + ':100'
            else:
                user.rep += ',' + str(buis.id) + ':100'
            user.save()

        e = Event(name='New Business', uid=request.facebook.uid, suid=request.facebook.uid, bid=buis, status=0, hide=0, type='bus_create', desc='You successfully created a new business: %s' % buis.name)
        e.save()

        return render_to_response('create_resp.fbml', {'bname': buis.name, 'bpurpose': buis.purpose, 'bdate': buis.creat_date, 'badmodel': buis.admodel})

    return direct_to_template(request, 'create.fbml')

@facebook.require_login()
def manage(request):
    if 'bselect' in request.POST:
        buis = Business.objects.get(id=request.POST['bselect'])
        if buis.members is not None:
            members_list = buis.members.split(',')
        else:
            members_list=[]
        if request.facebook.uid in members_list:
            return render_to_response('manage_detail.fbml', {'bid': buis.id, 'bname': buis.name, 'bpurpose': buis.purpose, 'bdate': buis.creat_date, 'badmodel': buis.admodel})

    buis_by_uid = Business.objects.filter(members__icontains=request.facebook.uid)
    if (len(buis_by_uid) > 0):
        return render_to_response('manage.fbml', {'bids': buis_by_uid})
    else:
        return render_to_response('manage.fbml', {})

@facebook.require_login()
def events(request):
    event_list = Event.objects.filter(uid=request.facebook.uid).exclude(hide=1)
    if (len(event_list) > 0):
        return render_to_response('events.fbml', {'events': event_list, 'events_count': len(event_list)})
    else:
        return render_to_response('events.fbml', {})
    
@facebook.require_login()
def eventbynum(request, event_id):
    e = Event.objects.get(id=event_id)
    return render_to_response('event_detail.fbml', {'event': e})

@facebook.require_login()
def eventhide(request, event_id):
    e = Event.objects.get(id=event_id)
    e.hide = 1
    e.save()
    event_list = Event.objects.filter(uid=request.facebook.uid).exclude(hide=1)
    if (len(event_list) > 0):
        return render_to_response('events.fbml', {'events': event_list})
    else:
        return render_to_response('events.fbml', {})

@facebook.require_login()
def manageinvite(request, bid):
    buis = Business.objects.get(id=bid)
    for i in request.POST.getlist('ids[]'):
        uname = request.facebook.users.getInfo([request.facebook.uid], ['name'])[0]['name']
        e = Event(name='Business Invitation', uid=i, suid=request.facebook.uid, bid=buis, status=0, hide=0, type='bus_invite', desc='You have been invited to join the %s business by %s' % (buis.name, uname))
        e.save()
    return manage(request)

@facebook.require_login()
def closeevent(request, event_id):
    if 'forward' in request.POST:
        e = Event.objects.get(id=event_id)
        for i in request.POST.getlist('ids[]'):
            uname = request.facebook.users.getInfo([request.facebook.uid], ['name'])[0]['name']
            e = Event(name='Business Invitation', uid=i, suid=request.facebook.uid, bid=e.bid, status=0, hide=0, type='bus_invite', desc='You have been invited to join the %s business by %s' % (e.bid.name, uname))
            e.save()

    if 'accept' in request.POST:
        e = Event.objects.get(id=event_id)
        buis = e.bid
        if buis.members is not None:
            members_list = buis.members.split(',')
        else:
            members_list=[]

        if request.facebook.uid not in members_list:
            members_list += [request.facebook.uid]
            buis.members = ','.join(members_list)
            user = User.objects.get_current()
            if user.rep is None:
                user.rep = str(buis.id) + ':0'
                user.save()
            else:
                rep_list = user.rep.split(',')
                rep_map = {}
                for r in rep_list:
                    ub,ur = r.split(':')
                    rep_map[ub] = ur
                if buis not in rep_map:
                    user.rep += ',' + str(buis.id) + ':0'
                    user.save()
        buis.save()

        uname = request.facebook.users.getInfo([request.facebook.uid], ['name'])[0]['name']
        e = Event(name='Business Invitation Accepted', uid=e.suid, suid=request.facebook.uid, bid=buis, status=0, hide=0, type='bus_invite_acc', desc='%s has accepted your invitation to join the %s business' % (uname, buis.name))
        e.save()

    return HttpResponseRedirect(reverse('socialfarm.sfmanage.views.events'))

@facebook.require_login()
def managemembers(request, bid):
    buis = Business.objects.get(id=bid)
    if buis.members is not None:
        buid_list = buis.members.split(',')
        buid_list.sort()
        members_list = []
        for uid in buid_list:
            uname = request.facebook.users.getInfo([uid], ['name'])[0]['name']
            members_list += [(uid, uname)]
        return render_to_response('manage_members.fbml', {'bid': bid, 'bname': buis.name, 'members_list': members_list, 'members_count': len(members_list)})
    else:
        return HttpResponseRedirect(reverse('socialfarm.sfmanage.views.manage'))

@facebook.require_login()
def managemember(request, bid, uid):
    buis = Business.objects.get(id=bid)
    if 'remove' in request.POST:
        if buis.members is not None:
            event_list = Event.objects.filter(uid=uid, bid=bid, type='bus_invite')
            for e in event_list:
                e.hide = 1
                e.save()
            buid_list = buis.members.split(',')
            buid_list.sort()
            buid_list.remove(uid)
            buis.members = ','.join(buid_list)
            buis.save()
            members_list = []
            for uid in buid_list:
                uname = request.facebook.users.getInfo([uid], ['name'])[0]['name']
                members_list += [(uid, uname)]
            return render_to_response('manage_members.fbml', {'bname': buis.name, 'members_list': members_list, 'members_count': len(members_list)})
        else:
            return HttpResponseRedirect(reverse('socialfarm.sfmanage.views.manage'))

    uname = request.facebook.users.getInfo([uid], ['name'])[0]['name']
    return render_to_response('manage_member.fbml', {'bname': buis.name, 'bid': bid, 'uid': uid, 'uname': uname})

@facebook.require_login()
def managegroups(request, bid):
    buis = Business.objects.get(id=bid)
    if buis.members is not None:
        buid_list = buis.members.split(',')
        buid_list.sort()
        members_list = []
        for uid in buid_list:
            uname = request.facebook.users.getInfo([uid], ['name'])[0]['name']
            members_list += [(uid, uname)]
        return render_to_response('manage_members.fbml', {'bid': bid, 'bname': buis.name, 'members_list': members_list, 'members_count': len(members_list)})
    else:
        return HttpResponseRedirect(reverse('socialfarm.sfmanage.views.manage'))

@facebook.require_login()
def managerep(request, bid):
    #Get ref to Business object
    buis = Business.objects.get(id=bid)

    # User submit an update
    if 'submit' in request.POST:
        group_list  = [(0, 'Key Contributor', request.POST['0'])]
        group_list += [(1, 'Board Members', request.POST['1'])]
        group_list += [(2, 'Other Members', request.POST['2'])]
        rep_tot = int(request.POST['0']) + int(request.POST['1']) + int(request.POST['2'])
        # User submitted an invalid distribution
        if rep_tot != 100:
            return render_to_response('manage_rep.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'rep_tot': rep_tot, 'res_code': 'BAD_DIST'})
        # Distribution good now save it
        buis.cont_rep  = request.POST['0']
        buis.board_rep = request.POST['1']
        buis.other_rep = request.POST['2']
        buis.save()
        return render_to_response('manage_rep.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'rep_tot': rep_tot, 'res_code': 'SUCC'})

    # Default case
    group_list  = [(0, 'Key Contributor', buis.cont_rep)]
    group_list += [(1, 'Board Members', buis.board_rep)]
    group_list += [(2, 'Other Members', buis.other_rep)]
    rep_tot = buis.cont_rep + buis.board_rep + buis.other_rep
    return render_to_response('manage_rep.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'rep_tot': rep_tot, 'res_code': 'QUERY'})

@facebook.require_login()
def managepay(request, bid):
    #Get ref to Business object
    buis = Business.objects.get(id=bid)

    # User submit an update
    if 'submit' in request.POST:
        group_list  = [(0, 'Key Contributor', request.POST['0'])]
        group_list += [(1, 'Board Members', request.POST['1'])]
        group_list += [(2, 'Other Members', request.POST['2'])]
        rep_tot = int(request.POST['0']) + int(request.POST['1']) + int(request.POST['2'])
        # User submitted an invalid distribution
        if pay_tot != 100:
            return render_to_response('manage_pay.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'pay_tot': pay_tot, 'res_code': 'BAD_DIST'})
        # Distribution good now save it
        buis.cont_pay  = request.POST['0']
        buis.board_pay = request.POST['1']
        buis.other_pay = request.POST['2']
        buis.save()
        return render_to_response('manage_pay.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'pay_tot': pay_tot, 'res_code': 'SUCC'})

    # Default case
    group_list  = [(0, 'Key Contributor', buis.cont_pay)]
    group_list += [(1, 'Board Members', buis.board_pay)]
    group_list += [(2, 'Other Members', buis.other_pay)]
    pay_tot = buis.cont_pay + buis.board_pay + buis.other_pay
    return render_to_response('manage_pay.fbml', {'bid': bid, 'bname': buis.name, 'group_list': group_list, 'pay_tot': pay_tot, 'res_code': 'QUERY'})
