import threading
import psycopg2
from selenium.webdriver.common.by import By
import pathlib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

class Baza():
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", user="user", password="SecretPassword")
        self.conn.autocommit = True