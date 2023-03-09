def userEntity(user) -> dict:
    return {
        'id': user.id,
        'email': user.email,
        'bookmarks': user.bookmarks,
    }
