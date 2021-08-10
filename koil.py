from flask import Flask,render_template,redirect,request,flash,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message,Mail
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
import hashlib
from flask_login import LoginManager as l
from flask_login import current_user,UserMixin,login_user,logout_user,UserMixin,login_required
from flask_bcrypt import Bcrypt as B
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as st
import os
from PIL import Image
app=Flask(__name__,template_folder='templates')
nam='Antony1a'
key=hashlib.md5(nam.encode('utf-8')).hexdigest()
app.config['SECRET_KEY']=key
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///jimmy.db'
data=SQLAlchemy(app)
lm=l(app)
@lm.user_loader
def load_user(m_id):
    return member.query.get(int(m_id))
class member(data.Model,UserMixin):
    id=data.Column(data.Integer,primary_key=True)
    email=data.Column(data.String(40),nullable=False)
    password=data.Column(data.String,nullable=False)
    image=data.Column(data.String(50),nullable=False,default='default.jpg')
    rela=data.relationship('content',backref="author",lazy=True)
    def __repr__(self):
        return str(self.id)
class about(data.Model):
    id=data.Column(data.Integer,primary_key=True)
    service1=data.Column(data.Text,nullable=False)
    s1_pic=data.Column(data.String(50),nullable=False,default='default.jpg')
    service2=data.Column(data.Text,nullable=False)
    s2_pic=data.Column(data.String(50),nullable=False,default='default.jpg')
    service3=data.Column(data.Text,nullable=False)
    s3_pic=data.Column(data.String(50),nullable=False,default='default.jpg')
    def __repr__(self):
        return str(self.id)
class content(data.Model):
    id=data.Column(data.Integer,primary_key=True)
    title=data.Column(data.Integer,nullable=False)
    date=data.Column(data.DateTime,nullable=False,default=datetime.utcnow)
    video=data.Column(data.String(50),nullable=True,default="default.mp4")
    posts=data.Column(data.Text,nullable=False)
    pics=data.Column(data.String(50),nullable=True)
    m_id=data.Column(data.Integer,data.ForeignKey('member.id'),nullable=False)
    def __repr__(self):
        return str(self.id)
class comments(data.Model):
    id=data.Column(data.Integer,primary_key=True)
    name=data.Column(data.String(50),nullable=True)
    comment=data.Column(data.Text,nullable=True)
class logform(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email(message='invalid email')])
    password=PasswordField('password',validators=[DataRequired(),Length(min=8,max=30)])
    remember=BooleanField('remember me')
    submit=SubmitField('login')
