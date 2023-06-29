import requests
from polldata import PollData
import unittest


class StrawpollService:

    def __init__(self):
        pass

    def get_data(self, link: str, ref_name: str) -> PollData:
        if link.find("api.strawpoll.com") == -1:
            link = link.replace("https://strawpoll.com/", "https://api.strawpoll.com/v3/polls/")

        content_map = requests.get(link).json()
        options: dict[str, int] = {}
        total_votes = 0

        for option in content_map["poll_options"]:
            vote_count = int(option["vote_count"])
            options[option["value"]] = vote_count
            total_votes += vote_count

        return PollData(question=content_map["title"], options=options, total_votes=total_votes,
                        link=link, reference_name=ref_name)


class TestStrawpollService(unittest.TestCase):

    def test_can_retrieve_data(self):
        # Arrange
        link = "https://api.strawpoll.com/v3/polls/PKgl3wqaQnp"
        strawpoll_service = StrawpollService()

        # Act
        poll_test_data = strawpoll_service.get_data(link, "Test")

        # Assert
        self.assertTrue(poll_test_data.options is not None)

    def test_can_format_link(self):
        # Arrange
        link = "https://strawpoll.com/PKgl3wqaQnp"
        strawpoll_service = StrawpollService()
        api_link = "https://api.strawpoll.com/v3/polls/PKgl3wqaQnp"

        # Act
        poll_test_data = strawpoll_service.get_data(link, "Test")

        # Assert
        self.assertEqual(poll_test_data.link, api_link)


if __name__ == "__main__":
    service = StrawpollService()
    poll_data = service.get_data("https://api.strawpoll.com/v3/polls/PKgl3wqaQnp")
    print(poll_data)
