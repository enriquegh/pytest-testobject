=================
pytest-testobject
=================

.. image:: https://travis-ci.org/enriquegh/pytest-testobject.svg?branch=master
    :target: https://travis-ci.org/enriquegh/pytest-testobject
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/enriquegh/pytest-testobject?branch=master
    :target: https://ci.appveyor.com/project/enriquegh/pytest-testobject/branch/master
    :alt: See Build Status on AppVeyor

Plugin to use TestObject Suites with Pytest

----

This `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `Cookiecutter-pytest-plugin`_ template.


Features
--------

* Use TestObject's Suites feature to group types of tests.
* Run tests with different iOS and Android devices without re-writing code


Requirements
------------

See `requirements.txt`_

To run from source install via:
::

 $ pip install -r requirements.txt


Installation
------------

You can install "pytest-testobject" via `pip`_ from `PyPI`_
::

 $ pip install pytest-testobject


Usage
-----

Add your credentials via the following flags:

::

 --to-username=TO_USERNAME
 --to-api-key=TO_API_KEY
 --to-suite-id=TO_SUITE_ID


For these to work your tests need to be on a class.

Add the fixtures to_suite and to_driver to your class.
Then use the to_driver fixture on your tests as your driver instance.

So it'll look something like this:

.. code-block:: python

    @pytest.mark.usefixtures("to_suite","to_driver")
    class TestTODriver(object):

        def test_saucelabs(self, to_driver):
            #Do stuff like to_driver.get(...)

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-testobject" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/enriquegh/pytest-testobject/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`requirements.txt`: requirements.txt