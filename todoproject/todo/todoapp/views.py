from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . models import  task
from.forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

# Create your views here.
class tasklistview(ListView):
    model=task
    template_name="home.html"
    context_object_name="task"

class taskdetailview(DetailView):
    model=task
    template_name = "details.html"
    context_object_name = "task1"

class taskupdateview(UpdateView):
    model = task
    template_name="update.html"
    context_object_name = "task1"
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class taskdeleteview(DeleteView):
    model = task
    template_name = "delete.html"
    success_url = reverse_lazy('cbvhome')


def add(request):
    tasks1 = task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date', '')
        tasks=task(name=name,priority=priority,date=date)
        tasks.save()
    return render(request,"home.html",{'task':tasks1})

def delete(request,taskid):

    tasks=task.objects.get(id=taskid)
    if request.method=="POST":
        tasks.delete()
        return redirect("/")
    return render(request,'delete.html')

def update(request,id):
    tasks=task.objects.get(id=id)
    form=TodoForm(request.POST or None,instance=tasks)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'edit.html', {'form': form, 'task':tasks })
