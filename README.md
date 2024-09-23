![image](https://github.com/user-attachments/assets/42850aaf-2346-46e4-99f7-5bbb00675b27)

### Set Up Your Environment :
## Install Required Packages: Make sure you have Python installed. Then, install Flask, Flask-GraphQL, and pymongo.
![image](https://github.com/user-attachments/assets/633cbe24-505d-412e-8c46-c75ae8cf82e0)

![image](https://github.com/user-attachments/assets/c0facc04-d516-4993-bbd3-1c32bb43eaaa)

## Set Up MongoDB Atlas:
![image](https://github.com/user-attachments/assets/676c6e0d-b944-4cdc-9b6e-cf12af15770a)
Import your netflix.csv file into the netflixes collection using MongoDB Compass.

![image](https://github.com/user-attachments/assets/9c5851df-91b2-428d-83ba-17280f25e235)
# Data Access has Username and Password
![image](https://github.com/user-attachments/assets/297ad680-4d0d-4e5c-b90f-1a7dc97f57a4)

# Make sure Network Access in MongoDB Atlas has below IP Address
![image](https://github.com/user-attachments/assets/bab5fbe1-cec6-4c10-be98-dd78f4a367df)

## Make Sure MongoDB Compass Connected
![image](https://github.com/user-attachments/assets/0d539bf9-e289-4cdb-81b6-06c4cda8dae4)

## Run the application
![image](https://github.com/user-attachments/assets/9fef45f5-0c53-4cd3-b09d-9038bb5bd1c2)

## Open Apollo Server using Below url
http://127.0.0.1:5017/graphql

## GraphQL Queries:
# 1.Create function: insert the new movies or shows.
mutation {
  createMovie(
    title: "KALKI 2",
    description: "KALKI 2",
    runtime: 50,
    genres: ["Periodic"],
    imdbScore: 9.0,  # If you don't have an IMDb score, you can set this to null or omit it based on your mutation design.
    ageCertification: "TV-MA",
    productionCountries: ["IN"],
    releaseYear: 2026,
    type: "MOVIE"
  ) {
    movie {
      title
      description
      runtime
      imdbScore
      genres
      ageCertification
      productionCountries
      releaseYear
      type
    }
  }
}

# 2.Update function: update the movie and show information using title, and modifies only description, runtime, genres and imdb_score attributes).
mutation {
  updateMovie(title: "Old Money", description: "A family, blessed with richness and power, is desperately seeking for a liver for their father, who wants to hand down his wealth to the one who gets the organ.", runtime: 134, genres: ["Action"], imdbScore: 8.5) {
    movie {
      title
      description
      runtime
      imdbScore
    }
  }
}

# 3.Delete function: delete the movie or show document using title.
mutation {
  deleteMovie(title: "Old Money") {
    success
  }
}

# 4.Read function (I): retrieve all the movie or show documents.
query {
  allMovies {
    title
    description
    runtime
    imdbScore  
    genres
  }
}

# 5.Read function (II): display the detail of the movie or show using title.
query {
  movieByTitle(title: "Taxi Driver") {
    title
    description
    runtime
    imdbScore  
    genres
  }
}

![image](https://github.com/user-attachments/assets/0c1e4811-4701-444d-a933-0cc9ff9c054f)







