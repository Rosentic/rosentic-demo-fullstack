from __future__ import annotations

import importlib
import json
import re
import unittest
from pathlib import Path

import yaml
from graphql import build_schema, get_operation_ast, get_variable_values, parse, validate
from graphql.language.ast import DocumentNode


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "tests" / "contracts"


def load_contract_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CONTRACT_DIR.glob("*.json"))
    ]


def resolve_callable(reference: str):
    module_name, _, function_name = reference.partition(":")
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def route_matches(template: str, path: str) -> bool:
    template = template.rstrip("/") or "/"
    path = path.rstrip("/") or "/"
    template_parts = template.strip("/").split("/")
    path_parts = path.strip("/").split("/")
    if len(template_parts) != len(path_parts):
        return False
    return all(
        left == right or (left.startswith("{") and left.endswith("}"))
        for left, right in zip(template_parts, path_parts)
    )


def declared_http_routes() -> set[tuple[str, str]]:
    from backend.services.user_service import router

    routes: set[tuple[str, str]] = set()
    for route in router.routes:
        for method in route.methods or ():
            if method not in {"HEAD", "OPTIONS"}:
                routes.add((method, route.path))

    go_source = (ROOT / "gateway" / "routes.go").read_text(encoding="utf-8")
    for match in re.finditer(r'mux\.HandleFunc\("([^"]+)"', go_source):
        block = go_source[match.start():match.start() + 500]
        method_match = re.search(r"r\.Method\s*!=\s*http\.Method(\w+)", block)
        if method_match:
            routes.add((method_match.group(1).upper(), match.group(1).rstrip("/")))

    openapi = yaml.safe_load((ROOT / "api" / "openapi.yaml").read_text(encoding="utf-8"))
    for path, operations in openapi.get("paths", {}).items():
        for method in operations:
            if method.lower() in {"get", "post", "put", "patch", "delete"}:
                routes.add((method.upper(), path))
    return routes


def openapi_request_schema(method: str, path: str) -> dict:
    document = yaml.safe_load((ROOT / "api" / "openapi.yaml").read_text(encoding="utf-8"))
    operation = document["paths"][path][method.lower()]
    schema = operation["requestBody"]["content"]["application/json"]["schema"]
    if "$ref" in schema:
        target = document
        for part in schema["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        schema = target
    return schema


def proto_messages() -> dict[str, set[str]]:
    source = (ROOT / "proto" / "order.proto").read_text(encoding="utf-8")
    source = re.sub(r"//.*", "", source)
    messages: dict[str, set[str]] = {}
    for message in re.finditer(r"message\s+(\w+)\s*\{([^}]*)\}", source, re.DOTALL):
        fields = {
            field.group(1)
            for field in re.finditer(
                r"(?:repeated\s+)?[\w.<>]+\s+(\w+)\s*=\s*\d+",
                message.group(2),
            )
        }
        messages[message.group(1)] = fields
    return messages


class DemoContractProof(unittest.TestCase):
    def test_python_entrypoints_execute(self):
        for case in load_contract_cases():
            for call in case.get("python_calls", []):
                with self.subTest(case=case["name"], call=call["call"]):
                    result = resolve_callable(call["call"])(*call.get("args", []))
                    if "expected" in call:
                        self.assertEqual(call["expected"], result)
                    for key, value in call.get("expected_subset", {}).items():
                        self.assertEqual(value, result[key])

    def test_http_consumers_resolve_to_a_declared_route(self):
        routes = declared_http_routes()
        for case in load_contract_cases():
            for request in case.get("http_requests", []):
                with self.subTest(case=case["name"], request=request):
                    self.assertTrue(
                        any(
                            request["method"] == method
                            and route_matches(template, request["path"])
                            for method, template in routes
                        ),
                        f"{request['method']} {request['path']} has no provider route",
                    )

    def test_openapi_requests_include_every_required_field(self):
        for case in load_contract_cases():
            for request in case.get("openapi_requests", []):
                with self.subTest(case=case["name"], request=request):
                    schema = openapi_request_schema(request["method"], request["path"])
                    missing = set(schema.get("required", [])) - set(request["body"])
                    self.assertEqual(set(), missing, f"missing required request fields: {sorted(missing)}")

    def test_graphql_operations_and_variables_match_the_schema(self):
        schema = build_schema((ROOT / "schema" / "schema.graphql").read_text(encoding="utf-8"))
        for case in load_contract_cases():
            for operation_case in case.get("graphql_operations", []):
                with self.subTest(case=case["name"], operation=operation_case["operation"]):
                    document = parse(
                        (ROOT / operation_case["file"]).read_text(encoding="utf-8")
                    )
                    operation = get_operation_ast(document, operation_case["operation"])
                    self.assertIsNotNone(operation)
                    operation_document = DocumentNode(definitions=(operation,))
                    self.assertEqual([], validate(schema, operation_document))
                    variable_result = get_variable_values(
                        schema,
                        operation.variable_definitions,
                        operation_case.get("variables", {}),
                    )
                    self.assertIsInstance(variable_result, dict, variable_result)

    def test_proto_consumers_only_use_declared_fields(self):
        messages = proto_messages()
        for case in load_contract_cases():
            for usage in case.get("proto_fields", []):
                with self.subTest(case=case["name"], usage=usage):
                    self.assertIn(usage["message"], messages)
                    missing = set(usage["fields"]) - messages[usage["message"]]
                    self.assertEqual(set(), missing, f"removed proto fields still used: {sorted(missing)}")

    def test_contract_cases_are_grounded_in_consumer_source(self):
        for case in load_contract_cases():
            for assertion in case.get("source_contains", []):
                with self.subTest(case=case["name"], file=assertion["file"]):
                    source = (ROOT / assertion["file"]).read_text(encoding="utf-8")
                    for needle in assertion["needles"]:
                        self.assertIn(needle, source)


if __name__ == "__main__":
    unittest.main()
