from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views import View
from .models import FruitsModel, CommentsModel
from .forms import FruitsForm, FruitUpdateForm, CommentForm, CommentUpdateForm

# Create your views here.


@login_required
def homepage_view(request):
    return render(request, "home.html")

class FruitsView(View):
    def get(self, request):
        query = request.GET.get("q")
        if query:
            fruits_list = FruitsModel.objects.filter(
                Q(name__icontains=query) | Q(price__icontains=query)
            ).order_by("-id")
        else:
            fruits_list = FruitsModel.objects.all().order_by("-id")
        page = request.GET.get("page", 1)
        paginator = Paginator(fruits_list, 2)

        try:
            fruits = paginator.page(page)
        except PageNotAnInteger:
            fruits = paginator.page(1)
        except EmptyPage:
            fruits = paginator.page(paginator.num_pages)

        return render(request, "fruits/fruits.html", {"fruits": fruits})


class AddFruitView(View):
    def post(self, request):
        form = FruitsForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            form.save()
            return redirect("fruits")
        else:
            return render(request, "fruits/add_fruit.html", {"form": form})

    def get(self, request):
        form = FruitsForm()
        return render(request, "fruits/add_fruit.html", {"form": form})


class FruitView(View):
    def get(self, request, pk):
        fruit = FruitsModel.objects.get(id=pk)
        comments = CommentsModel.objects.filter(fruit=pk).order_by("-id")
        total_star = 0
        count = 1
        for star in comments:
            total_star += star.star_given
            count += 1
        if count > 1:
            count -= 1
        
        context = {
            "fruit": fruit,
            "comments": comments,
            "total_star": total_star / count,
        }
        return render(request, "fruits/fruit.html", context=context)


class UpdateFruitView(View):
    def get(self, request, pk):
        fruit = get_object_or_404(FruitsModel, id=pk)
        form = FruitUpdateForm(instance=fruit)
        context = {"form": form, "fruit": fruit}
        return render(request, "fruits/update_fruit.html", context=context)

    def post(self, request, pk):
        fruit = get_object_or_404(FruitsModel, id=pk)
        form = FruitUpdateForm(request.POST, request.FILES, instance=fruit)
        if form.is_valid():
            form.save()
            return redirect("fruits")
        context = {"form": form, "fruit": fruit}
        return render(request, "fruits/update_fruit.html", context=context)


class DeleteFruitView(View):
    def get(self, request, pk):
        fruit = get_object_or_404(FruitsModel, id=pk)
        return render(request, "fruits/delete_fruit.html", {"fruit": fruit})

    def post(self, request, pk):
        fruit = get_object_or_404(FruitsModel, id=pk)
        fruit.delete()
        return redirect("fruits")


class AddCommentView(View):
    def get(self, request, pk):
        form = CommentForm()
        return render(
            request, "fruits/add_comment.html", {"form": form, "fruit_id": pk}
        )

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.fruit_id = pk
            comment.user = request.user
            comment.save()
            return redirect("fruit", pk=pk)
        return render(
            request, "fruits/add_comment.html", {"form": form, "fruit_id": pk}
        )


class DeleteCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(CommentsModel, id=pk)
        return render(request, "fruits/delete_comment.html", {"comment": comment})

    def post(self, request, pk):
        comment = get_object_or_404(CommentsModel, id=pk)
        pk = comment.fruit.pk
        comment.delete()
        return redirect("fruit", pk=pk)


class UpdateCommentView(View):
    def get(self, request, pk):
        comment = get_object_or_404(CommentsModel, id=pk)
        form = CommentUpdateForm(instance=comment)
        context = {"form": form, "comment": comment}
        return render(request, "fruits/update_comment.html", context=context)

    def post(self, request, pk):
        comment = get_object_or_404(CommentsModel, id=pk)
        form = CommentUpdateForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            pk = comment.fruit.pk
            form.save()
            return redirect("fruit", pk=pk)
        context = {"form": form, "comment": comment}
        return render(request, "fruits/update_comment.html", context=context)
