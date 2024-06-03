import React, { useState } from 'react';
import './FormComponent.css';
const FormComponent = () => {
  const [formData, setFormData] = useState({
    field1: '',
    field2: '',
    field3: '',
    field4: '',
    field5: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data submitted:', formData);
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <div className="form-group">
        <label htmlFor="field1">Equation:</label>
        <input type="text" id="field1" name="field1" value={formData.field1} onChange={handleChange} />
      </div>
      <div className="form-group">
        <label htmlFor="field2">X min:</label>
        <input type="text" id="field2" name="field2" value={formData.field2} onChange={handleChange} />
      </div>
      <div className="form-group">
        <label htmlFor="field3">X max:</label>
        <input type="text" id="field3" name="field3" value={formData.field3} onChange={handleChange} />
      </div>
      <div className="form-group">
        <label htmlFor="field4">Y min:</label>
        <input type="text" id="field4" name="field4" value={formData.field4} onChange={handleChange} />
      </div>
      <div className="form-group">
        <label htmlFor="field5">X max:</label>
        <input type="text" id="field5" name="field5" value={formData.field5} onChange={handleChange} />
      </div>
      <button type="submit" className="submit-button">Submit</button>
    </form>
  );
};

export default FormComponent;
