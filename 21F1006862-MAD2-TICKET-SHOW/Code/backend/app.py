import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from flask_caching import Cache
import redis
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
from celery import Celery
from celery.schedules import crontab

app = Flask(__name__)




app.config['JWT_SECRET_KEY'] = 'my_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


mail= MIMEMultipart()


cache = Cache(app, config={'CACHE_TYPE': 'RedisCache','Cache_REDIS_HOST':'localhost','Cache_REDIS_PORT':6379,'Cache_REDIS_DB':0})

cache.init_app(app)



db = SQLAlchemy(app)


CORS(app)

jwt = JWTManager(app)




redis_client = redis.Redis(host='localhost', port=6379, db=0)



celery_app = Celery('tasks', broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/1")

celery_app.conf.timezone = 'Asia/Kolkata'
app.config['CELERY_BEAT_TIMEZONE'] = 'Asia/Kolkata'

@celery_app.on_after_configure.connect
def daily_task(sender, **kwargs):
    sender.add_periodic_task(crontab(hour = 8,minute =0), dailyreminder.s(), name='send_daily_reminder')
    sender.add_periodic_task(crontab(day_of_month=1,hour=8, minute=0), monthlyreport.s(), name='send_monthly_report')
    sender.add_periodic_task(crontab(day_of_month=1, hour=8, minute=0), export.s(), name='export_data')


# celery -A app:celery_app worker -l info -P eventlet
# celery -A app:celery_app beat -l info

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name= db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password= db.Column(db.String(30), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    def __repr__(self):
        return f'User({self.email})'
    def __init__ (self,name,email,password,role_id):
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

class Movie(db.Model):
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    name= db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    rating= db.Column(db.String(30), nullable=False)
    shows=db.relationship('Shows',backref=db.backref('movie', lazy=True))
    def __init__ (self,name,genre,rating):
        self.name = name
        self.genre = genre
        self.rating = rating
class Shows(db.Model):
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    def __init__ (self,theater_id,ticket_price,available_tickets,datetime,movie_id):
        self.theater_id = theater_id
        self.ticket_price = ticket_price
        self.available_tickets = available_tickets
        self.datetime = datetime
        self.movie_id = movie_id
class Role(db.Model):
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    name= db.Column(db.String(30), nullable=False)
    users=db.relationship('User',backref=db.backref('role', lazy=True))
    def __init__ (self,name):
        self.name = name

class Ticket(db.Model):
        id = db.Column(db.Integer,autoincrement=True , primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
        nooftickets = db.Column(db.Integer, nullable=False)
        ticket_price = db.Column(db.Integer,db.ForeignKey('shows.ticket_price'), nullable=False)
        def __init__ (self,user_id,show_id,nooftickets,ticket_price):
            self.user_id = user_id
            self.show_id = show_id
            self.nooftickets = nooftickets
            self.ticket_price = ticket_price

class Theaters(db.Model):
    id = db.Column(db.Integer,autoincrement=True , primary_key=True)
    name= db.Column(db.String(30), nullable=False)
    place= db.Column(db.String(30), nullable=False)
    capacity= db.Column(db.Integer, nullable=False)
    shows=db.relationship('Shows',backref=db.backref('theaters', lazy=True))
    def __init__ (self,name,place,capacity):
        self.name = name
        self.place = place
        self.capacity = capacity

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Users only!"), 403

        return decorator

    return wrapper




@celery_app.task
def monthlyreport():
      with app.app_context():
        user = User.query.all()
        for user in user:           
            tickets = Ticket.query.filter_by(user_id=user.id).all()
            ticketlist = []
            for ticket in tickets:
                if ticket is not None:
                    show = Shows.query.filter_by(id=ticket.show_id).one_or_none()
                    movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
                    username = User.query.filter_by(id=ticket.user_id).one_or_none().name
                    date = show.datetime.strftime("%Y/%m/%d")
                    time = show.datetime.strftime("%H:%M")
                    theater_name = Theaters.query.filter_by(id=show.theater_id).one_or_none().name
                    ticketlist.append({'id':ticket.id,'name': movie.name, 'ticket_price': ticket.ticket_price, 'nooftickets': ticket.nooftickets, 'username': username, 'theater_name': theater_name, 'date': date, 'time': time})
            #generate monthly report in html and send it to via email
            html = "<html><body><table><tr><th>Movie Name</th><th>Ticket Price</th><th>No of Tickets</th><th>User Name</th><th>Theater Name</th><th>Date</th><th>Time</th></tr>"
            for ticket in ticketlist:
                html = html + "<tr><td>"+ticket['name']+"</td><td>"+str(ticket['ticket_price'])+"</td><td>"+str(ticket['nooftickets'])+"</td><td>"+ticket['username']+"</td><td>"+ticket['theater_name']+"</td><td>"+ticket['date']+"</td><td>"+ticket['time']+"</td></tr>"
            html = html + "</table></body></html>"
            msg= MIMEText(html, 'html')
            mail = smtplib.SMTP("localhost", 1025)
            mail.login("adm@adm.com", "1234")

            mail.sendmail("adm@adm.com", user.email , msg.as_string())
            mail.close()

        return "email sent"

@celery_app.task
def dailyreminder():
  with app.app_context():
    users = User.query.all()
    for user in users:
        tickets = Ticket.query.filter_by(user_id=user.id).all()
        if len(tickets) == 0:
            msg = MIMEText("It seems you have not booked any tickets yet. Book now!")
            mail = smtplib.SMTP("localhost", 1025)
            mail.login("", "1234")
            email = user.email
            mail.sendmail("adm@adm.com", email , msg.as_string())
            mail.close()

        return "email sent"
# export all the data to a csv file
@celery_app.task
def export():
    with app.app_context():
        shows = Shows.query.all()
        showlist = []
        for show in shows:
            theater = Theaters.query.filter_by(id=show.theater_id).one_or_none()
            theater_name = theater.name
            movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
            date = show.datetime.strftime("%Y/%m/%d")
            time = show.datetime.strftime("%H:%M")
            booked_tickets = theater.capacity - show.available_tickets
            total_sales = booked_tickets * show.ticket_price
            showlist.append({'id':show.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating,  'ticket_price': show.ticket_price, 'available_tickets': show.available_tickets, 'theater_name': theater_name, 'date': date, 'time': time, 'booked_tickets': booked_tickets, 'total_sales': total_sales})
        #convert show list to csv
        file = open("export.csv", "w")
        file.write("id,name,genre,rating,ticket_price,available_tickets,theater_name,date,time,booked_tickets,total_sales\n")
        for show in showlist:
            file.write(str(show['id'])+","+show['name']+","+show['genre']+","+show['rating']+","+str(show['ticket_price'])+","+str(show['available_tickets'])+","+show['theater_name']+","+show['date']+","+show['time']+","+str(show['booked_tickets'])+","+str(show['total_sales'])+"\n")
        file.close()
        msg = MIMEMultipart("Please find the attached csv file")
        with open("export.csv", "rb") as file:
            msga = MIMEBase("application", "octet-stream")
            msga.set_payload(file.read())
        msga.add_header("Content-Disposition", "attachment; filename=export.csv")
        encoders.encode_base64(msga)
        msg.attach(msga)
        
        mail = smtplib.SMTP("localhost", 1025)
        mail.login("abc@abc.com", "1234")

        mail.sendmail("abc@abc.com", "adm@adm.com", msg.as_string())
        mail.close()


        return "email sent"

@app.route('/')
@cache.memoize(timeout=10)
@jwt_required()
def getshows():
    shows = Shows.query.all()
    showlist = []
    for show in shows:
        theater_name = Theaters.query.filter_by(id=show.theater_id).one_or_none().name
        movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
        date = show.datetime.strftime("%Y/%m/%d")
        time = show.datetime.strftime("%H:%M")
        showlist.append({'id':show.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating,  'ticket_price': show.ticket_price, 'available_tickets': show.available_tickets, 'theater_name': theater_name, 'date': date, 'time': time})
    return jsonify({'message': "success",'shows': showlist})



@app.route('/getmovies', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=10)
def getmovies():
    movies = Movie.query.all()
    movielist = []
    for movie in movies:
        movielist.append({'id':movie.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating})
    return jsonify({'message':'success','movies': movielist})

    
@app.route('/getmovie/<int:id>', methods=['GET'])
@cache.memoize(timeout=10)
@jwt_required()
def getmovie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is not None:
        movies={}
        movies['id']=movie.id
        movies['name']=movie.name
        movies['genre']=movie.genre
        movies['rating']=movie.rating
        return jsonify({'message': 'success', 'movie': movies}),200
    else:
        return jsonify({'message': 'failed'}),401
@app.route('/editmovie/<int:id>', methods=['POST'])
@cache.memoize(timeout=10)
@admin_required()
def editmovie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is not None:
        data = request.json
        name = data.get('name')
        genre = data.get('genre')
        rating = data.get('rating')
        movie.name = name
        movie.genre = genre
        movie.rating = rating
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'}),401

@app.route('/deletemovie/<int:id>', methods=['POST'])
@cache.memoize(timeout=10)
@admin_required()
def deletemovie(id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    shows = Shows.query.filter_by(movie_id=id).all()
    if movie is not None:
        for show in shows:
            db.session.delete(show)
            ticket = Ticket.query.filter_by(show_id=show.id).all()
            for ticket in ticket:
                db.session.delete(ticket)
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'}),401
    
@app.route('/viewshow/<int:id>', methods=['GET'])
@cache.memoize(timeout=10)
@jwt_required()
def viewshow(id):
    show = Shows.query.filter_by(movie_id=id).all()
    movie = Movie.query.filter_by(id=id).one_or_none()
    showlist = []
    for show in show:
        theater_name = Theaters.query.filter_by(id=show.theater_id).one_or_none().name
        date = show.datetime.strftime("%Y/%m/%d")
        time = show.datetime.strftime("%H:%M")
        showlist.append({'id':show.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating,  'ticket_price': show.ticket_price, 'available_tickets': show.available_tickets, 'theater_name': theater_name, 'date': date, 'time': time})
    return jsonify({'message': "success",'show': showlist})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_id = 2
    userlist = User.query.all()
    for user in userlist:
        if user.email == email:
            return jsonify({'message': 'user already exists'})
    new_user = User(name=name,email=email,password=generate_password_hash(password),role_id=role_id)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'user created successfully'})

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).one_or_none()
        if user is not None:
            if user.role_id==1 and  check_password_hash(user.password, password):
                access_token = create_access_token(identity=email, additional_claims={"is_administrator": True})
                return jsonify({'message': 'admin login successful', 'access_token': access_token}),200
            elif check_password_hash(user.password, password):
                access_token = create_access_token(identity=email, additional_claims={"is_administrator": False})
                return jsonify({'message': 'login successful', 'access_token': access_token}),200
        else:
            return jsonify({'message': 'failed'})
@app.route('/checklogin', methods=['GET'])
@jwt_required()
def checklogin():
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).one_or_none()
    if user is not None:
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'})

