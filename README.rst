.. |pypi_version| image:: https://badge.fury.io/py/sunix-ledstrip-controller-client.svg
    :target: https://badge.fury.io/py/sunix-ledstrip-controller-client

sunix-ledstrip-controller-client  |pypi_version|
================================

A python 3.4+ library for controlling the Sunix® RGB / RGBWWCW WiFi LED Strip controller.

Build Status
============

.. |build_master| image:: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client.svg?branch=master
    :target: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client/branches

.. |build_beta| image:: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client.svg?branch=beta
    :target: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client/branches

.. |build_dev| image:: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client.svg?branch=dev
    :target: https://travis-ci.org/markusressel/sunix-ledstrip-controller-client/branches


.. |codebeat_master| image:: https://codebeat.co/badges/9dd4227d-a247-4c9b-9091-7472f3e19434
    :target: https://codebeat.co/projects/github-com-markusressel-sunix-ledstrip-controller-client-master

.. |codebeat_beta| image:: https://codebeat.co/badges/68d80d07-2c69-4320-9f0a-02165dafae11
    :target: https://codebeat.co/projects/github-com-markusressel-sunix-ledstrip-controller-client-beta

.. |codebeat_dev| image:: https://codebeat.co/badges/256be541-3755-45f3-91ca-12f1257cd9a5
    :target: https://codebeat.co/projects/github-com-markusressel-sunix-ledstrip-controller-client-dev

+--------------------+------------------+-----------------+
| Master             | Beta             | Dev             |
+====================+==================+=================+
| |build_master|     | |build_beta|     | |build_dev|     |
+--------------------+------------------+-----------------+
| |codebeat_master|  | |codebeat_beta|  | |codebeat_dev|  |
+--------------------+------------------+-----------------+


How to use
==========

Installation
------------

:code:`pip install sunix-ledstrip-controller-client`

Usage
-----

For a basic example have a look at the `example.py <https://github.com/markusressel/sunix-ledstrip-controller-client/blob/master/example.py>`_ file.
If you need more info have a look at the `documentation <http://sunix-ledstrip-controller-client.readthedocs.io/>`_ which should help.

Basic Example
=============

Create the :code:`LEDStripControllerClient` object
--------------------------------------------------

The first thing you need to communicate with any controller is the api client.
Create one like this:

.. code-block:: python

    from sunix_ledstrip_controller_client import LEDStripControllerClient

    api = LEDStripControllerClient()

The next thing you need is a :code:`Controller` object that specifies the basics about your Sunix controller hardware.
You can either let the api search automatically for your controller using:

.. code-block:: python

    devices = api.discover_controllers()

or create one manually like this:

.. code-block:: python

    from sunix_ledstrip_controller_client.controller import Controller
    device = Controller("192.168.2.23")

or including a port if you want to access it from outside of your local network:

.. code-block:: python

    device = Controller("192.168.2.23", 12345)

Turn it on!
-----------

Now you have all that is needed to control your device. It's time to turn it on and off!
Use this method to turn it on:

.. code-block:: python

    api.turn_on(device)

and this to turn it off:

.. code-block:: python

    api.turn_off(device)

Make it a rainbow (changing colors)
-----------------------------------

Now to the fun part. The RGB values and the WW (warm white and cold white) value can be adjusted
separately (while keeping the other value) or both at the same time.

All values have a valid range of :code:`0` to :code:`255`.

If you only want to change the RGB values use:

.. code-block:: python

    api.set_rgb(device, 255, 255, 255)

and this one if you only want to change the WW value:

.. code-block:: python

    api.set_ww(device, 255, 255)

To set both at the same time use (you guessed it):

.. code-block:: python

    api.set_rgbww(device, 255, 255, 255, 255, 255)

Functions
---------

The official app for the Sunix controller offers 20 different functions that can be activated and customized in speed.
These functions are hardcoded in the controller so they can not be altered in any way.
You can activate them though using:

.. code-block:: python

    from sunix_ledstrip_controller_client.functions import FunctionId
    api.set_function(device, FunctionId.RED_GRADUAL_CHANGE, 240)

Function ids can be found in the :code:`FunctionId` enum class.

**0 is slow - 255 is fast.**

In the network protocol the speed is actually reversed (0 is fast, 255 is slow) but I changed this for the sake of simplicity.
You should be aware though that the **speed curve seems to be exponential**. This means 255 is very fast but 240 is
already **a lot** slower.

Custom Functions
----------------

Another feature of the official app is to set a custom color loop with a custom transition and speed between the colors.
Since v1.2.0 of this library you can set those too :)

Simply have a look at the `example_custom_function.py <https://github.com/markusressel/sunix-ledstrip-controller-client/blob/master/example_custom_function.py>`_ file
for a detailed example.

Set/Get Time
------------

The Sunix® controller has a build in clock to be able to execute timer actions.
Currently there is no way to get or set timers with this library.
You can however get and set the current time of the controller.

To get the currently set time use:

.. code-block:: python

    time = api.get_time(device)

To set a new value use:

.. code-block:: python

    dt = datetime.datetime.now()
    api.set_time(device, dt)


Attributions
============

I want to give a huge shoutout to `Chris Mullins (alias sidoh) <https://github.com/sidoh>`_ and his
`ledenet_api <https://github.com/sidoh/ledenet_api>`_ library. Although the protocol used by the sunix controller
is not exactly the same to the one used by the LEDENET Magic UFO controller it's quite similar and his work was a
great starting point for me.

Contributing
============

Github is for social coding: if you want to write code, I encourage contributions through pull requests from forks
of this repository. Create Github tickets for bugs and new features and comment on the ones that you are interested in.

License
=======

::

    sunix-ledstrip-controller-client by Markus Ressel
    Copyright (C) 2017  Markus Ressel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

