# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, YearArchiveView
from clubManagement.models import Attendance
from registration.models import UserInfo


class AttendanceAddView(View):
    template_name = 'clubManagement/attendance_add.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *args, **kwargs):
        year = int(kwargs.get('batch', None))
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        user_info_list = UserInfo.objects.filter(year=year)
        attendance_list = []
        for user_info in user_info_list:
            try:
                attendance = Attendance.objects.get(user=user_info.user, date=d)
            except Attendance.DoesNotExist:
                attendance = Attendance(user=user_info.user,
                                        added_by=User.objects.get(username=self.request.user.username), date=d)
                attendance.save()
            attendance_list.append(attendance)
        return {'attendance_list': attendance_list}

    def post(self, request, *args, **kwargs):
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        attendance_list = Attendance.objects.filter(date=d)
        for i in attendance_list:
            i.attendance = False
            i.save()
        for key in request.POST:
            try:
                user = User.objects.get(username=key)
            except User.DoesNotExist:
                user = None
            if user:
                att = Attendance.objects.get(user=user, date=d)
                att.attendance = True
                att.save()
        return redirect('add_attendance', **kwargs)


class YearAttendanceReportView(View):
    template_name = 'clubManagement/attendance_yearly.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if 'user_id' in kwargs:
            user = User.objects.get(id=int(kwargs.get('user_id')))
            att = user.attendance_set.filter(date__year=int(kwargs.get('year')))
            month_att = []
            month = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                     "October", "November", "December"]
            month_num = range(12)
            for i in month_num:
                month_att.append(len(att.filter(date__month=(i + 1))))
            context = {'user': user, 'month_att': month_att, 'month': month, 'month_num': month_num, 'year': kwargs.get('year')}
        return render(request, self.template_name, context)