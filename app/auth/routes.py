from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.data_manager import load_users
from . import auth_bp

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html')
