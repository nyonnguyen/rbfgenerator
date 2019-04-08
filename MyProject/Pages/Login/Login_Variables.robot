*** Variables ***
# Locators
${USERNAME_FIELD}         id=email
${PASSWORD_FIELD}         id=passwd
${LOGIN_BUTTON}           id=SubmitLogin
${MAIN_HEADER}            id=header

# String
${USERNAME_IS_REQUIRED_MESSAGE}      An email address required.
${USERNAME_IS_INVALID_MESSAGE}       Invalid email address.
${PASSWORD_IS_REQUIRED_MESSAGE}      Password is required.
${AUTHEN_FAILED_MESSAGE}             Authentication failed.

${LOGIN_URL}   ${WEB_URL}/index.php?controller=authentication&back=my-account