class poster(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    posts= TextAreaField('posts',validators=[DataRequired()])
    pic=FileField('post picture',validators=[FileAllowed(['jpg','png'])])
    vid=StringField('post video (copy youtube video link)')
    submit=SubmitField('post')
class abouts(FlaskForm):
    service1= TextAreaField('first service you offer',validators=[DataRequired()])
    pic1=FileField('add picture about it',validators=[FileAllowed(['jpg','png'])])
    service2= TextAreaField('second service you offer',validators=[DataRequired()])
    pic2=FileField('add picture about it',validators=[FileAllowed(['jpg','png'])])
    service3= TextAreaField('third service you offer',validators=[DataRequired()])
    pic3=FileField('add picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField("ADD")
class logform(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email(message='invalid email')])
    password=PasswordField('password',validators=[DataRequired(),Length(min=5,max=30)])
    remember=BooleanField('remember me')
    submit=SubmitField('login')
def pi_save(pi):
    rand_he=secrets.token_hex(8)
    _,ex=os.path.splitext(pi.filename)
    pi_fname=rand_he + ex
    pi_path=os.path.join(app.root_path,'static/images',pi_fname)
    out_size=(301,222)
    im=Image.open(pi)
    im.thumbnail(out_size)
    im.save(pi_path)
    return pi_fname
@app.route('/')
def home():
    latests=content.query.order_by(content.date.desc())
    commen=comments.query.all()
    abts=about.query.all()
    abt_imag1="static/images/"+abts[0].s1_pic
    abt_imag2="static/images/"+abts[0].s2_pic
    abt_imag3="static/images/"+abts[0].s2_pic
    latest=[]
    imag_path=[]
    print(latests[0].video)
    for i in latests:
        image_p=os.path.join("static/images",i.pics)
        imag_path.append(image_p)
        latest.append(" ".join(i.posts.split()[0:30]))
    return render_template("new.html",latest=latest,latests=latests,abts=abts,abt_imag1=abt_imag1,abt_imag2=abt_imag2,abt_imag3=abt_imag3,imag_path=imag_path,commen=commen)
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(''))
    form=logform()
    if form.validate_on_submit():
        credentials=member.query.filter_by(email=form.email.data).first()
        if credentials and credentials.password:
            login_user(credentials,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'invalid email or password','danger')
    return render_template('login.html',form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@login_required
@app.route('/about',methods=["GET","POST"])
def abbt():
    form=abouts()
    serv=about.query.all()
    if form.validate_on_submit():
        print(form.pic1.data)
        pic_1=pi_save(form.pic1.data)
        pic_2=pi_save(form.pic2.data)
        pic_3=pi_save(form.pic3.data)
        abts=about(service1=form.service1.data,s1_pic=pic_1,service2=form.service2.data,s2_pic=pic_2,service3=form.service3.data,s3_pic=pic_3)
        data.session.add(abts)
        data.session.commit()
        return redirect(url_for('home'))
        flash('about created successfully','success')
    return render_template('about.html',form=form,serv=serv)
@login_required
@app.route('/post',methods=["GET","POST"])
def post():
    form=poster()
    if form.validate_on_submit():
        pic_f=pi_save(form.pic.data)
        pi_dir="static/images/"+pic_f
        post=content(title=form.title.data,video=form.vid.data,posts=form.posts.data,author=current_user,pics=pi_dir)
        data.session.add(post)
        data.session.commit()
        return redirect(url_for('blog'))
        flash('post created successfully','success')
    return render_template('post.html',form=form)
@app.route('/blog',methods=['GET','POST'])
def blog():
    page=request.args.get('page',type=int)
    pos=content.query.order_by(content.date.desc())
    commen=comments.query.order_by(comments.id.desc())
    imag=[]
    post=[]
    for p in pos:
        imag.append(p.pics)
        post.append(p.title)
    posts=content.query.order_by(content.date.desc()).paginate(page=page,per_page=5)
    print(imag)
    if request.method=="POST":
        name=request.form["name"]
        comment=request.form["comments"]
        co=comments(name=name,comment=comment)
        data.session.add(co)
        data.session.commit()
    return render_template('afri.html',posts=posts,imag=imag,post=post,commen=commen)
@app.route('/donate')
def donate():
    return render_template('donate.html')
@login_required
@app.route('/editing')
def editing():
    cont=content.query.order_by(content.date.desc())
    return render_template('ed.html',cont=cont)
@login_required
@app.route('/editing/<int:id>/update',methods=['GET','POST'])
def update(id):
    conte=content.query.get_or_404(id)
    if conte.author!=current_user:
        abort(403)
    form=poster()
    if form.validate_on_submit():
        conte.title=form.title.data
        conte.posts=form.posts.data
        data.session.commit()
        flash('post updated successfully')
        return redirect(url_for('blog',id=conte.id))
    elif request.method=='GET':
        form.title.data=conte.title
        form.posts.data=conte.posts
    return render_template('update.html',form=form,title='update post')
@login_required
@app.route('/editing/<int:id>/delete',methods=['GET','POST'])
def delete(id):
    cont=content.query.get_or_404(id)
    if cont.author!=current_user:
        abort(403)
    data.session.delete(cont)
    data.session.commit()
    flash(f'post deleted successfully','success')
    return redirect(url_for('blog'))
@login_required
@app.route('/about/<int:id>/dele',methods=['GET','POST'])
def del_serv(id):
    service=about.query.get_or_404(id)
    data.session.delete(service)
    data.session.commit()
    flash(f'service deleted successfully','success')
    return redirect(url_for('blog'))
if __name__=="__main__":
    app.run(debug=True)
