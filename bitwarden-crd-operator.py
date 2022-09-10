#!/usr/bin/env python3
import kopf
import kubernetes
import base64
from jinja2 import Template


@kopf.on.create('bitwarden-secrets.lerentis.uploadfilter24.eu')
def create_fn(spec, name, namespace, logger, **kwargs):

    type = spec.get('type')
    id = spec.get('id')
    secret_name = spec.get('name')
    secret_namespace = spec.get('namespace')

    api = kubernetes.client.CoreV1Api()

    # TODO: this should better be a os lookup
    with open('/home/bw-operator/templates/username-password.yaml.j2') as file_:
        template = Template(file_.read())

    data = template.render(
        original_crd=name,
        secret_name=secret_name,
        namespace=secret_namespace,
        username=base64.b64encode("test"),
        password=base64.b64encode("test")
    )

    obj = api.create_namespaced_secret(
        namespace=secret_namespace,
        body=data
    )

    logger.info(f"Secret {name} is created: {obj}")


@kopf.on.update('bitwarden-secrets.lerentis.uploadfilter24.eu')
def my_handler(spec, old, new, diff, **_):
    pass

@kopf.on.delete('bitwarden-secrets.lerentis.uploadfilter24.eu')
def my_handler(spec, **_):
    pass