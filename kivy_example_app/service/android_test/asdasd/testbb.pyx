
def android_start_service(j_title, j_description, j_arg):
    print('SUCCESS', j_title, j_description, j_arg)

def start_service(title=None, description=None, arg=None):
    # cdef char *j_title = NULL
    # cdef char *j_description = NULL
    j_title, j_description, j_arg = b'', b'', b''
    if title is not None:
        j_title = <bytes>title
    if description is not None:
        j_description = <bytes>description
    if arg is not None:
        j_arg = <bytes>arg
    android_start_service(j_title, j_description, j_arg)