@app.route('/bookshow/<int:id>', methods=['POST'])
@user_required()
def bookshow(id):
    data = request.json
    nooftickets = data.get('nooftickets')
    show = Shows.query.filter_by(id=id).one_or_none() 
    ticket_price = show.ticket_price
    if show.available_tickets < nooftickets:
        return jsonify({'message': 'houseful'})
    else:
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).one_or_none()
        new_ticket = Ticket(user_id=user.id,show_id=id,nooftickets=nooftickets,ticket_price=ticket_price*nooftickets)
        show.available_tickets = show.available_tickets - nooftickets
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({'message': 'success'}),200

@app.route('/search/<string:name>', methods=['GET'])
@jwt_required()
def search(name):
    movies = Movie.query.filter(Movie.name.ilike('%'+ name +'%')).all()
    movielist = []
    for movie in movies:
        show = Shows.query.filter_by(movie_id=movie.id).all()
        for show in show:
            date = show.datetime.strftime("%Y/%m/%d")
            time = show.datetime.strftime("%H:%M")
            movielist.append({'id':movie.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating,'show_id': show.id, 'ticket_price': show.ticket_price, 'available_tickets': show.available_tickets, 'theater_name': Theaters.query.filter_by(id=show.theater_id).one_or_none().name, 'date': date, 'time': time})
    return jsonify({'message':'success','movies': movielist})



