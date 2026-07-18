import React from "react";
import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";
import { getAllMovies } from "../calls/movieCalls";
import MovieCard from "../components/MovieCard";

function Home() {
  const [movies, setMovies] = useState(null);

  useEffect(() => {
    (async () => {
      const  movie = await getAllMovies();
      setMovies(movie.data);
    })();
  }, []);
  

  return (
    <div>
      <Navbar />

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "20px",
          padding: "20px",
        }}
      >
        {movies &&
          movies.map((movieObj, index) => (
            <MovieCard
              key={index}
              title={movieObj.title}
              posterUrl={movieObj.posterPath}
              language={movieObj.language}
              rating={movieObj.ratings}
              genre={movieObj.genre}
            />
          ))}
      </div>
      </div>
  );
}

export default Home;