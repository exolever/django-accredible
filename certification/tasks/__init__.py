import celery

from celery import current_app as app

from .create_accredible_group import CreateAccredibleGroupTask  # noqa
from .create_accredible_consultant_role_group import CreateAccredibleConsultantRoleGroupTask  # noqa
from .create_accredible_simple_credential import CreateAccredibleSimpleCredentialTask  # noqa
from .create_accredible_group_credential import CreateAccredibleGroupCredentialTask  # noqa
from .delete_accredible_group import DeleteAccredibleGroupTask  # noqa
from .update_accredible_group import UpdateAccredibleGroupTask  # noqa

if '5.2' in celery.__version__:
    app.register_task(CreateAccredibleGroupTask())
    app.register_task(CreateAccredibleConsultantRoleGroupTask())
    app.register_task(CreateAccredibleSimpleCredentialTask())
    app.register_task(CreateAccredibleGroupCredentialTask())
    app.register_task(DeleteAccredibleGroupTask())
    app.register_task(UpdateAccredibleGroupTask())

else:
    app.tasks.register(CreateAccredibleGroupTask())
    app.tasks.register(CreateAccredibleConsultantRoleGroupTask())
    app.tasks.register(CreateAccredibleSimpleCredentialTask())
    app.tasks.register(CreateAccredibleGroupCredentialTask())
    app.tasks.register(DeleteAccredibleGroupTask())
    app.tasks.register(UpdateAccredibleGroupTask())
