# Bouncer
## Toolkit for automated signup and email management for Peralta Student Clubs

The Bouncer toolkit allows for automated member signup for Peralta clubs. All you need is a Google Account a Google Forms sign-up form, AWS account, and some knowledge of DynamoDB.

Future iterations will focus on making the process workable end-to-end for any club without the need for technical expertise.

### Intended Usage

1. The first step is to create a sign up form. One needs to make a response spreadsheet using Google Sheets from the google signup form, which can be done by the owner of the form. Here's a link for how to do this: https://support.google.com/docs/answer/2917686?hl=en

2. Create a dynamoDB table. This will be automated in the future, but for now, you'll need to create a table to store all the users.

3. Create an EC2 instance. Download this repository onto the instance and create a cronjob to run the functions every interval - whatever interval you prefer.

