import React, { useEffect, useState } from "react";
import { getAllMovies, deleteMovie } from "../../calls/movieCalls";
import { Table, Button, message } from "antd";
import moment from "moment";
import MovieForm from "./MovieForm";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

function MovieList() {
  const [movies, setMovies] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formType, setFormType] = useState("add");
  const [selectedMovie, setSelectedMovie] = useState(null);

  // getting all the Movies
  const getMovies = async () => {
    try {
      const respone = await getAllMovies();
      setMovies(respone.data);
      console.log(respone.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getMovies();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await deleteMovie(id);
      if (response && response.success) {
        message.success(response.message);
        getMovies();
      } else {
        message.error(response?.message || "Failed to delete movie");
      }
    } catch (error) {
      console.log(error);
      message.error("Failed to delete movie");
    }
  };

  const tableHeadings = [
    {
      title: "Poster",
      dataIndex: "poster",
      render: (text, data) => {
        return <img width="100" height="auto" src={data.posterPath} />;
      },
    },

    {
        title:'Title',
        dataIndex : 'title'
     },


     {
        title:'Description',
        dataIndex : 'description'
     },

     {
        title:'Language',
        dataIndex : 'language'
     },

     {
        title:'Genre',
        dataIndex : 'genre'

     },

     {
      title: "Release Date",
      dataIndex: "releaseDate",
      render: (text, data) => {
        return moment(data.releaseDate).format("DD-MM-YYYY");
         }
     },

     {
        title: "Duration",
        dataIndex: "duration",
        render: (text) => {
          return `${text} min`;
        }
     },

     {
        title:'Ratings',
        dataIndex:'ratings',
     },

     {
      title: "Action",
      render: (text, data) => {
      console.log(data)
        return (
          <div className="d-flex">
            <Button
              onClick={() => {
                setIsModalOpen(true);
                setSelectedMovie(data);
                setFormType("edit");
              }}
            >
              <EditOutlined />
            </Button>
            <Button onClick={() => handleDelete(data.id)}>
              <DeleteOutlined />
            </Button>
          </div>
        );
      },
    },
  ]

  return (
    <div>
      <div className="d-flex justify-content-end">
        <Button
          onClick={() => {
            setIsModalOpen(true);
            setSelectedMovie(null)
          }}
        >
          Add Movie
        </Button>
      </div>

      <Table dataSource={movies} columns={tableHeadings} />
      {isModalOpen && (
         <MovieForm
          isModalOpen={isModalOpen}
          setIsModalOpen={setIsModalOpen}
          formType={formType}
          selectedMovie={selectedMovie}
          setSelectedMovie={setSelectedMovie}
        />
      )}
    </div>
  );
}

export default MovieList;