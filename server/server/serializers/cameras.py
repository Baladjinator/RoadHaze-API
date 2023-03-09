def userEntity(camera) -> dict:
    return {
        'id': camera.id,
        'name': camera.name,
        'lat': camera.lat,
        'lon': camera.lon,
        'active': camera.active,
        'url': camera.url
    }
