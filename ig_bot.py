from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from secrets import pw
import re


class InstagramBot():

    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username
        self.pw = pw
        self.driver.get("https://instagram.com")
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        time.sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        time.sleep(2)

    def followWithUsername(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.driver.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")

    def unfollowWithUsername(self, username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.driver.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.driver.find_element_by_xpath(
                '//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")

    def getUserFollowers(self, username, max):
        file_1 = open("followers.txt", "w")
        self.driver.get('https://www.instagram.com/' + username)
        followersLink = self.driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.driver.find_element_by_css_selector(
            'div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(
            followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(
                followersList.find_elements_by_css_selector('li'))
        followers = []

        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href').split('?')[0].split('/')[3]
            followers.append(userLink)

            if (len(followers) == max):
                break
        for ele in followers:
            file_1.write(ele+"\n")
            if (len(ele) == max):
                break
        file_1.close()
        return followers

    def getUserFollowings(self, username, max):
        file_2 = open("followings.txt", "w")
        self.driver.get('https://www.instagram.com/' + username)
        followingLink = self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        time.sleep(2)
        followingsList = self.driver.find_element_by_css_selector(
            'div[role=\'dialog\'] ul')
        numberOfFollowingsInList = len(
            followingsList.find_elements_by_css_selector('li'))

        followingsList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (numberOfFollowingsInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowingsInList = len(
                followingsList.find_elements_by_css_selector('li'))
        followings = []

        for user in followingsList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href').split('?')[0].split('/')[3]
            followings.append(userLink)

            if (len(followings) == max):
                break
        for ele in followings:
            file_2.write(ele+"\n")
            if (len(ele) == max):
                break
        file_2.close()
        return followings

    def mutualFollowers(self):
        with open('followers.txt', 'r') as file1:
            with open('followings.txt', 'r') as file2:
                same = set(file1).intersection(file2)

        same.discard("\n")

        with open('mutual.txt', 'w') as file_out:
            for line in same:
                file_out.write(line)

    def nonFollowing(self):
        with open('followers.txt', 'r') as file1:
            with open('followings.txt', 'r') as file2:
                diff = set(file1).difference(file2)

        diff.discard("\n")

        with open('non-following.txt', 'w') as file_out:
            for line in diff:
                file_out.write(line)

    def nonFollowers(self):
        with open('followers.txt', 'r') as file1:
            with open('followings.txt', 'r') as file2:
                diff = set(file2).difference(file1)

        diff.discard("\n")

        with open('non-followers.txt', 'w') as file_out:
            for line in diff:
                file_out.write(line)

    def closedriver(self):
        self.driver.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closedriver()


my_bot = InstagramBot("krish7x", pw)
# my_bot.followWithUsername("jlo")
# my_bot.unfollowWithUsername("jlo")
my_bot.getUserFollowers("krish7x", 212)
my_bot.getUserFollowings("krish7x", 393)
my_bot.mutualFollowers()
my_bot.nonFollowing()
my_bot.nonFollowers()
my_bot.closedriver()
