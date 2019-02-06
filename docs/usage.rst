=====
Usage
=====

To use django-accredible in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'certification.apps.CertificationConfig',
        ...
    )

Add django-accredible's URL patterns:

.. code-block:: python

    from certification import urls as certification_urls


    urlpatterns = [
        ...
        url(r'^', include(certification_urls)),
        ...
    ]