@app.route('/createshow', methods=['POST'])
@admin_required()
def createshow():
    data = request.json
    movie_id = data.get('movie_id')
    theaterid = data.get('theaterid')
    ticket_price = data.get('ticket_price')
    date=data.get('date')
    time=data.get('time')
    datetime1 = datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M')
    capacity = Theaters.query.filter_by(id=theaterid).one_or_none().capacity
    new_show = Shows(movie_id=movie_id,theater_id=theaterid,ticket_price=ticket_price,available_tickets=capacity,datetime=datetime1)
    db.session.add(new_show)
    db.session.commit()
    return jsonify({'message': 'show created successfully'})

@app.route('/createmovie', methods=['POST'])
@admin_required()
def createmovie():
    data = request.json
    name = data.get('name')
    genre = data.get('genre')
    rating = data.get('rating')
    new_movie = Movie(name=name,genre=genre,rating=rating)
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({'message': 'movie created successfully'}),200

@app.route('/gettheaters', methods=['GET'])
@jwt_required()
def gettheaters():
    theaters = Theaters.query.all()
    theaterlist = []
    for theater in theaters:
        theaterlist.append({'id':theater.id,'name': theater.name, 'place': theater.place, 'capacity': theater.capacity})
    return jsonify({'message':'success','theaters': theaterlist})

