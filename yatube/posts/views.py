from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post



def index(request):
    # одна строка вместо тысячи слов на SQL, берем первые 10 строк взятые отсорченые по дате с конца
    latest = Post.objects.order_by('-pub_date')[:10]
    # # собираем тексты постов в один, разделяя новой строкой
    # output = []
    # for item in latest:
    #     output.append(item.text)
    # return HttpResponse('\n'.join(output))
    return render(request, "index.html", {"posts": latest})


