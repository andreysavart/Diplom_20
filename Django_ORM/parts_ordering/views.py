from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
)

from .models import (
    Bolt,
    BoltJoint,
    Nut,
    Order,
    Washer,
)


def index(request):
    orders = Order.objects.all()
    return render(request, 'index.html', context={'orders': orders})


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    fields = ['customer', 'order_items']
    
    def get_success_url(self):
        return '/orders'
    

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    fields = ['customer', 'order_items']

    def get_success_url(self):
        order = self.get_object()
        return f'/order/{order.id}'


def get_bolt_joints(request):
    bolt_joints = BoltJoint.objects.all()
    return render(request, 'bolt_joints.html', context={'bolt_joints': bolt_joints})


class BoltJointCreateView(CreateView):
    model = BoltJoint
    template_name = 'bolt_joint_create.html'
    fields = ['bolt', 'bolt_washer', 'material', 'nut_washer', 'nut', 'locknut']
    
    def get_success_url(self):
        return '/bolt_joints'
    

class BoltJointDetailView(DetailView):
    model = BoltJoint
    template_name = 'bolt_joint_detail.html'


class BoltJointUpdateView(UpdateView):
    model = BoltJoint
    template_name = 'bolt_joint_update.html'
    fields = ['bolt', 'bolt_washer', 'material', 'nut_washer', 'nut', 'locknut']

    def get_success_url(self):
        bolt_joint = self.get_object()
        return f'/bolt_joint/{bolt_joint.id}'


def get_bolts(request):
    bolts = Bolt.objects.all()
    return render(request, 'bolts.html', context={'bolts': bolts})


class BoltCreateView(CreateView):
    model = Bolt
    template_name = 'bolt_create.html'
    fields = ['name', 'diameter', 'weight', 'accuracy_class', 'cost', 'strength_class', 'length', 'size']
    
    def get_success_url(self):
        return '/bolts'


class BoltDetailView(DetailView):
    model = Bolt
    template_name = 'bolt_detail.html'


class BoltUpdateView(UpdateView):
    model = Bolt
    template_name = 'bolt_update.html'
    fields = ['name', 'diameter', 'length', 'weight', 'accuracy_class', 'cost', 'strength_class', 'size']

    def get_success_url(self):
        bolt = self.get_object()
        return f'/bolt/{bolt.id}'


def get_nuts(request):
    nuts = Nut.objects.all()
    return render(request, 'nuts.html', context={'nuts': nuts})


class NutCreateView(CreateView):
    model = Nut
    template_name = 'nut_create.html'
    fields = ['name', 'diameter', 'weight', 'accuracy_class', 'cost', 'strength_class', 'size']
    
    def get_success_url(self):
        return '/nuts'


class NutDetailView(DetailView):
    model = Nut
    template_name = 'nut_detail.html'


class NutUpdateView(UpdateView):
    model = Nut
    template_name = 'nut_update.html'
    fields = ['name', 'diameter', 'weight', 'accuracy_class', 'cost', 'strength_class', 'size']

    def get_success_url(self):
        nut = self.get_object()
        return f'/nut/{nut.id}'


def get_washers(request):
    washers = Washer.objects.all()
    return render(request, 'washers.html', context={'washers': washers})


class WasherCreateView(CreateView):
    model = Washer
    template_name = 'washer_create.html'
    fields = ['name', 'diameter', 'weight', 'accuracy_class', 'cost', 'strength_class']
    
    def get_success_url(self):
        return '/washers'


class WasherDetailView(DetailView):
    model = Washer
    template_name = 'washer_detail.html'


class WasherUpdateView(UpdateView):
    model = Washer
    template_name = 'washer_update.html'
    fields = ['name', 'diameter', 'weight', 'accuracy_class', 'cost', 'strength_class']

    def get_success_url(self):
        washer = self.get_object()
        return f'/washer/{washer.id}'
