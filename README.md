# EduQuiz

EduQuiz is a web application that allows teachers to create quizzes and students to take them. It is built using the Django framework and is currently in development.

## Installation
You can install EduQuiz by cloning this repository and running the following commands:

* you must have python3 and pip installed on your machine:

    * [Python3](https://www.python.org/downloads/)
    * [Pip](https://pip.pypa.io/en/stable/installing/)

*   Run the following commands in your terminal to clone the repository and install the dependencies:
    ``` bash
    git clone <url>
    cd eduquiz
    ```

*   Create a virtual environment and install the dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```

## Usage
To use EduQuiz, you must first create a superuser account. You can do this by running the following command:

    $ python manage.py createsuperuser --username=<username> --email=<email>
    $ python manage.py runserver

You can then log in to the teacher panel at `http://localhost:8000/accounts/create_quiz/` and create a quiz. You can then log in to the student panel at `http://localhost:8000/accounts/take_quiz/` and take the quiz.

## Database Schema

We use a relational database to store the data for EduQuiz. The database schema is as follows:

    * Profile
        * user (OneToOneField, User)
        * bio (TextField)
        * avatar (ImageField)
        * is_teacher (BooleanField)

    * Quiz
        * profile (ForeignKey, Profile)
        * title (CharField)
        * start_at (DateTimeField)
        * end_at (DateTimeField)
        * time_limit (IntegerField)
        * is_available (BooleanField)
        * upload_quiz (FileField, image/csv, image/xlsx)

    * Question
        * quiz (ForeignKey, Quiz)
        * question (TextField)
    
    * Answer
        * question (ForeignKey, Question)
        * answer (TextField)
        * is_correct (BooleanField)

    * StudentAnswer
        * profile (ForeignKey, Profile)
        * quiz (ForeignKey, Quiz)
        * question (ForeignKey, Question)
        * answer (ForeignKey, Answer)


## Apps Structure

EduQuiz is built using the Django framework. It consists of the following apps:

*loginsystem* - This app handles the authentication system.
*Dashboard* - This app handles the teacher dashboard.
    
    
**loginsystem**
EduQuiz uses Django's built-in authentication system. When a user registers, they are assigned a profile. The profile is used to determine whether the user is a teacher or a student. Teachers can create quizzes and students can take them.

**Dashboard**
The dashboard app handles the teacher dashboard. It allows teachers to create quizzes and view the results of their quizzes. also the teacher can edit his profile and delete quiz and all related questions and answers. also the student can edit his profile and reset his password, and there's a button where the student can pass the quiz and see his results.

* I used the `django.contrib.auth` package to handle the authentication system.
* I used the `django-crispy-forms` package to style the forms.


## Technologies
* [Django](https://www.djangoproject.com/)
* [Tailwind CSS](https://tailwindcss.com/)
* [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)

## Roadmap
* Add a feature to allow teachers to upload a CSV or Excel file containing the quiz questions and answers. **(Done)**
* Add a feature when students finish taking a quiz to show them their results and send there results to the teacher.(in progress)
* Add a feature to allow teachers to view the results of their quizzes.
* Delete the quiz and all its questions and answers when the teacher deletes it.**(Done)**
* Add a feature to allow teachers to edit their quizzes. **(in progress)**
* password reset for teachers and students. (Done)




## production
* the project is deployed on server using ubuntu 20.04 and nginx and gunicorn.
* the project is deployed on [EduQuiz](https://eduquiz.yassineamjad.me/)


## License
[MIT](https://choosealicense.com/licenses/mit/)




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
* [Yassine Amjad](https://yassineamjad.me/)


## Project status
This project is currently in development. Users can currently create quizzes and take them. The teacher can edit his profile and delete quiz and all related questions and answers. also the student can edit his profile and reset his password, and there's a button where the student can pass the quiz and see his results.

## Contact
You can contact me at email:
[email@yassineamjad.me](emailto:email@yassineamjad.me)