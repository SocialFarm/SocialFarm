from django.http import HttpResponse

def test(request):
    return HttpResponse("this is a test")    

def facebook(request, uid):
    return HttpResponse("this is a test, uid = %s" % uid)
