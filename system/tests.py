from datetime import timedelta, datetime

from django.test import TestCase

# Create your tests here.
a=timedelta(days=5)
n=datetime.now()+timedelta(days=5)
n=n.timestamp()

print(n)
print(type(n))