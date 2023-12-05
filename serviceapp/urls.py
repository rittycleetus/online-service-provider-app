from django.urls import path
from .import views

urlpatterns = [
      path('',views.home,name='home'),
      path('usersignup',views.usersignup,name='usersignup'),
      path('workersignup',views.workersignup,name='workersignup'),
      path('useraction',views.useraction,name='useraction'),
      path('workeraction',views.workeraction,name='workeraction'),
      path('login1',views.login1,name='login1'),
      path('loginact',views.loginact,name='loginact'),
      path('useraction1',views.useraction1,name='useraction1'),
      path('workeraction1',views.workeraction1,name='workeraction1'),
      path('dash',views.dash,name='dash'),
      path('addcategory',views.addcategory,name='addcategory'),
      path('addcat',views.addcat,name='addcat'),
      path('showuser',views.showuser,name='showuser'),
      path('useredit/<int:pk>',views.useredit,name='useredit'),
      path('useredit1/<int:pk>',views.useredit1,name='useredit1'),
      path('workercard/<int:pk>',views.workercard,name='workercard'),
      path('workeredit/<int:pk>',views.workeredit,name='workeredit'),
      path('workeredit1/<int:pk>',views.workeredit1,name='workeredit1'),
      path('showusers',views.showusers,name='showusers'),
      path('addservice',views.addservice,name='addservice'),
      path('addservice1',views.addservice1,name='addservice1'),
      path('nofitr',views.nofitr,name='nofitr'),
      path('fitr/<int:pk>',views.fitr,name='fitr'),
      path('bookit/<int:pk>',views.bookit,name='bookit'),
      path('bookit1/<int:pk>',views.bookit1,name='bookit1'),
      
      path('showworkers',views.showworkers,name='showworkers'),
      path('workercard1/<int:pk>',views.workercard1,name='workercard1'),
      path('deleteworker/<int:pk>',views.deleteworker,name='deleteworker'),
      path('deleteuser/<int:pk>',views.deleteuser,name='deleteuser'),
      path('logoutt',views.logoutt,name='logoutt'),
      path('viewservices',views.viewservices,name='viewservices'),
      path('viewworkercards',views.viewworkercards,name='viewworkercards'),
      path('deleteorder',views.deleteorder,name='deleteorder'),
      path('myorderview',views.myorderview,name='myorderview'),
 
      path('approve/<int:pk>',views.approve,name='approve'),
      path('disapproval/<int:pk>',views.disapproval,name='disapproval'),
      path('approdetails',views.approdetails,name='approdetails'),
      path('workeractionfake',views.workeractionfake,name='workeractionfake'),
      path('show_notification',views.show_notification,name='show_notification'),
      path('logoutt',views.logoutt,name='logoutt'),
      path('servicebooking',views.servicebooking,name='servicebooking'),
      path('disapprovalorder/<int:pk>',views.disapprovalorder,name='disapprovalorder'),
      path('appovalorder/<int:pk>',views.approvalorder,name='approvalorder'),
      path('update_password',views.update_password,name='update_password'),
      path('usercard/<int:pk>',views.usercard,name='usercard'),
      path('viewallbookings',views.viewallbookings,name='viewallbookings'),
     
     
      path('viewprodadminandworker',views.viewprodadminandworker,name='viewprodadminandworker'),
      path('showworkersforuser',views.showworkersforuser,name='showworkersforuser'),
     
      path('rating',views.rating,name='rating'),

       path('addcategoryworker',views.addcategoryworker,name='addcategoryworker'),

      path('addcatworker',views.addcatworker,name='addcatworker'),

      path('addserviceworker',views.addserviceworker,name='addserviceworker'),
      path('addservice2',views.addservice2,name='addservice2'),

]