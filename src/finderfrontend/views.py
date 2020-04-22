from django.shortcuts import render

# Create your views here.
def frontindex(request):
  return render(request, 'index.html')