@app.route('/createtheater', methods=['POST'])
@admin_required()
def createtheater():
    data = request.json
    name = data.get('name')
    place = data.get('place')
    capacity = data.get('capacity')
    new_theater = Theaters(name=name,place=place,capacity=capacity)
    db.session.add(new_theater)
    db.session.commit()
    return jsonify({'message': 'success'}),200

@app.route('/edittheater/<int:id>', methods=['POST'])
@admin_required()
def edittheater(id):
    theater = Theaters.query.filter_by(id=id).one_or_none()
    if theater is not None:
        data = request.json
        name = data.get('name')
        place = data.get('place')
        capacity = data.get('capacity')
        theater.name = name
        theater.place = place
        theater.capacity = capacity
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'})
    
@app.route('/deletetheater/<int:id>', methods=['POST'])
@admin_required()
def deletetheater(id):
    theater = Theaters.query.filter_by(id=id).one_or_none()
    shows=Shows.query.filter_by(theater_id=id).all()
    if theater is not None:
        for show in shows:
            db.session.delete(show)
            ticket = Ticket.query.filter_by(show_id=show.id).all()
            for ticket in ticket:
                db.session.delete(ticket)
        db.session.delete(theater)
        db.session.commit()
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'failed'})
        
    
@app.route('/gettheater/<int:id>', methods=['GET'])
@jwt_required()
def gettheater(id):
    theater = Theaters.query.filter_by(id=id).one_or_none()
    if theater is not None:
        theaters={}
        theaters['id']=theater.id
        theaters['name']=theater.name
        theaters['place']=theater.place
        theaters['capacity']=theater.capacity
        return jsonify({'message': 'success', 'theater': theaters}),200
    else:
        return jsonify({'message': 'failed'}),401
    
