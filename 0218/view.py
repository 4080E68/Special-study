def cpu1(request):
    cpus = cpu.objects.all().order_by('-price')
    aFilter = cpuFilter(queryset=cpus)
    Filter_all = cpuFilter(queryset=cpus)
    if request.method == "POST":
            aFilter = cpuFilter(request.POST, queryset=cpus)
            Filter_all = cpuFilter(request.POST, queryset=cpus)
    context = {
        'aFilter': aFilter,
        'Filter_all': Filter_all
    }
    

    return render(request, 'cpu.html', context)
