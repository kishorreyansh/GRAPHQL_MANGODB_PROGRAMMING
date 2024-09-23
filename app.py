from flask import Flask
from flask_graphql import GraphQLView
from graphql import GraphQLError
from pymongo import MongoClient
import graphene

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
# Database Name
db = client["Netflix"]
# Collection Name
collection = db["netflixes"]

# GraphQL Schema
class Movie(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    description = graphene.String()
    genres = graphene.List(graphene.String)
    imdb_score = graphene.Float()
    runtime = graphene.Int()
    release_year = graphene.Int()
    age_certification = graphene.String()
    production_countries = graphene.List(graphene.String)
    type = graphene.String()

# 4. Read function (I): retrieve all the movie or show documents.
# 5. Read function (II): display the detail of the movie or show using title.

class Query(graphene.ObjectType):
    all_movies = graphene.List(Movie)
    movie_by_title = graphene.Field(Movie, title=graphene.String())

    def resolve_all_movies(self, info):
        return list(collection.find())

    def resolve_movie_by_title(self, info, title):
        movie = collection.find_one({"title": title})
        if not movie:
            raise GraphQLError("Movie not found")
        return movie

# 1.Create function: insert the new movies or shows.
class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        runtime = graphene.Int(required=True)
        genres = graphene.List(graphene.String, required=True)
        imdbScore = graphene.Float(required=False)  # Make this optional if it can be null
        age_certification = graphene.String(required=True)
        production_countries = graphene.List(graphene.String, required=True)
        release_year = graphene.Int(required=True)
        type = graphene.String(required=True)

    movie = graphene.Field(Movie)

    def mutate(self, info, title, description, runtime, genres, imdbScore, age_certification, production_countries, release_year, type):
        new_movie = {
            "title": title,
            "description": description,
            "runtime": runtime,
            "genres": genres,
            "imdb_score": imdbScore,  # Handle null or omit if not provided
            "age_certification": age_certification,
            "production_countries": production_countries,
            "release_year": release_year,
            "type": type
        }
        # Insert the new movie into the MongoDB collection
        collection.insert_one(new_movie)
        # Return the created movie
        return CreateMovie(movie=Movie(
            title=new_movie['title'],
            description=new_movie['description'],
            runtime=new_movie['runtime'],
            imdb_score=new_movie.get('imdb_score'),  
            genres=new_movie['genres'],
            age_certification=new_movie['age_certification'],
            production_countries=new_movie['production_countries'],
            release_year=new_movie['release_year'],
            type=new_movie['type']
        ))

# 2.Update function: update the movie and show information using title, and modifies only description, runtime, genres and imdb_score attributes).
class UpdateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()  # Optional
        runtime = graphene.Int()          # Optional
        genres = graphene.List(graphene.String)  # Optional
        imdbScore = graphene.Float()      # Optional

    movie = graphene.Field(Movie)

    def mutate(self, info, title, description=None, runtime=None, genres=None, imdbScore=None):
        # Create a dictionary to hold the update data
        update_data = {}

        if description is not None:
            update_data["description"] = description
        if runtime is not None:
            update_data["runtime"] = runtime
        if genres is not None:
            update_data["genres"] = genres
        if imdbScore is not None:
            update_data["imdb_score"] = imdbScore  # Ensure this matches your DB field

        # Perform the update in the database
        result = collection.update_one({"title": title}, {"$set": update_data})

        # Check if the update was successful
        if result.matched_count == 0:
            raise GraphQLError("Movie not found")

        # Retrieve the updated movie information
        updated_movie = collection.find_one({"title": title})

        return UpdateMovie(movie=Movie(
            title=updated_movie['title'],
            description=updated_movie['description'],
            runtime=updated_movie['runtime'],
            imdb_score=updated_movie['imdb_score']  
        ))


# 3.Delete function: delete the movie or show document using title.
class DeleteMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, title):
        result = collection.delete_one({"title": title})
        return DeleteMovie(success=result.deleted_count > 0)

class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(port=5017,debug=True)
