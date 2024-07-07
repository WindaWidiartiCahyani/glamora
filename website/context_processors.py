from .models import Kategori

def kategori_context_processor(request):
    return {
        'kategori': Kategori.objects.all()
    }