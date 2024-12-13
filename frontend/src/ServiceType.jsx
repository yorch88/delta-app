import React, { useState } from "react";
import axios from "axios";

function ServiceType() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  const [responseMessage, setResponseMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/servicetype/", formData);
      setResponseMessage(`Service Type created successfully: ${JSON.stringify(response.data)}`);
    } catch (error) {
      setResponseMessage(
        `Error: ${error.response?.data?.error || "Something went wrong"}`
      );
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <h1>Create Service Type</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            cols="50"
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default ServiceType;
