from django_jinja import library
lib = library.Library()


@lib.global_function
def custom_upper(name):
    return name.upper()
