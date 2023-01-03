def simple_middleware(get_response):
    def middleware(request):
        print("before request------11111-----")
        response = get_response(request)
        print('after request/response------11111-----')
        return response

    return middleware

def simple_middleware2(get_response):
    def middleware(request):
        print("before request ----22222----")
        response = get_response(request)
        print('after request/response-----2222----')
        return response

    return middleware
