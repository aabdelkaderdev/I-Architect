<!-- Source: https://docs.streamlit.io/knowledge-base/deploy/share-apps-with-viewers-outside-organization -->

Now that your app is deployed you can easily share it and collaborate on it. But first, let's take a moment and do a little joy dance for getting that app deployed! 🕺💃

Your app is now live at a fixed URL, so go wild and share it with whomever you want. Your app will inherit permissions from your GitHub repo, meaning that if your repo is private your app will be private and if your repo is public your app will be public. If you want to change that you can simply do so from the app settings menu.

You are only allowed one private app at a time. If you've deployed from a private repository, you will have to make that app public or delete it before you can deploy another app from a private repository. Only developers can change your app between public and private.

- [Make your app public or private](/deploy/streamlit-community-cloud/share-your-app#make-your-app-public-or-private)
- [Share your public app](/deploy/streamlit-community-cloud/share-your-app#share-your-public-app)
- [Share your private app](/deploy/streamlit-community-cloud/share-your-app#share-your-private-app)

If you deployed your app from a public repository, your app will be public by default. If you deployed your app from a private repository, you will need to make the app public if you want to freely share it with the community at large.

1. Access your [App settings](/deploy/streamlit-community-cloud/manage-your-app/app-settings) and go to the "**Sharing**" section.
2. Set your app's privacy under "Who can view this app." Select "**This app is public and searchable**" to make your app public. Select "**Only specific people can view this app**" to make your app private.

1. From your app at `<your-custom-subdomain>.streamlit.app`, click "**Share**" in the upper-right corner.
2. Toggle your app between public and private by clicking "**Make this app public**."

Once your app is public, just give anyone your app's URL and they view it! Streamlit Community Cloud has several convenient shortcuts for sharing your app.

1. From your app at `<your-custom-subdomain>.streamlit.app`, click "**Share**" in the upper-right corner.
2. Click "**Social**" to access convenient social media share buttons.

Use the social media sharing buttons to post your app on our forum! We'd love to see what you make and perhaps feature your app as our app of the month. 💖

Whether your app is public or private, you can send an email invite to your app directly from Streamlit Community Cloud. This grants the viewer access to analytics for all your public apps and the ability to invite other viewers to your workspace. Developers and invited viewers are identified by their email in analytics instead of appearing anonymously (if they view any of your apps while signed in). Read more about viewers in [App analytics](/deploy/streamlit-community-cloud/manage-your-app/app-analytics).

1. From your app at `<your-custom-subdomain>.streamlit.app`, click "**Share**" in the upper-right corner.
2. Enter an email address and click "**Invite**."
3. Invited users will get a direct link to your app in their inbox.

From your app click "**Share**" in the upper-right corner then click "**Copy link**."

To help others find and play with your Streamlit app, you can add Streamlit's GitHub badge to your repo. Below is an enlarged example of what the badge looks like. Clicking on the badge takes you to—in this case—Streamlit's Roadmap.

Once you deploy your app, you can embed this badge right into your GitHub README.md by adding the following Markdown:

```
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://<your-custom-subdomain>.streamlit.app)
```

Be sure to replace `https://<your-custom-subdomain>.streamlit.app` with the URL of your deployed app!

By default an app deployed from a private repository will be private to the developers in the workspace. A private app will not be visible to anyone else unless you grant them explicit permission. You can grant permission by adding them as a developer on GitHub or by adding them as a viewer on Streamlit Community Cloud.

Once you have added someone's email address to your app's viewer list, that person will be able to sign in and view your private app. If their email is associated with a Google account, they will be able to sign in with Google OAuth. Otherwise, they will be able to sign in with single-use, emailed links. Streamlit sends an email invitation with a link to your app every time you invite someone.

When you add a viewer to any app in your workspace, they are granted access to analytics for that app as well as analytics for all your public apps. They can also pass these permissions to others by inviting more viewers. All viewers and developers in your workspace are identified by their email in analytics. Furthermore, their emails show in analytics for every app in your workspace and not just apps they are explicitly invited to. Read more about viewers in [App analytics](/deploy/streamlit-community-cloud/manage-your-app/app-analytics)

1. From your app at `<your-custom-subdomain>.streamlit.app`, click "**Share**" in the upper-right corner.
2. Enter the email to send an invitation to and click "**Invite**."
3. Invited users appear in the list below.
4. Invited users will get a direct link to your app in their inbox.

- To remove a viewer, simply access the share menu as above and click the *close* next to their name.

1. Access your [App settings](/deploy/streamlit-community-cloud/manage-your-app/app-settings) and go to the "**Sharing**" section.
2. Add or remove users from the list of viewers. Click "**Save**."

[*arrow\_back*Previous: Manage your app](/deploy/streamlit-community-cloud/manage-your-app)[*arrow\_forward*Next: Embed your app](/deploy/streamlit-community-cloud/share-your-app/embed-your-app)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI