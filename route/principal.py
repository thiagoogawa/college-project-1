
from flask import Blueprint, request, jsonify, render_template
from database.database import executar_comando
from datetime import date
import smtplib
from email.message import EmailMessage
from decimal import Decimal
from datetime import datetime

principal = Blueprint('/', __name__)

@principal.route('/', methods=['GET'])
def exibi_form_principal():
    return render_template('pagina-principal.html')