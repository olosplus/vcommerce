from django.apps import apps
from django.http import HttpResponse

def get_model_by_string(module, model_name):
    list_module = module.split('.')    

    try:
        model = apps.get_app_config(list_module[len(list_module)-2]).get_model(model_name)
    except LookupError:
        return None
    return model
