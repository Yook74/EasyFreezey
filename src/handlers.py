from flask import Response, Blueprint


def handle_integrity_error(exception):
    return Response(exception.args[0], status=400)


def handle_key_error(exception):
    return Response(f'JSON was missing key "{exception.args[0]}"', status=400)
