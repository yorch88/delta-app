import React, { useState } from "react";
import axios from "axios";

function Users() {
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    email: "",
    password_user: "",
    user_level: "",
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
      const response = await axios.post("http://127.0.0.1:5000/users/", formData);
      setResponseMessage(`User added successfully: ${JSON.stringify(response.data)}`);
    } catch (error) {
      setResponseMessage(
        `Error: ${error.response?.data?.error || "Something went wrong"}`
      );
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <h1>Create User</h1>
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
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password_user"
            value={formData.password_user}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>User Level:</label>
          <input
            type="text"
            name="user_level"
            value={formData.user_level}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default Users;
