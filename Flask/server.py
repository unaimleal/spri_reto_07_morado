from flask import Flask, render_template, request
import bbdd.con_sql as sql


app = Flask(__name__)