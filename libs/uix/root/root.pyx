# cython: language_level
import json
import logging
from typing import Optional
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screenmanager import MDScreenManager

from libs.applibs import utils