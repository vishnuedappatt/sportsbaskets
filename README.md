# sportsbasket
This is a sample application that demonstrates an e-commerce website using the Python Django. The application loads products from a PostgreSQL database and displays them. Users can select to display products in a single category. Users can register and login to website and, click on any product to get more information including pricing, reviews and rating. Users can select items and add them to their shopping cart,and complete their payment using Razor-pay or cod. They can view their order status, can download invoice and add review of product.
In admin side, admins can manage users,products,categories,discount coupons,orders etc...


## Demonstration

Here is the screencast that show the E-commerce demo application in use: 
https://www.linkedin.com/posts/vishnu-p-edappatt_javascript-python-html-activity-6960576991674716160-k1hl?utm_source=share&utm_medium=member_desktop

## Key Features
#### User Modules
* User signUp using OTP (Twilio)
* User authentication with Email or password
* Email verification if forgot Password
* Cart functionality with product variations
* Add products to the cart even without signing-in, prompts a login page whenever the customer tries to checkout
* Discount coupons
* Sort products by price
* Payment using Razorpay,COD
* User can download invoice
#### Admin Modules
* Can analyze monthly orders in a graphical format
* Add featured products, coupons,category etc
* CRUD operations for products
* User management
* Payment details

 APIs integrated -  __Twilio,Razorpay ,googleReCaptch__
## Getting started
To get started you can simply clone this sportsbasket project repository and install the dependencies.

Clone the ecommerce-demo repository using git:
```python
git clone https://github.com/vishnuedappatt/sportsbaskets
 cd sportsbaskets
```
Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:
```python
(env)$ pip install -r requirement.txt
```
Note the ```(env)``` in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once ```pip``` has finished downloading the dependencies:
```python
(env)$ cd ecommerce-django
(env)$ python3 manage.py runserver
```
And navigate to ```http://127.0.0.1:8000/```


## Tech Stack
  Python
  
  Django
  
  PostgreSQL
  
  Bootstrap
  
  Javascript
