import unittest
from poll_fetchers.strawpollservice import StrawpollService
from plotting_services.plotly_service import PlottingService
import os.path


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strawpoll_service = StrawpollService()
        cls.plotting_service = PlottingService()
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

    def test_can_update_plot_from_poll(self):
        # Arrange
        poll_data = self.strawpoll_service.get_data(self.link, "Integration_Test")

        # Act
        self.plotting_service.update_plot(poll_data)
        new_file = os.path.isfile("plots/Integration_Test.png")
        old_file = os.path.isfile("plots/Integration_Test_old.png")

        # Assert
        self.assertTrue(new_file)
        self.assertTrue(old_file)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("plots/Integration_Test.png")
        #os.remove("plots/Integration_Test_old.png")