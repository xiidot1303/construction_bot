def all_libraries():
    from django.shortcuts import render, redirect
    from django.views.generic.edit import CreateView, UpdateView, DeleteView
    from django.contrib.auth.mixins import LoginRequiredMixin