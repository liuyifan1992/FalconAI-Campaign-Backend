from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Welcome to the email generator!")

@csrf_exempt
def sendEmail(request):
    if request.method == "POST" and 'email_content' in request.POST:
        # Process other email data here
        email_content = request.POST['email_content']
        return JsonResponse({'email_content': email_content}, status=200)
    else:
        raise HttpResponseBadRequest
