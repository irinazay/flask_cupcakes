from unittest import TestCase

from app import app
from models import db, Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_1 = {
    "flavor": "Test-Flavor-1",
    "size": "Test-Size-1",
    "rating": 10,
    "image": "https://cdn.sallysbakingaddiction.com/wp-content/uploads/2014/10/Red-Velvet-Cupcakes-6.jpg"
}
CUPCAKE_2 = {
    "flavor": "Test-Flavor-2",
    "size": "Test-Size-2",
    "rating": 9,
    "image": "https://choosingchia.com/jessh-jessh/uploads/2020/03/Vegan-carrot-cake-cupcakes3-1-of-1.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests views functions"""

    def setUp(self):
        """Make initial cupcakes."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_1)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "Test-Flavor-1",
                        "size": "Test-Size-1",
                        "rating": 10,
                        "image": "https://cdn.sallysbakingaddiction.com/wp-content/uploads/2014/10/Red-Velvet-Cupcakes-6.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "Test-Flavor-1",
                    "size": "Test-Size-1",
                    "rating": 10,
                    "image": "https://cdn.sallysbakingaddiction.com/wp-content/uploads/2014/10/Red-Velvet-Cupcakes-6.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_2)

            self.assertEqual(resp.status_code, 201)
            self.assertIsInstance(resp.json['cupcake']['id'], int)
            del resp.json['cupcake']['id']

            self.assertEqual(resp.json, {
                "cupcake": {
                    "flavor": "Test-Flavor-2",
                    "size": "Test-Size-2",
                    "rating": 9,
                    "image": "https://choosingchia.com/jessh-jessh/uploads/2020/03/Vegan-carrot-cake-cupcakes3-1-of-1.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=CUPCAKE_2)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "Test-Flavor-2",
                    "size": "Test-Size-2",
                    "rating": 9,
                    "image": "https://choosingchia.com/jessh-jessh/uploads/2020/03/Vegan-carrot-cake-cupcakes3-1-of-1.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)

    def test_update_cupcake_missing(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/17"
            resp = client.patch(url, json=CUPCAKE_2)

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {"message": "Deleted"})
            self.assertEqual(Cupcake.query.count(), 0)

    def test_delete_cupcake_missing(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/22"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)
