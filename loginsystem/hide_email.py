def hide_email(email):
        var = email.split('@')
        return f'{var[0][0]}*******{var[0][-1]}@{var[1]}'


