import pytest, logging, unittest
from werkzeug.security import generate_password_hash
from flask import jsonify
from datetime import date, datetime

#from App.main import create_app
from App.database import create_db
from App.models import User, Image, Rating, Ranking
from App.controllers.auth import authenticate

from App.controllers.distributor import(
    create_distributor,
    get_distributor,
    get_distributor_json,
    delete_distributor,
    )

from App.controllers.feed import (
    create_feed,
    get_feed,
    get_feeds_by_receiver,
    get_feeds_by_sender,
    get_feed_json,
    view_feed,
    delete_feed,
)

from App.controllers.user import (
    create_user,
    get_user,
    getUserbyUsername,
    get_all_users,
    get_all_users_json,
    update_user,
    delete_user,
    )

from App.controllers.image import (   
    create_image,
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,
    )

from App.controllers.rating import (   
    create_rating,
    get_rating,
    get_rating_json,
    get_ratings_by_ratee,
    get_ratings_by_rater,
    update_rating,
    delete_rating,
    )

from App.controllers.ranking import (
    create_ranking, 
    get_ranking,
    get_rankings_by_ranker,
    get_rankings_by_image,
    update_ranking,
    delete_ranking,

    ) 

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_create_user(self):
        user = User("bob", "bobpass")
        self.assertEqual (user.username) == "bob"

    def test_toJSON(self):
        user = User("bob1", "bobpass")
        self.assertDictEqual( user.to_json(), {"id": None, "username": "bob1", "images": []})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class ImageUnitTests(unittest.TestCase):

    def test_new_image(self):
        user = User("rob", "robpass")
        image = Image(user.id, "https://via.placeholder.com/150x200")
        assert image.userId == user.id

    def test_to_json(self):
        user = User("rob1", "robpass")
        image = Image(user.id, "https://via.placeholder.com/150x200")
        self.assertDictEqual(
            image.toJSON(),
            {
                "id": image.id,
                "userId": user.id,
                "rank": 0,
                "num_rankings": 0,
                "url": "https://via.placeholder.com/150x200",
            },
        )

    def test_get_average_rank(self):
        image = Image(1, "https://via.placeholder.com/150x200")
        assert image.getAverageRank() == 0
    
class RatingUnitTests(unittest.TestCase):

    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.score == 3

    def test_toJSON(self):
        rating = Rating(1, 2, 3)
        rating_json = rating.toJSON()
        self.assertDictEqual(rating_json, {"id":None, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()})

class RankingUnitTests(unittest.TestCase):

    def test_new_ranking(self):
        ranking = Ranking(1, 2, 3)
        assert ranking.score == 3

    def test_toJSON(self):
        ranking = Ranking(1, 2, 3)
        ranking_json = ranking.toJSON()
        self.assertDictEqual(ranking_json, {"id":None, "creatorId":1, "imageId": 2, "score":3})


class FeedUnitTests(unittest.TestCase):
    def test_new_feed(self):
        feed = Feed(1, 2, 3)
        assert feed.distributorId == 3

    def test_to_json(self):
        feed = Feed(1, 2, 3)
        self.assertDictEqual(
            feed.to_json(),
            {
                "id": feed.id,
                "senderId": 1,
                "receiverId": 2,
                "distributorId": 3,
                "seen": False,
            },
        )

    def test_setSeen(self):
        feed = Feed(1, 2, 3)
        feed.setSeen()
        assert feed.seen is True


class DistributorUnitTests(unittest.TestCase):
    def test_new_distributor(self):
        distributor = Distributor(5)
        assert distributor.numOfProfiles == 5

    def test_to_json(self):
        distributor = Distributor(5)
        self.assertDictEqual(
            distributor.to_json(),
            {
                "id": distributor.id,
                "numOfProfiles": 5,
                "timestamp": distributor.timestamp,
            },
        )


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
 
