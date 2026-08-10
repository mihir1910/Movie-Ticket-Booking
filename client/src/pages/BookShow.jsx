import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getTheShow } from "../calls/showCalls";

function BookShow() {
  const params = useParams();
  const [show, setShow] = useState();

  const getData = async () => {
    try {
      const res = await getTheShow({ showId: params.id });
      setShow(res.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getData();
  }, []);

  const getSeats = () => {
    let columns = 10;
    const totalSeats = show?.totalSeats;
    let rows = Math.ceil(totalSeats / columns);
  };

  return <div>
         {/* seating component */}
  </div>;
}


export default BookShow;