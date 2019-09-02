=============================
django-accredible
=============================

.. image:: https://badge.fury.io/py/django-accredible.svg
    :target: https://badge.fury.io/py/django-accredible

.. image:: https://requires.io/github/exolever/django-accredible/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-accredible/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-accredible.svg?branch=master
    :target: https://travis-ci.org/exolever/django-accredible

.. image:: https://codecov.io/gh/exolever/django-accredible/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-accredible

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-accredible&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-accredible
  
.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/exolever/django-accredible/issues
    
.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT

Integrate Accredible certification in a Django App



Quickstart
----------

Install django-accredible::

    pip install django-accredible

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'certification',
        ...
    )

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
