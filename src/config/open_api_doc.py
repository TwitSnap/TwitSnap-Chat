from fastapi.openapi.utils import get_openapi


def configure_openapi(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Twit-Snap User Service",
            version="1.0.0",
            routes=app.routes,
        )
        for path, path_item in openapi_schema["paths"].items():
            if path.startswith("/api/v1"):
                for method in path_item.values():
                    if "parameters" not in method:
                        method["parameters"] = []
                    method["parameters"].append(
                        {
                            "in": "header",
                            "name": "user_id",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "user id",
                        }
                    )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
