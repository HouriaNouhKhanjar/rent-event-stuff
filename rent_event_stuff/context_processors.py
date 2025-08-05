def canonical_url(request):
    uri = request.build_absolute_uri()
    clean_uri = uri.split('?')[0]
    return {'canonical_url': clean_uri}