def test_authenticate():
        user = create_user("bob", "bobpass")
        assert authenticate("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_user(self):
        user = get_user(1)
        assert user.username == "bob"

    def test_get_user_by_username(self):
        user = get_user_by_username("rick")
        assert user["username"] == "rick"

    def test_get_all_users(self):
        userList = []
        userList.append(get_user(1))
        userList.append(get_user(2))
        self.assertEqual(get_all_users(), userList)

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", "images": [], "ratings": []}, {"id":2, "username":"rick", "images": [], "ratings": []}], users_json)

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_delete_user(self):
        create_user("phil", "philpass")
        delete_user(3)
        user = get_user(3)
        assert user == None

class ImageIntegrationTests(unittest.TestCase):

    def test_create_image(self):
        user = create_user("tom1", "tompass")
        image = createImage(user.getId(), "https://via.placeholder.com/150x200")
        assert image.getUserId() == user.getId()()

    def test_get_image(self):
        user = create_user("tom2", "tompass")
        image = createImage(user.getId(), "https://via.placeholder.com/150x200")
        image2 = get_image(image.getId())
        assert image2.getURL() == image.getURL()


    def test_get_image_json(self):
        user = create_user("tom3", "tompass")
        image = createImage(user.getId()(), "https://via.placeholder.com/150x200")
        self.assertDictEqual(
            get_image_json(image.getId()),
            {
                "id": image.getId(),
                "user_id": user.getId(),
                "rank": 0,
                "num_rankings": 0,
                "url": "https://via.placeholder.com/150x200",
            },
        )    

    def test_get_all_images(self):
        image = createImage(1)
        imageList = []
        imageList.append(getImage(1))
        imageList.append(getImage(2))
        self.assertListEqual(getAllImages(), imageList)

    def test_get_all_images_json(self):
        images_json = getAllImages_JSON()
        self.assertListEqual([{"id":1, "rankings":[], "userId": 2}, {"id":2, "rankings":[], "userId": 1}], images_json)

    def test_getAverageImageRank(self):
        user = create_user("tom5", "tompass")
        user2 = create_user("tom6", "tompass")
        image = createImage(user.get_id(), "https://via.placeholder.com/150x200")
        create_ranking(user2.getId(), image.getId(), 1)
        create_ranking(user2.getId(), image.getId(), 3)
        average_rank = test_getAverageImageRank(image.get_id())
        assert average_rank == 2

    def test_getImagesByUser(self):
        user = create_user("tom4", "tompass")
        create_image(user.getId(), "https://via.placeholder.com/150x200")
        create_image(user.getId(), "https://via.placeholder.com/150x200")
        images = getImagesByUser(user.get_id())
        assert len(images) == 2

    def test_deleteImage(self):
        image = create_image(1)
        deleteImage(image.id)
        image = getImage(image.id)
        assert image == None

    
class RatingIntegrationTests(unittest.TestCase):

    def test_create_rating(self):
        rating = create_rating(1, 2, 3)
        assert rating.id == 1

    def test_get_rating(self):
        rating = get_rating(1)
        assert rating.creatorId == 1

    def test_get_all_ratings(self):
        rating = create_rating(2, 1, 4)
        ratingList = []
        ratingList.append(get_rating(1))
        ratingList.append(get_rating(2))
        self.assertListEqual(get_all_ratings(), ratingList)

    def test_get_all_ratings_json(self):
        ratings_json = get_all_ratings_json()
        self.assertListEqual([{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}, {"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}], ratings_json)

    def test_get_ratings_by_creatorid(self):
        ratings = get_ratings_by_creator(2)
        self.assertListEqual(ratings, [{"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}])

    def test_get_ratings_by_targetid(self):
        ratings = get_ratings_by_target(2)
        self.assertListEqual(ratings, [{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}])

    def test_get_rating_by_actors(self):
        rating = get_rating_by_actors(1, 2)
        assert rating.id == 1

    def test_update_rating(self):
        rating = update_rating(1, 5)
        assert rating.score == 5

    def test_try_calculate_rating(self):
        user = create_user("phil", "philpass")
        rating = create_rating(user.id, 2, 5)
        calculated = get_calculated_rating(2)
        assert calculated == 4

    def test_get_level(self):
        assert get_level(1) == 1


class RankingIntegrationTests(unittest.TestCase):

    def test_create_rating(self):
        ranking = create_ranking(1, 2, 3)
        assert ranking.id == 1

    def test_get_ranking(self):
        ranking = get_ranking(1)
        assert ranking.creatorId == 1

    def test_get_all_rankings(self):
        ranking = create_ranking(2, 1, 4)
        rankingList = []
        rankingList.append(get_ranking(1))
        rankingList.append(get_ranking(2))
        self.assertListEqual(get_all_rankings(), rankingList)

    def test_get_all_rankings_json(self):
        rankings_json = get_all_rankings_json()
        self.assertListEqual([{"id":1, "creatorId":1, "imageId": 2, "score":3}, {"id":2, "creatorId":2, "imageId": 1, "score":4}], rankings_json)

    def test_get_rankings_by_creatorid(self):
        rankings = get_rankings_by_creator(2)
        self.assertListEqual(rankings, [{"id":2, "creatorId":2, "imageId": 1, "score":4}])

    def test_get_rankings_by_imageid(self):
        rankings = get_rankings_by_image(2)
        self.assertListEqual(rankings, [{"id":1, "creatorId":1, "imageId": 2, "score":3}])

    def test_get_ranking_by_actors(self):
        ranking = get_ranking_by_actors(1, 2)
        assert ranking.id == 1

    def test_update_ranking(self):
        ranking = update_ranking(1, 5)
        assert ranking.score == 5

    def test_try_calculate_ranking(self):
        ranking = create_ranking(3, 2, 5)
        calculated = get_calculated_ranking(2)
        assert calculated == 4