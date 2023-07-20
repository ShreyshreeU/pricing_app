**Pricing App**

Django project for price calculation based on various metrics, full description about the problem statement can be found here -- https://flying-barge-2a8.notion.site/Pricing-Module-v2-8e3addff2b224074a820c63ea29dc012


**Note* All the installation can be done in a virtualenv as follows --**

1. Install virtualenv -- pip install virtualenv
2. Initialize a virtualenv - virtualenv env
3. Activate the env - env\Scripts\activate


**Requirements -- **

1. Install python v3 or greater.
2. Install pip to install and load modules.
3. We use django for this project so install django --
   pip install django


**Create Super User to access the admin UI --**

Be the base directory where manage.py file is present and run following command

<python manage.py createsuperuser>


**Launch the server and add Pricing Config**

1. Launch the server -- <python manage.py runserver>
2. Goto localhost to see the UI -- http://localhost:8000/admin/
3. Login with the superuser credentials

**Following UI will be visible after successfull login**

<img width="1153" alt="Screenshot 2023-07-20 at 11 47 57 AM" src="https://github.com/ShreyshreeU/pricing_app/assets/131691942/da86ec9d-9135-4a4a-9d82-64b94d7411ff">

**Goto Pricing configuration to add/update/activate any config**

Following UI is for adding the config --
<img width="790" alt="Screenshot 2023-07-20 at 11 50 10 AM" src="https://github.com/ShreyshreeU/pricing_app/assets/131691942/a63b36ce-e4f0-468c-b0ed-3219047a6422">


**API for price calculation**

1. URL for the API -- http://localhost:8000/pricing/calculate-price/
2. Type - POST
3. Expects json body with 3 input parameters: "distance", "time" and "waiting_time".

**Sample curl for the API -- **

curl --location 'http://localhost:8000/pricing/calculate-price/' \
--header 'Content-Type: application/json' \
--data '{
    "distance": 3,
    "time": 1,
    "waiting_time": 1
}'


**Postman request and response snippet**
<img width="1287" alt="Screenshot 2023-07-20 at 11 55 28 AM" src="https://github.com/ShreyshreeU/pricing_app/assets/131691942/53419fcd-0681-4606-8339-73cbca1a54a0">

