"""
TestCustomerModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db
from service.common import status  # HTTP Status Codes

import json
from tests.factories import CustomerFactory


from service.models import Customer

BASE_URL = "/customers"

from flask import jsonify

######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomerServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        
    def _create_customers(self, count):
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_customer(self):
        """It should Delete a Customer"""
        test_customer = self._create_customers(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_customer.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_customer(self):
        """ Create a new Customer """
        # Arrange

        fake_customer = CustomerFactory()
        data = json.dumps({
            "id": fake_customer.id,
            "first_name": fake_customer.first_name,
            "last_name": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address
        })

        # Action
        response = self.client.post(
            "/customers", 
            data=data,
            content_type="application/json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check the data is correct
        new_json = json.loads(response.data)
        self.assertEqual(new_json["first_name"], fake_customer.first_name)
        self.assertEqual(new_json["last_name"], fake_customer.last_name)
        self.assertEqual(new_json["email"], fake_customer.email)
        self.assertEqual(new_json["address"], fake_customer.address)

    def test_create_customer_wrong_field(self):
        """ Create a new Customer with wrong field """
        # Arrange

        fake_customer = CustomerFactory()
        data = json.dumps({
            "id": fake_customer.id,
            "firstName": fake_customer.first_name,
            "lastName": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address
        })

        # Action
        response = self.client.post(
            "/customers", 
            data=data,
            content_type="application/json"
        )
        
        # Check the data is correct
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_customer_no_json(self):
        """ Create a new Customer with no JSON data """
        # Arrange
        fake_customer = CustomerFactory()

        # Convert the data to a string instead of JSON
        data = json.dumps({
        })

        # Action
        response = self.client.post(
            "/customers", 
            data=data,
            content_type="application/json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_customer_not_json(self):
        """ Create a new Customer with non-JSON data """
        # Arrange
        fake_customer = CustomerFactory()

        # Convert the data to a string instead of JSON
        data = str({
            "id": fake_customer.id,
            "first_name": fake_customer.first_name,
            "last_name": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address
        })

        # Action
        response = self.client.post(
            "/customers", 
            data=data,
            content_type="text/plain"  # Send as plain text instead of JSON
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        

    def test_create_customer_no_type(self):
        """ Create a new Customer with no content_type"""
        # Arrange
        fake_customer = CustomerFactory()

        # Convert the data to a string instead of JSON
        data = str({
            "id": fake_customer.id,
            "first_name": fake_customer.first_name,
            "last_name": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address
        })

        # Action
        response = self.client.post(
            "/customers", 
            data=data,
            # Send as no type instead of JSON
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)  # Expect a 400 error

    def test_create_customer_missing_field(self):
        """ Create a new Customer with missing fields """
        # Arrange
        fake_customer = CustomerFactory()
        data_dict = {
            "id": fake_customer.id,
            "first_name": fake_customer.first_name,
            "last_name": fake_customer.last_name,
            "email": fake_customer.email,
            "address": fake_customer.address
        }

        required_fields = ["first_name", "last_name", "email", "address"]

        for key in required_fields:
            bad_data = data_dict.copy()
                

            # Remove a required field
            del bad_data[key]

            # Action
            response = self.client.post(
                "/customers", 
                data=json.dumps(bad_data),
                content_type="application/json"
            )

            # Assert
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Expect a 400 error

            # Check the error message
            error_json = json.loads(response.data)
            self.assertEqual(error_json["error"], "Invalid Customer: missing " + key)

    def test_get_customer(self):
        # """It should Read a Customer"""
        # customer = CustomerFactory()
        # logging.debug(customer)
        # customer.id = None
        # customer.create()
        # self.assertIsNotNone(customer.id)
        # # Fetch it back
        # found_customer = Customer.find(customer.id)
        # self.assertEqual(found_customer.id, customer.id)
        # self.assertEqual(found_customer.first_name, customer.first_name)
        # self.assertEqual(found_customer.last_name, customer.last_name)
        # self.assertEqual(found_customer.email, customer.email)
        # self.assertEqual(found_customer.address, customer.address)
        
        
        # Create a test resource using the factory
        customer = CustomerFactory()
        
        response = self.client.get(
            "/customers/" + str(customer.id), 
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
        customer.create()

        # Send a GET request to retrieve the resource
        response = self.client.get(
            "/customers/" + str(customer.id), 
        )
        
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        customer = Customer.find(customer.id)
        found_customer = response.get_json()

        # Check if the returned JSON data matches the resource data
        self.assertEqual(found_customer, customer.serialize())