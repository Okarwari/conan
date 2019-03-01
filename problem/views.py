import json
import math
import requests

from django.http import HttpResponseBadRequest, JsonResponse, QueryDict, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from django.views.generic import ListView, DetailView, CreateView


from accounts.models import User
from problem.models import Problem, ProblemComment, CommitRecord
from utils.paginator import ProblemPaginator


class ProblemListView(ListView):
    template_name = 'problem/problems.html'
    context_object_name = 'problems'
    queryset = Problem.objects.all()
    PAGE_LIMITED = 50

    def get_context_data(self, **kwargs):
        content = super(ProblemListView, self).get_context_data(**kwargs)
        try:
            current_page = int(self.request.GET.get('page', 1))
        except:
            current_page = 1
        paginator = ProblemPaginator(object_list=content.get('problem_lst', self.queryset),
                                     per_page=50,
                                     current_page=current_page)
        content['problem_lst'] = paginator.page(paginator.current_page)
        content['paginator'] = paginator
        content['current_page'] = paginator.current_page
        return content


class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    context_object_name = 'problem'
    queryset = Problem.objects.all()
    pk_url_kwarg = 'id'


class AnswerView(View):
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        problem_id = self.request.POST.get('problem_id')
        commit = CommitRecord(code=code,pid=problem_id, uid=request.user.id)
        url = "http://39.96.194.42:5000/python/"
        res = requests.post(url=url, data=json.dumps(commit, default=commit.serializer))
        print(commit.__dict__)
        return JsonResponse(res.content)




class ProblemCommentView(ListView):
    template_name = 'problem/comments.html'
    context_object_name = 'comments'
    queryset = ProblemComment.objects.all()


    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        for obj in self.object_list:
            print(obj.id)
            print(obj.children_comments.all())
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        comment_body = request.POST.get('comment', "")
        if not comment_body:
            return HttpResponseBadRequest('评论不能为空')
        comment = ProblemComment()
        comment.body = comment_body
        comment.problem = Problem(id=self.request.POST.get('problem_id'))
        comment.author = self.request.user
        print(request.POST.get('parent_comment_id'))
        if request.POST.get('parent_comment_id') and request.POST.get('replied_id'):
            reply = User(id=request.POST.get('replied_id'))
            comment.reply = reply
            comment.parent_comment = ProblemComment(id=request.POST.get('parent_comment_id'))
            comment.is_problem_comment = False
        comment.save()
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        template_text = loader.render_to_string(self.template_name, context=context, request=request)
        data = {'code': 0, 'content': template_text}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        # try:
        put_dict= QueryDict(self.request.body)
        comment_id = put_dict.get('id')
        print(type(comment_id), comment_id)
        comment = self.queryset.get(id=comment_id)
        comment.star += 1
        comment.save()
        data = {'code': 0, 'content': comment.star}
        # except Exception as e:
        #     print(e)
        #     data = {'code': -1, 'content': '异常'}
        #     return JsonResponse(data)
        return JsonResponse(data)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.problem_id = self.kwargs.get('id')
        return queryset.filter(problem=self.problem_id, is_problem_comment=True).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data()
        content['problem_id'] = self.problem_id or self.kwargs.get('id')
        return content

