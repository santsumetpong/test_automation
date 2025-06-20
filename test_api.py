import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_get_all_posts():
    logging.info("\nrunning test: GET posts")
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    assert response.status_code == 200, f"expected status code 200, got {response.status_code}"
    logging.info(f"status code {response.status_code} OK")

    data = response.json()
    assert isinstance(data, list)
    logging.info(f"response is a list of length {len(data)}")

    if data:
        first_post = data[0]
        assert "userId" in first_post, "first post missing 'userId' key"
        assert "id" in first_post, "first post missing 'id' key"
        assert "title" in first_post, "first post missing 'title' key"
        assert "body" in first_post, "first post missing 'body' key"
        logging.info("first post contains expected keys")
    logging.info("test 1 passed!")


def test_get_one_post():
    logging.info("\nrunning test: GET one post (ID 1)")
    post_id = 1
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"expected status code 200, got {response.status_code}"
    logging.info(f"status code {response.status_code} OK")

    data = response.json()

    assert data["id"] == post_id, f"expected post id {post_id}, got {data['id']}"
    assert "sunt aut facere repellat provident occaecati excepturi optio reprehenderit" in data["title"], f"unexpected title for post {post_id}"
    logging.info(f"post ID {data['id']} retrieved correctly")
    logging.info("test 2 passed!")


def test_create_new_post():
    logging.info("\nrunning test: POST new post")
    url = "https://jsonplaceholder.typicode.com/posts"
    new_post_data = {
        "title": "my new test post",
        "body": "this is the content of my new test post.",
        "userId": 101
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=new_post_data, headers=headers)

    assert response.status_code == 201, f"expected status code 201, but got {response.status_code}"
    logging.info(f"status code {response.status_code} created")

    response_data = response.json()
    assert response_data["title"] == new_post_data["title"], "created post title mismatch"
    assert response_data["body"] == new_post_data["body"], "created post body mismatch"
    assert "id" in response_data, "new post missing 'id'"
    logging.info(f"new post created with id {response_data['id']}")
    logging.info("test 3 passed!")


def test_put_post():
    logging.info("\nrunning test: PUT post")
    post_id = 2
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    updated_post_data = {
        "id": post_id,
        "title": "updated test post title",
        "body": "this is the updated content for the test post.",
        "userId": 1
    }

    response = requests.put(url, json=updated_post_data)

    assert response.status_code == 200, f"expected status code 200, but got {response.status_code}"
    logging.info(f"status code {response.status_code} updated")

    response_data = response.json()

    assert response_data["id"] == post_id, f"expected post id {post_id}, got {response_data["id"]}"
    logging.info(f"response data id {response_data["id"]} matches post id")

    assert response_data["title"] == updated_post_data["title"], (f"expected post title {updated_post_data["title"]}, "
                                                                  f"got {response_data["title"]}")
    logging.info(f"response title {response_data["title"]} matches post title")

    assert response_data["body"] == updated_post_data["body"], (f"expected post body {updated_post_data["body"]}, "
                                                                f"got {response_data["body"]}")
    logging.info(f"response body {response_data["body"]} matches post body")

    assert response_data["userId"] == updated_post_data["userId"], (f"expected post user id {updated_post_data["userId"]}, "
                                                                    f"got {response_data["userId"]}")
    logging.info(f"response user id {response_data["userId"]} matches post user id")

    logging.info("successfully updated post contents using PUT")
    logging.info("test 4 passed!")


def test_patch_post():
    logging.info("\nrunning test: PATCH post")
    post_id = 3
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    updated_post_data = {
        # "id": post_id,
        "body": "bla bla bla!",
    }

    response = requests.patch(url, json=updated_post_data)

    assert response.status_code == 200, f"expected status code 200, but got {response.status_code}"
    logging.info(f"status code {response.status_code} updated")

    response_data = response.json()

    assert response_data["id"] == post_id, f"expected post id {post_id}, got {response_data["id"]}"
    logging.info(f"response data id {response_data["id"]} matches post id")

    assert response_data["body"] == updated_post_data["body"], (f"expected post body {updated_post_data["body"]}, "
                                                                f"got {response_data["body"]}")
    logging.info(f"response body {response_data["body"]} matches post body")

    og_post_response = requests.get(url)
    og_post_data = og_post_response.json()

    assert response_data["title"] == og_post_data["title"], "PATCH unexpectedly changed title"
    assert response_data["userId"] == og_post_data["userId"], "PATCH unexpectedly changed userId"
    logging.info("other fields (title, userId) remained unchanged as expected.")

    logging.info("successfully updated post contents using PATCH")
    logging.info("test 5 passed!")


def test_delete_post():
    logging.info("\nrunning test: DELETE post")
    post_id = 4
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    response = requests.delete(url)

    assert response.status_code == 200, f"expected status code 200, got {response.status_code}"
    logging.info(f"status code {response.status_code} OK")

    verification = requests.get(url)

    assert verification.status_code == 404, f"expected status code 404, got {verification.status_code}"
    logging.info(f"status code {verification.status_code} OK, which means not found")

    logging.info("successfully removed post contents using DELETE")
    logging.info("test 6 passed!")


"""if __name__ == "__main__":
    try:
        test_get_all_posts()
        test_get_one_post()
        test_create_new_post()
        test_put_post()
        test_patch_post()
        test_delete_post()
        logging.info("\nall api tests passed successfully!")
    except AssertionError as e:
        logging.info(f"\napi test failed: {e}")
    except requests.exceptions.RequestException as e:
        logging.info(f"\nnetwork/request error: {e}")
    except Exception as e:
        logging.info(f"\nunexpected error: {e}")"""