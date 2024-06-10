import os, subprocess, logging, json, requests
logging.basicConfig(level=logging.INFO)

from datetime import date, datetime

from apscheduler.schedulers.blocking import BlockingScheduler
logging.getLogger('apscheduler.executors.default').propagate = False

# directory structure setup 
prodPath = 'sync-origin'
buPath = 'sync-dest'
dirs2sync = ['files', 'media']

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

# read the webhook for posting slack messages

#webhook_url = "https://hooks.slack.com/services/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"


def sync_that_stuff():
    
    ''' recurrent syncronisattion of the data '''

    now = datetime.now()
    today = date.today()

    stderrMessage = '' # placeholder for the errors, if any

    dbSync = subprocess.run(
            ['rsync', os.path.join(prodPath, 'data/db/db.sqlite3'), os.path.join(buPath, f'db.{str(today)}.sqlite3')],
        capture_output=True)
    if not dbSync.returncode == 0:
        stderrMessage += dbSync.stderr.decode('utf-8')

    for dirName in dirs2sync:
        dirSync = subprocess.run(
            ['rsync', '-r', os.path.join(prodPath, dirName), os.path.join(buPath)],
            capture_output=True)
        if not dirSync.returncode == 0:
            stderrMessage += dirSync.stderr.decode('utf-8')

    logging.info(f' {now}: 🤖 sync complete \n{stderrMessage}')

    # generate slack message depending on errors or not
   # if not stderrMessage == '':
   #     slack_data = {'text': "🎭 actor-backup: :warning: something's wrong, see below: \n```{}```".format(stderrMessage)}
   # else:
   #     slack_data = {'text': "🎭 actor-backup: :beach_with_umbrella: data backed up"}

    # post a slack message
   # response = requests.post(
   #     webhook_url, data=json.dumps(slack_data),
   #     headers={'Content-Type': 'application/json'}
   # )

    # make sure there's no problems with sending the notification
   # if response.status_code != 200:
   #     raise ValueError(
   #         'Request to slack returned an error %s, the response is:\n%s'
   #         % (response.status_code, response.text)
   #     )

if __name__ == "__main__":

    scheduler = BlockingScheduler(timezone="Europe/Berlin")
    scheduler.add_job(sync_that_stuff, 'cron', day_of_week='mon-sun', hour=7, minute=00)
    scheduler.start()
