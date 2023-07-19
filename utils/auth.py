from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user, meta_data=None):
    # Generate JWT tokens for the given user
    refresh = RefreshToken.for_user(user)
    # Create a dictionary to store the tokens and user information
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'email': user.email,
    }

    # Add additional metadata to the token if provided
    if meta_data:
        token.update(meta_data)

    # Return the token dictionary
    return token
