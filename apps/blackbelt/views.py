from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages

# Create your views here.
# Renders Log in page
def index(request):
	return render(request, "blackbelt/index.html")

# process log in and regstration
def process_logreg(request):
	if request.POST['action'] == 'register':
		postData = {
			'name': request.POST['name'],
			'username': request.POST['username'],
			'password': request.POST['password'],
			'confirmpw': request.POST['confirmpw'],
		}
		user = User.objects.register(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			messages.success(request, 'Successfully registered, you may now log in.')
			return redirect('/')
	elif request.POST['action'] == 'login':
		postData = {
			'username': request.POST['username'],
			'password': request.POST['password']
		}
		user = User.objects.login(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			return redirect('/travels')

# logout
def logout(request):
	request.session.clear()
	return redirect('/')

# Renders Dashboard
def dashboard(request):
	trips = Trip.objects.all()
	context = {
		'user': User.objects.get(id=request.session['user']),
		'trips': trips
	}
	return render(request, "blackbelt/dashboard.html", context)

def addpage(request):
    return render(request, "blackbelt/addtrip.html")

def addtrip(request):
    postData = {
        'destination': request.POST['destination'],
        'description': request.POST['description'],
        'startdate': request.POST['startdate'],
        'enddate': request.POST['enddate'],
        'user_id': request.session['user']
    }
    trip = Trip.objects.add(postData)
    if 'error' in trip:
        for message in trip['error']:
            messages.error(request, message)
        return redirect('/travels/add')
    if 'trip' in trip:
        pass
    return redirect('/travels')

def destination(request, id):
    trip = Trip.objects.get(id=id)
    context = {
        'trip': trip
    }
    return render(request, "blackbelt/destination.html", context)

def join(request, id):
    user = User.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    trip.attendees.add(user)
    return redirect('/travels')
