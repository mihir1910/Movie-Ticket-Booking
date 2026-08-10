import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getSingleMovie } from "../calls/movieCalls";
import moment from "moment";
import {
  Card,
  Row,
  Col,
  Image,
  Typography,
  Rate,
  Tag,
  Button,
  Input,
  Divider
} from "antd";
import { getAllTheatresAndShows } from "../calls/showCalls";

const { Title } = Typography;

export default function SingleMovie() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [date, setDate] = useState(moment().format("YYYY-MM-DD"));
  const [theatres, setTheatres] = useState([]);
  const navigate = useNavigate();

  const handleDate = (e) => {
    setDate(moment(e.target.value).format("YYYY-MM-DD"));
    navigate(`/singleMovie/${id}?date=${e.target.value}`);
  };

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const res = await getSingleMovie(id);
        setMovie(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    if (id) fetchMovie();
  }, [id]);

  const getAllShowsWithTheatres = async () => {
    try {
      const res = await getAllTheatresAndShows({ movie: id, date });
      setTheatres(res.shows);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getAllShowsWithTheatres();
  }, [date]);

  return (
   <div style={{ padding: 16 }}>
       {movie && (
        <Card>
          <Row gutter={16}>
            <Col xs={24} sm={8}>
              <Image
                src={movie.posterPath}
                alt={movie.title}
                style={{ width: "100%", borderRadius: 6 }}
                fallback="/placeholder-poster.png"
              />
            </Col>

            <Col xs={24} sm={16}>
              <Title level={4} style={{ marginBottom: 8 }}>
                {movie.title}
              </Title>

              {/* Genre (only if present) */}
              {movie.genre && (
                <div style={{ marginBottom: 8 }}>
                  {(Array.isArray(movie.genre)
                    ? movie.genre
                    : movie.genre.toString().split(",")
                  ).map((g) => (
                    <Tag key={g} style={{ marginBottom: 4 }}>
                      {g.toString().trim()}
                    </Tag>
                  ))}
                </div>
              )}

              {/* Rating (only if present) */}
              {movie.ratings !== undefined && (
                <div style={{ marginBottom: 12 }}>
                  <Rate disabled value={Number(movie.ratings) || 0} />
                  <span style={{ marginLeft: 8 }}>{movie.ratings}</span>
                </div>
              )}

              {/* Description */}
              {movie.description && (
                <p style={{ whiteSpace: "pre-line", marginBottom: 12 }}>
                  {movie.description}
                </p>
              )}

              {/* Release date and language (only the fields you have) */}
              <div>
                {movie.releaseDate && (
                  <div>
                    <strong>Release Date: </strong>
                    {moment(movie.releaseDate).format("DD-MM-YYYY")}
                  </div>
                )}
                {movie.language && (
                  <div>
                    <strong>Language: </strong>
                    {movie.language}
                  </div>
                )}

                {/* Book Tickets Button */}
                <div style={{ marginTop: 16 }}>
                  <Button type="primary">Book Tickets</Button>
                </div>
                {/* Date Picker */}
                <div className="d-flex">
                  <label>Choose Date</label>
                  <Input onChange={handleDate} type="date" value={date} />
                </div>
              </div>
            </Col>
          </Row>
        </Card>
      )}
      {theatres.length > 0 && (
        <div className="theatre-wrapper mt-3 pt-3">
          <h2>Theatres</h2>
          {theatres.map((theatre) => {
            return (
              <div key={theatre._id}>
                <Row gutter={24} key={theatre._id}>
                  <Col xs={{ span: 24 }} lg={{ span: 8 }}>
                    <h3>{theatre.name}</h3>
                    <p>{theatre.address}</p>
                  </Col>
                  <Col xs={{ span: 24 }} lg={{ span: 16 }}>
                    <ul className="show-ul">
                      {theatre.shows
                        .sort(
                          (a, b) =>
                            moment(a.time, "HH:mm") - moment(b.time, "HH:mm")
                        )
                        .map((singleShow) => {
                          return (
                            <li
                         //     key={singleShow._id}
                              onClick={() =>
                                navigate(`/bookshow/${singleShow._id}`)                              }
                            >
                              {moment(singleShow.time, "HH:mm").format(
                                "hh:mm A"
                              )}
                            </li>
                          );
                        })}
                    </ul>
                  </Col>
                </Row>
                <Divider />
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}