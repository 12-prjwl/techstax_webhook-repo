import React, { useState, useEffect } from "react";
import axios from "axios";
import "../WebhookEvents.css";

const WebhookEvents = () => {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "https://techstaxassignment.onrender.com/events",
          {
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          }
        );
        if (Array.isArray(response.data)) {
          setEvents(response.data);
        } else {
          console.error("Unexpected response format:", response.data);
          setError("Unexpected response format");
        }
      } catch (err) {
        console.error("Error fetching events:", err);
        setError("Failed to fetch data. Check the network request or server.");
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 15000);
    return () => clearInterval(intervalId);
  }, []);

  const parseCustomDate = (dateString) => {
    const cleanDateString = dateString.replace(/(\d+)(th|st|nd|rd)/, "$1"); // Remove ordinal suffix
    const [datePart, timePart] = cleanDateString.split(" - ");
    const [day, month, year] = datePart.split(" ");
    const months = {
      January: "01",
      February: "02",
      March: "03",
      April: "04",
      May: "05",
      June: "06",
      July: "07",
      August: "08",
      September: "09",
      October: "10",
      November: "11",
      December: "12",
    };
    const formattedDate = `${year}-${months[month]}-${day.padStart(2, "0")}T${
      timePart.split(" ")[0]
    }:00Z`;
    return new Date(formattedDate);
  };

  return (
    <div className="webhook-container">
      <h2 className="webhook-header">Webhook Events</h2>
      {error && <p className="webhook-error">{error}</p>}
      <ul className="webhook-list">
        {events.map((event, index) => (
          <li key={index} className="webhook-item">
            {event.action === "Push" &&
              `"${event.author}" pushed to "${
                event.to_branch
              }" on ${parseCustomDate(event.timestamp).toLocaleString()}`}
            {event.action === "Pull Request" &&
              `"${event.author}" submitted a pull request from "${
                event.from_branch
              }" to "${event.to_branch}" on ${parseCustomDate(
                event.timestamp
              ).toLocaleString()}`}
            {event.action === "Merge" &&
              `"${event.author}" merged branch "${event.from_branch}" to "${
                event.to_branch
              }" on ${parseCustomDate(event.timestamp).toLocaleString()}`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WebhookEvents;
