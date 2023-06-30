import unittest
import strawpollservice
import os.path


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strawpoll_service = strawpollservice.StrawpollService()
        cls.plotting_service = plottingservice.PlottingService()
        cls.link = "https://strawpoll.com/PKgl3wqaQnp"
        os.chdir("..")

    def test_can_generate_plot_from_poll(self):
        # Arrange
        poll_data = self.strawpoll_service.get_data(self.link, "Integration_Test")

        # Act
        self.plotting_service.create_plot(poll_data)
        my_file = os.path.isfile("plots/Integration_Test.png")
        # Assert
        self.assertTrue(my_file)


    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("plots/Integration_Test.png")