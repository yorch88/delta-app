import React, { useEffect, useState } from 'react';

function ServiceRequestForm() {
  const [serviceTypes, setServiceTypes] = useState([]); // Holds the list of service types
  const [selectedServiceType, setSelectedServiceType] = useState(""); // Selected service type
  const [description, setDescription] = useState(""); // Description input
  const [status] = useState("A"); // Default status
  const [nickname, setNickname] = useState(""); // Nickname input
  const [email, setEmail] = useState(""); // Email input
  const [phoneNumber, setPhoneNumber] = useState(""); // Phone number input
  const [message, setMessage] = useState(""); // Success/error message

  // Fetch service types on component mount
  useEffect(() => {
    fetch("http://127.0.0.1:5000/servicetype/all/")
      .then((response) => response.json())
      .then((data) => {
        setServiceTypes(data);
        if (data.length > 0) {
          setSelectedServiceType(data[0].id); // Default to the first service type
        }
      })
      .catch((error) => {
        console.error("Error fetching service types:", error);
      });
  }, []);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    const requestData = {
      id_servicetype: selectedServiceType,
      description,
      status,
      nickname,
      email,
      phone_number: phoneNumber,
    };

    fetch("http://127.0.0.1:5000/servicerequest/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (response.ok) {
          setMessage("Service request created successfully!");
        } else {
          response.json().then((data) => {
            setMessage(data.error || "Failed to create service request.");
          });
        }
      })
      .catch((error) => {
        console.error("Error submitting service request:", error);
        setMessage("Error submitting service request.");
      });
  };

  return (
    <div>
      <h1>Create Service Request</h1>
      <form onSubmit={handleSubmit}>
        {/* Service Type Dropdown */}
        <label htmlFor="serviceType">Service Type:</label>
        <select
          id="serviceType"
          value={selectedServiceType}
          onChange={(e) => setSelectedServiceType(e.target.value)}
        >
          {serviceTypes.map((type) => (
            <option key={type.id} value={type.id}>
              {type.name}
            </option>
          ))}
        </select>
        <br />

        {/* Description Input */}
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="4"
          cols="50"
          required
        ></textarea>
        <br />

        {/* Nickname Input */}
        <label htmlFor="nickname">Nickname:</label>
        <input
          id="nickname"
          type="text"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          required
        />
        <br />

        {/* Email Input */}
        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br />

        {/* Phone Number Input */}
        <label htmlFor="phoneNumber">Phone Number:</label>
        <input
          id="phoneNumber"
          type="text"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />
        <br />

        {/* Submit Button */}
        <button type="submit">Submit</button>
      </form>

      {/* Success/Error Message */}
      {message && <p>{message}</p>}
    </div>
  );
}

export default ServiceRequestForm;
