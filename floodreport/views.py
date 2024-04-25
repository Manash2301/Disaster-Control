import datetime

from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def index(request):
    return render(request, 'index.html')

def reporting(request):
    error = ""
    if request.method == "POST":
        FullName = request.POST['FullName']
        MobileNumber = request.POST['MobileNumber']
        Location = request.POST['Location']
        Message = request.POST['Message']
        try:
            Floodreport.objects.create(FullName=FullName, MobileNumber=MobileNumber, Location=Location, Message=Message)
            error = "no"
        except:
            error = "yes"
    return render(request, 'reporting.html', locals())

def viewStatus(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            floodreport = Floodreport.objects.filter(Q(FullName__icontains=sd) | Q(MobileNumber=sd) | Q(Location__icontains=sd))
        except:
            floodreport = ""
    return render(request, 'viewStatus.html', locals())

def viewStatusDetails(request,pid):
    floodreport = Floodreport.objects.get(id=pid)
    report1 = Floodtequesthistory.objects.filter(floodreport=floodreport)
    reportcount = Floodtequesthistory.objects.filter(floodreport=floodreport).count()
    return render(request, 'viewStatusDetails.html', locals())

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    totalnewequest = Floodreport.objects.filter(Status__isnull=True).count()
    totalAssign = Floodreport.objects.filter(Status='Assigned').count()
    totalontheway = Floodreport.objects.filter(Status='Team On the Way').count()
    totalworkprocess = Floodreport.objects.filter(Status='Flood Relief Work in Progress').count()
    totalreqcomplete = Floodreport.objects.filter(Status='Request Completed').count()
    totalflood = Floodreport.objects.all().count()
    return render(request, 'admin/dashboard.html', locals())

def addTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']

        try:
            Teams.objects.create(teamName=teamName, teamLeaderName=teamLeaderName, teamLeadMobno=teamLeadMobno, teamMembers=teamMembers)
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/addTeam.html', locals())

def manageTeam(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.all()
    return render(request, 'admin/manageTeam.html', locals())

def editTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.get(id=pid)
    error =""
    if request.method == "POST":
        teamName = request.POST['teamName']
        teamLeaderName = request.POST['teamLeaderName']
        teamLeadMobno = request.POST['teamLeadMobno']
        teamMembers = request.POST['teamMembers']

        teams.teamName = teamName
        teams.teamLeaderName = teamLeaderName
        teams.teamLeadMobno = teamLeadMobno
        teams.teamMembers = teamMembers

        try:
            teams.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editTeam.html', locals())

def deleteTeam(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    teams = Teams.objects.get(id=pid)
    teams.delete()
    return redirect('manageTeam')

def newRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.filter(Status__isnull=True)
    return render(request, 'admin/newRequest.html', locals())

def assignRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.filter(Status='Assigned')
    return render(request, 'admin/assignRequest.html', locals())

def teamontheway(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.filter(Status='Team On the Way')
    return render(request, 'admin/teamontheway.html', locals())

def workinprogress(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.filter(Status='Flood Relief Work in Progress')
    return render(request, 'admin/workinprogress.html', locals())

def completeRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.filter(Status='Request Completed')
    return render(request, 'admin/completeRequest.html', locals())

def allRequest(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.all()
    return render(request, 'admin/allRequest.html', locals())

def deleteRequest(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.get(id=pid)
    floodreport.delete()
    return redirect('allRequest')

def viewRequestDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    floodreport = Floodreport.objects.get(id=pid)
    report1 = Floodtequesthistory.objects.filter(floodreport=floodreport)
    floodreportid = floodreport.id
    team = Teams.objects.all()
    reportcount = Floodtequesthistory.objects.filter(floodreport=floodreport).count()
    try:
        if request.method == "POST":
            teamid = request.POST['AssignTo']
            Status="Assigned"
            team1 = Teams.objects.get(id=teamid)
            try:
                floodreport.AssignTo = team1
                floodreport.Status = Status
                now = datetime.now()
                floodreport.AssignedTime = now.strftime("%m/%d/%Y %H:%M:%S")
                floodreport.save()
                error = "no"
            except:
                error = "yes"
    except:
        if request.method == "POST":
            status = request.POST['status']
            remark = request.POST['remark']

            try:
                requesttracking = Floodtequesthistory.objects.create(floodreport=floodreport,status=status, remark=remark)
                floodreport.Status = status
                floodreport.save()
                floodreport.UpdationDate = date.today()
                error1 = "no"
            except:
                error1 = "yes"
    return render(request, 'admin/viewRequestDetails.html', locals())

def dateReport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == 'POST':
        fd = request.POST['fromDate']
        td = request.POST['toDate']
        floodreport = Floodreport.objects.filter(Q(Postingdate__gte=fd) & Q(Postingdate__lte=td))
        return render(request, 'admin/betweendateReportDtls.html', locals())
    return render(request, 'admin/dateReport.html', locals())

def search(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            floodreport = Floodreport.objects.filter(Q(FullName__icontains=sd) | Q(MobileNumber=sd) | Q(Location__icontains=sd))
        except:
            floodreport = ""
    return render(request, 'admin/search.html', locals())

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/changePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')
