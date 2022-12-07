import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate
from App.main import create_app
from App.controllers import ( 

    create_user, 
    get_all_users_json, 
    get_all_users,
    getUserbyUsername, 
    createImage,
    distribute_all,
    distribute, 
    get_all_distributors, 
    get_distributor_json,
    get_receiver_feeds,
    get_feed
     )

# This commands file allow you to create convenient CLI commands for testing controllers


app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Generic Commands
'''

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
    

app.cli.add_command(test)

@app.cli.command("create-user")
@click.argument("number", default="1")
def create_user_command(number):
    user = getUserbyUsername(f"bob{number}")
    if not user:
        create_user(f"bob{number}", "bobpass")
        print(f"bob{number} created!")
    else:
        print(f"bob{number} already exists")


@app.cli.command("create-users")
@click.argument("number", default=4)
def create_users_command(number):
    for i in range(1, number + 1):
        user = getUserbyUsername(f"rob{i}")
        if not user:
            create_user(f"rob{i}", f"rob{i}pass")
            print(f"rob{i} created!")
        else:
            print(f"rob{i} already exists")

@app.cli.command("add-images")
def add_images_command():
    users = get_all_users()
    for user in users:
        createImage(user.id, "https://via.placeholder.com/150x200")
        createImage(user.id, "https://via.placeholder.com/150x203")
        createImage(user.id, "https://via.placeholder.com/150x204")
        createImage(user.id, "https://via.placeholder.com/150x205")
    print("images added")

@app.cli.command("distribute-data")
def distribute_data_command():
    outcome = distribute()
    if outcome:
        print("data distributed...see table below")
        distributors = get_all_distributors()
        print(distributors)
        print("FEED ID  |  RECEIVER  |  SENDER  |  DISTRIBUTOR  |  SEEN")
        for distributor in distributors:
            for feed in distributor.feed:
                print(
                    f"    {feed.id}    |    {feed.receiverId}    |    {feed.senderId}    |    {feed.distributorId}    |   {feed.seen}    "
                )
    else:
        print("distribution not done - profiles at limit")

@app.cli.command("distribute-all")
def distribute_all_command():
    counter = distribute_all()
    if counter:
        print(f"{counter} distributions made")


@app.cli.command("view-profile")
@click.argument("feed-id", default=1)
def view_profile_command(id):
    feed = get_feed(id)
    if feed:
        feed_view(id)
    else:
        print("feed not found")


@app.cli.command("view-all-feeds")
@click.argument("receiver-id", default=1)
def view_all_feeds_command(receiverId):
    feeds = get_receiver_feeds(receiverId)
    if feeds:
        for feed in feeds:
            feed_view(feed.id)
            print("all feeds viewed")
    else:
        print("no feeds found")


@app.cli.command("print-distribution")
def print_distribution_command():
    distributors = get_all_distributors()
    print("FEED ID  |  RECEIVER  |  SENDER  |  DISTRIBUTOR  |  SEEN")
    for distributor in distributors:
        for feed in distributor.feed:
            print(
                f"    {feed.id}    |    {feed.receiverId}    |    {feed.senderId}    |    {feed.distributorId}    |   {feed.seen}    "
            )


@app.cli.command("print-distributors")
def print_distributors():
    distributors = [get_distributor_json(j.id) for j in get_all_distributors()]
    print(distributors)
