from flask import send_file, request, jsonify
from state import State, FetchTimeoutError, NotAtHeadVersionError, InvalidNamespaceError


def register_routes(app):
    @app.route("/")
    def main():
        return send_file("build/index.html")

    @app.route("/api/create_namespace", methods=["POST"])
    def handle_create_ns():
        state = State.get_instance()
        ns = request.json["namespace"]
        success = state.create_namespace(ns)
        if not success:
            resp = jsonify({
                "error": "namespace_conflict",
            })
            resp.status_code = 400
            return resp
        return jsonify({})

    @app.route("/api/list_namespaces", methods=["POST"])
    def handle_list_nss():
        state = State.get_instance()
        nss = state.list_namespaces()
        return jsonify({
            "namespaces": nss
        })

    @app.route("/api/commit", methods=["POST"])
    def handle_commit():
        state = State.get_instance()
        ns = request.json["namespace"]
        version = request.json["version"]
        data = request.json["data"]
        try:
            success = state.commit(ns, version, data)
        except NotAtHeadVersionError:
            resp = jsonify({
                "error": "not_at_head_version",
            })
            resp.status_code = 412
            return resp
        except InvalidNamespaceError:
            resp = jsonify({
                "error": "invalid_namespace",
            })
            resp.status_code = 400
            return resp
        return jsonify({})

    @app.route("/api/fetch", methods=["POST"])
    def handle_fetch():
        state = State.get_instance()
        ns = request.json["namespace"]
        version = request.json["version"]
        try:
            resp = state.fetch(ns, version)
            return jsonify({
                "version": resp.version,
                "data": resp.data,
            })
        except InvalidNamespaceError:
            resp = jsonify({
                "error": "invalid_namespace",
            })
            resp.status_code = 400
            return resp
        except FetchTimeoutError:
            resp = jsonify({
                "error": "timeout",
            })
            resp.status_code = 408
            return resp