@app.route('/gettheatershows/<int:id>', methods=['GET'])
@jwt_required()
def getshowstheater(id):
    shows = Shows.query.filter_by(theater_id=id).all()
    showlist = []
    for show in shows:
        theater_name = Theaters.query.filter_by(id=show.theater_id).one_or_none().name
        movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
        date = show.datetime.strftime("%Y/%m/%d")
        time = show.datetime.strftime("%H:%M")
        showlist.append({'id':show.id,'name': movie.name, 'genre': movie.genre, 'rating': movie.rating,  'ticket_price': show.ticket_price, 'available_tickets': show.available_tickets, 'theater_name': theater_name, 'date': date, 'time': time})
    return jsonify({'message': "success",'shows': showlist, 'theater_name': theater_name})

@app.route('/getshow/<int:id>', methods=['POST'])
@jwt_required()
def getshow(id):
    show = Shows.query.filter_by(id=id).one_or_none()
    movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
    if show is not None:
        shows={}
        shows['id']=show.id
        shows['name']=movie.name
        shows['genre']=movie.genre
        shows['rating']=movie.rating
        shows['ticket_price']=show.ticket_price
        shows['available_tickets']=show.available_tickets
        shows['date']=show.datetime.strftime("%Y-%m-%d")
        shows['time']=show.datetime.strftime("%H:%M")
        return jsonify({'message': 'success', 'show': shows}),200
    else:
        return jsonify({'message': 'failed'}),401

@app.route('/editshow/<int:id>', methods=['POST'])
@admin_required()
def editshow(id):
    show = Shows.query.filter_by(id=id).one_or_none()
    movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
    if show is not None:
        data = request.json
        name = data.get('name')
        genre = data.get('genre')
        rating = data.get('rating')
        date=data.get('date')
        time=data.get('time')
        movie.name = name
        movie.genre = genre
        movie.rating = rating
        show.datetime = datetime.strptime(date+" "+time, '%Y-%m-%d %H:%M')
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'}),401

@app.route('/deleteshow/<int:id>', methods=['POST'])
@admin_required()
def deleteshow(id):
    show = Shows.query.filter_by(id=id).one_or_none()
    if show is not None:
        tickets = Ticket.query.filter_by(show_id=id).all()
        for ticket in tickets:
            db.session.delete(ticket)
        db.session.delete(show)
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'}),401
    
@app.route('/gettickets', methods=['GET'])
@jwt_required()
def gettickets():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).one_or_none()
    tickets = Ticket.query.filter_by(user_id=user.id).all()
    ticketlist = []
    for ticket in tickets:
        if ticket is not None:
            show = Shows.query.filter_by(id=ticket.show_id).one_or_none()
            movie = Movie.query.filter_by(id=show.movie_id).one_or_none()
            username = User.query.filter_by(id=ticket.user_id).one_or_none().name
            date = show.datetime.strftime("%Y/%m/%d")
            time = show.datetime.strftime("%H:%M")
            theater_name = Theaters.query.filter_by(id=show.theater_id).one_or_none().name
            ticketlist.append({'id':ticket.id,'name': movie.name, 'ticket_price': ticket.ticket_price, 'nooftickets': ticket.nooftickets, 'username': username, 'theater_name': theater_name, 'date': date, 'time': time})
    return jsonify({'message': "success",'tickets': ticketlist})


@app.route('/deleteticket/<int:id>', methods=['POST'])
@jwt_required()
def deleteticket(id):
    ticket = Ticket.query.filter_by(id=id).one_or_none()
    if ticket is not None:
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'}),401


@app.route('/checkadmin', methods=['GET'])
@jwt_required()
def checkadmin():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).one_or_none()
    if user.role_id == 1:
        return jsonify({'message': 'success'}),200
    else:
        return jsonify({'message': 'failed'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3435)
  
    
