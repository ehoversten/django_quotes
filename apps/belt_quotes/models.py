from __future__ import unicode_literals
from django.db import models
from datetime import datetime
# --- Import VALIDATORS
from  django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt

now = str(datetime.now())
# print(type(now))

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class UserManager(models.Manager):

    def reg_validator(self, form):
        errors = []

        if not form['name']:
            errors.append("Name is required")
        if not form['alias']:
            errors.append("Alias is required")
    # --- Validate EMAIL ---
        if not form['email']:
            errors.append("Email is required")
        elif not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif User.objects.filter(email=form['email']):
             errors.append("Account already exists.")
    # --- Validate PASSWD ---
        if len(form['passwd']) < 5:
            errors.append("Password must have at least 5 characters.")
        if form['passwd'] != form['pass_confirm']:
            errors.append("Passwords do not match")
    # --- Validate BIRTH_DATE
        if not form['birth_date']:
            errors.append("Please add a birth date")
        elif form['birth_date'] > now:
            errors.append("Birthday cannot be in the future")

        if not errors:
            hashed_pass = bcrypt.hashpw(form['passwd'].encode(), bcrypt.gensalt())
            print("*"*100)
            print(hashed_pass)
            print("*"*100)
    # --- BE ADVISED !!! *** I had to add the '.decode("utf-8")' to hashed_pass for my environment for LOGIN bcrypt to work correctly.
            user = User.objects.create(name=form['name'], alias=form['alias'], email=form['email'], passwd=hashed_pass.decode("utf-8"), birth_date=form['birth_date'] )
            return (True, user)
        else:
            return (False, errors)

    def loginValidator(self, form):

        errors = []
    # --- Validate EMAIL ---
        if not form['email']:
            errors.append("Email required.")
        elif not ValidateEmail(form['email']):
            errors.append("Email must have valid format.")
        elif not User.objects.filter(email=form['email']):
             errors.append("Please register first")
    # --- Validate PASSWORD ---
        if len(form['passwd']) < 1:
            errors.append("Password cannot be empty")
        else:
            user = User.objects.filter(email=form['email'])
            if not bcrypt.checkpw(form['passwd'].encode(), user[0].passwd.encode()):
                errors.append("Password does not match password in database.")

        if not errors:
            return (True, user[0])
        else:
            return (False, errors)

class QuoteManager(models.Manager):

    def quote_validator(self, form, user_id):
        errors = []

        # if not form['author']:
        #     errors.append("Quoted By is required")
        if len(form['author']) < 3:
            errors.append("Quoted By must be more than 3 characters")
        # if not form['posted_quote']:
        #     errors.append("Message is required")
        if len(form['posted_quote']) < 10:
            errors.append("Message must be more than 10 characters")

        if not errors:
            this_user_quote = User.objects.get(id=user_id)
            print("*"*25)
            print('THIS USER: ', this_user_quote)
            print("*"*25)

            new_quote = Quote.objects.create(author=form['author'], posted_quote=form['posted_quote'], poster=this_user_quote)

            print("-"*25)
            print('THIS Quote: ', new_quote)
            print("-"*25)

        # --- Adding NEW_QUOTE to USER Join table
            this_user_quote.added_fav.add(new_quote)

            return (True, new_quote)
        else:
            return (False, errors)



# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    birth_date = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<User: {}| {} - {} | {} : {} : {}>".format(self.id, self.name, self.alias, self.email, self.birth_date, self.passwd)

    objects = UserManager()


class Quote(models.Model):
    author = models.CharField(max_length=255)
    posted_quote = models.CharField(max_length=255)

    poster = models.ForeignKey(User, related_name="quoted", on_delete=models.CASCADE)
    users_favs = models.ManyToManyField(User, related_name="added_fav")

    def __repr__(self):
        return "<User: {}| {} - {} | {}>".format(self.id, self.author, self.posted_quote, self.poster)

    objects = QuoteManager()
