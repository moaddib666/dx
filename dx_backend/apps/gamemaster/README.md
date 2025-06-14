# Game Master API

This application provides an API for game masters to perform actions that are currently only available through the admin panel or via "hacking". The API follows the pattern `api/v1/gamemaster/...`.

## Endpoints

### Character Management

- `api/v1/gamemaster/characters/` - List and create characters
- `api/v1/gamemaster/characters/{id}/` - Retrieve, update, and delete a character
- `api/v1/gamemaster/characters/{id}/character_info/` - Get detailed information about a character
- `api/v1/gamemaster/characters/{id}/character_stats/` - Get character stats

### World Management

- `api/v1/gamemaster/dimensions/` - List and create dimensions
- `api/v1/gamemaster/planets/` - List and create planets
- `api/v1/gamemaster/continents/` - List and create continents
- `api/v1/gamemaster/countries/` - List and create countries
- `api/v1/gamemaster/cities/` - List and create cities
- `api/v1/gamemaster/areas/` - List and create areas
- `api/v1/gamemaster/locations/` - List and create locations
- `api/v1/gamemaster/positions/` - List and create positions
- `api/v1/gamemaster/maps/` - List and create maps

### Items Management

- `api/v1/gamemaster/items/` - List and create items
- `api/v1/gamemaster/items/{id}/` - Retrieve, update, and delete an item
- `api/v1/gamemaster/world-items/` - List and create world items
- `api/v1/gamemaster/world-items/{id}/` - Retrieve, update, and delete a world item
- `api/v1/gamemaster/character-items/` - List and create character items
- `api/v1/gamemaster/character-items/{id}/` - Retrieve, update, and delete a character item

### Skills Management

- `api/v1/gamemaster/learned-skills/` - List and create learned skills
- `api/v1/gamemaster/learned-skills/{id}/` - Retrieve, update, and delete a learned skill
- `api/v1/gamemaster/learned-schools/` - List and create learned schools
- `api/v1/gamemaster/learned-schools/{id}/` - Retrieve, update, and delete a learned school

### Effects Management

- `api/v1/gamemaster/effects/` - List and create effects
- `api/v1/gamemaster/effects/{id}/` - Retrieve, update, and delete an effect
- `api/v1/gamemaster/active-effects/` - List and create active effects
- `api/v1/gamemaster/active-effects/{id}/` - Retrieve, update, and delete an active effect

### School Management

- `api/v1/gamemaster/schools/` - List and create schools
- `api/v1/gamemaster/schools/{id}/` - Retrieve, update, and delete a school
- `api/v1/gamemaster/skills/` - List and create skills
- `api/v1/gamemaster/skills/{id}/` - Retrieve, update, and delete a skill
- `api/v1/gamemaster/paths/` - List and create paths
- `api/v1/gamemaster/paths/{id}/` - Retrieve, update, and delete a path
- `api/v1/gamemaster/paths/{id}/with_schools/` - Get a path with its schools

### Currency Management

- `api/v1/gamemaster/currency-tokens/` - List and create currency tokens
- `api/v1/gamemaster/currency-tokens/{id}/` - Retrieve, update, and delete a currency token
- `api/v1/gamemaster/character-currencies/` - List and create character currencies
- `api/v1/gamemaster/character-currencies/{id}/` - Retrieve, update, and delete a character currency

## Authentication

All endpoints require admin user authentication. You can authenticate using JWT tokens:

```
POST /auth/jwt/token/
{
    "username": "admin",
    "password": "password"
}
```

Then include the token in the Authorization header:

```
Authorization: Bearer <token>
```

## Permissions

All endpoints require admin user permissions. Only users with `is_staff=True` can access these endpoints.
