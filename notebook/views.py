from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from .forms import AnalystForm, TaskForm
from .models import LABORATORIES, Supervisor, Analyst, Task


class LaboratoryView(View):
    """Class inheriting from built-in class-based base View from Django."""

    def get(self, request):
        """It builds a HomePage of LaboratoryNotebook website.

        LABORATORIES: a global pre-defined variable with a list of available laboratory departments
        """

        return render(request, 'notebook/laboratory.html', {'laboratories': LABORATORIES})


class LaboratoryDepartmentView(View):
    """Class inheriting from built-in class-based base View from Django."""

    def get(self, request, laboratory):
        """It builds a HomePage of each lab department.

        Data model references are used here for Supervisor & Analyst models to make DB queries
        and retrieve specific pieces of information.

        is_supervisor: a flag used to build different Views for Supervisors and other lab members
        LABORATORIES: a global pre-defined variable with a list of available laboratory departments
        """

        supervisor = Supervisor.objects.filter(laboratory__contains=[laboratory])
        analysts = Analyst.objects.filter(laboratory__contains=[laboratory])

        is_supervisor = False
        if supervisor:
            if request.user == supervisor[0].user:
                is_supervisor = True

        return render(request, "notebook/lab_department.html", {
            "supervisor": supervisor,
            "analysts": analysts,
            "laboratory_name": LABORATORIES[int(laboratory) - 1][1],
            "is_supervisor": is_supervisor,
        })


@login_required
def get_analyst_form(request):
    """Function allows to get the additional Analyst information from a new User.

    Initially, each new User does not have his own account in Analyst model created.
    The function allows to check whether such record already exists and asks for an Input from the current User.
    New record in Analyst table is added and finally a User is redirected to the page with his Current Tasks.
    """

    analyst = Analyst.objects.filter(user=request.user)
    if analyst:
        return redirect('view_current_tasks')

    if request.method == 'GET':
        return render(request, 'notebook/add_form_user.html', {
            'form': AnalystForm(),
            'laboratories': LABORATORIES,
        })
    else:
        try:
            form = AnalystForm(request.POST)
            new_analyst = form.save(commit=False)
            new_analyst.user = request.user
            new_analyst.save()
            return redirect('view_current_tasks')
        except ValueError as VE:
            return render(request, 'notebook/add_form_user.html', {
                'form': AnalystForm(),
                'laboratories': LABORATORIES,
                'error': VE
            })


@login_required
def superior_overview(request, analyst_pk):
    """This function retruns a Supervisior View on Task progression of each Analyst."""

    analyst = Analyst.objects.filter(user=analyst_pk)[0]
    current_tasks = Task.objects.filter(analyst_id=analyst, date_completed__isnull=True)
    completed_tasks = Task.objects.filter(analyst_id=analyst, date_completed__isnull=False)

    return render(request, 'notebook/analyst.html', {
        'analyst': analyst,
        'current_tasks': current_tasks,
        'completed_tasks': completed_tasks,
    })


@login_required
def create_task(request):
    """Function allows to Create a new Task"""

    if request.method == 'GET':
        return render(request, 'notebook/create_task.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)

            analyst = Analyst.objects.filter(user=request.user)
            new_task.analyst_id = analyst[0]

            new_task.date_sent = timezone.now()

            new_task.save()
            return redirect('view_current_tasks')
        except ValueError as VE:
            return render(request, 'notebook/create_task.html', {
                'form': TaskForm(),
                'error': VE
            })


@login_required
def view_current_tasks(request):
    """Function with the View on the list of Current Tasks"""

    analyst = Analyst.objects.filter(user=request.user)
    tasks = Task.objects.filter(analyst_id=analyst[0], date_completed__isnull=True)

    return render(request, 'notebook/current_tasks.html', {'tasks': tasks})


@login_required
def view_completed_tasks(request):
    """Function with the View on the list of Completed Tasks"""

    analyst = Analyst.objects.filter(user=request.user)
    tasks = Task.objects.filter(analyst_id=analyst[0], date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'notebook/completed_tasks.html', {'tasks': tasks})


@login_required
def view_task(request, task_pk):
    """Function with the View on the chosen Task.

    It allows to change the previously given Input and Save changes.
    """

    analyst = Analyst.objects.filter(user=request.user)
    task = get_object_or_404(Task, pk=task_pk, analyst_id=analyst[0])

    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'notebook/view_task.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('view_current_tasks')
        except ValueError as VE:
            return render(request, 'notebook/view_task.html', {
                'task': task,
                'form': form,
                'error': VE
            })


@login_required
def complete_task(request, task_pk):
    """Function allows to mark the Task as Completed."""

    analyst = Analyst.objects.filter(user=request.user)
    task = get_object_or_404(Task, pk=task_pk, analyst_id=analyst[0])

    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('view_current_tasks')


@login_required
def delete_task(request, task_pk):
    """Function allows to delete the Task."""

    analyst = Analyst.objects.filter(user=request.user)
    task = get_object_or_404(Task, pk=task_pk, analyst_id=analyst[0])
    if request.method == 'POST':
        task.delete()
        return redirect('view_current_tasks')
