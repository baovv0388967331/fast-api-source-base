import unittest

from fastapi.testclient import TestClient

from src.main import app


class BaseTest(unittest.TestCase):
    client = TestClient(app)
