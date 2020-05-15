@login_required(login_url="/login/")
@admin_only
def objects_dashboard_first_page(request):
    return redirect('/objects/dashboard/1')


@login_required(login_url="/login/")
@admin_only
def objects_dashboard(request, page):
    objects = Model.objects.all() # Replace Model
    amount = len(objects)
    objects = Paginator(objects, 100)
    objects = objects.get_page(page)
    context = {
        "objects": objects,
        "amount": amount,
        "wiki": "link_to_wiki_page",
        "title": "some_title"
    }
    return render(request, 'objects/dashboard.html', context)


@login_required(login_url="/login/")
@admin_only
def objects_delete(request, pk):
    obj = Model.objects.get(pk=pk) # Replace model
    if request.method == "POST":
        obj.delete()
        return redirect('objects_dashboard')
    context = {
        "object": obj,
        "help_text": "Some help text to be displayed."
    }
    return render(request, 'objects/delete.html', {'object': obj})


@login_required(login_url="/login/")
@admin_only
def objects_update(request, pk):
    obj = Model.objects.get(pk=pk) # Replace Model
    if request.method == "POST":
        form = SomeForm(request.POST, instance=obj) # Replace SomeForm
        if form.is_valid():
            form.save()
            return redirect('objects_dashboard')
    form = SomeForm(instance=obj) # Replace SomeForm
    return render(request, 'objects/update.html', {'form': form})

"""
CODE IN URLS

path('objects/create', views.objects_create, name='objects_create'),
path('objects/', views.objects_dashboard_first_page, name='objects_dashboard'),
path('objects/dashboard/', views.objects_dashboard_first_page, name='objects_dashboard'),
path('objects/dashboard/<int:page>', views.objects_dashboard),
path('objects/delete/<int:id>', views.objects_delete, name='objects_delete'),
path('objects/update/<int:id>', views.objects_update, name='objects_update'),
"""