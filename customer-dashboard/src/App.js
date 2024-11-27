import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
//import Slider from 'react-slider';
import axios from 'axios';
import './App.css';

function App() {
  const [customers, setCustomers] = useState([]);
  const [groupBy, setGroupBy] = useState('spending_class'); // Default grouping by cluster
  //const [eps, setEps] = useState(1.5); // Slider-controlled parameter
  const [hoveredPoint, setHoveredPoint] = useState(null); // Track hovered point
  const [focusedCustomer, setFocusedCustomer] = useState(null); // Customer to focus on
  const [manualControl, setManualControl] = useState(false); // Track if user manually interacted

  useEffect(() => {
    // Fetch customer data from the backend
    axios.get('http://127.0.0.1:5000/api/customers').then((response) => {
      setCustomers(response.data);
    });
  }, []);

  // Group data based on the selected grouping option
  const groupedData = customers.reduce((acc, customer) => {
    const groupKey = groupBy === 'cluster' ? customer.cluster : customer.spender_class;
    if (!acc[groupKey]) acc[groupKey] = { lat: [], lon: [], labels: [], points: [] };
    acc[groupKey].lat.push(customer.lat);
    acc[groupKey].lon.push(customer.lng);
    acc[groupKey].labels.push(`Customer ID: ${customer.id}`);
    acc[groupKey].points.push(customer);
    return acc;
  }, {});

  const traces = Object.entries(groupedData).map(([group, data]) => ({
    type: 'scattergeo',
    mode: 'markers',
    name: `Group: ${group}`,
    lat: data.lat,
    lon: data.lon,
    text: data.labels,
    marker: { size: 8 },
    customdata: data.points,
    hovertemplate: '<extra></extra>', // Prevent default hover box
  }));

  // Handle hover event
  const handleHover = (event) => {
    const point = event.points[0].customdata;
    setHoveredPoint(point);
  };

  // Handle click on a customer in the Top ROI list
  const handleFocusCustomer = (customer) => {
    setFocusedCustomer(customer);
  };

  // Handle manual map interactions
  const handleRelayout = () => {
    setManualControl(true); // Enable manual control on user interaction
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar for Summary Table */}
      <div className="sidebar">
        <h2>Summary Table</h2>
        <table border="1" style={{ width: '100%', textAlign: 'center' }}>
          <thead>
            <tr>
              <th>{groupBy === 'cluster' ? 'Cluster' : 'Spending Class'}</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(groupedData).map(([group, data]) => (
              <tr key={group}>
                <td>{group}</td>
                <td>{data.points.length}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        <h1>ELECTRA</h1>
        <h2>Electrification Leveling and Efficiency Cost-Targeting ROI Analyst</h2>

        <div className="controls">
          <div className="group-by">
            <h2>Group By</h2>
            <select value={groupBy} onChange={(e) => setGroupBy(e.target.value)}>
              <option value="cluster">Cluster</option>
              <option value="spending_class">Spending Class</option>
            </select>
          </div>
          <div className="sensitivity-slider">
          </div>
        </div>

        <Plot
          data={traces}
          layout={{
            title: `Customer Groups by ${groupBy === 'cluster' ? 'Cluster' : 'Identifier'}`,
            geo: {
              scope: 'usa',
              showland: true,
              landcolor: '#eafaf1',
              bgcolor: '#d4edda',
              lakecolor: '#c7e9f7',
              subunitcolor: '#6fcf97',
              countrycolor: '#6fcf97',
              ...(focusedCustomer && !manualControl && {
                center: {
                  lat: focusedCustomer.latitude,
                  lon: focusedCustomer.longitude,
                },
                projection: { scale: 7 }, // Zoom level
              }),
            },
            paper_bgcolor: '#f6fdfd',
            margin: { t: 40, b: 20, l: 20, r: 20 },
          }}
          style={{
            width: '100%',
            height: '60vh',
            borderRadius: '10px',
            boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
          }}
          onHover={handleHover} // Track hover events
          onRelayout={handleRelayout} // Track manual map interactions
        />
      </div>

      {/* Right Sidebar for Point Details */}
      <div className="details-sidebar">
        <h2>Customer Details</h2>
        {hoveredPoint ? (
          <div>
            <p><strong>Customer ID:</strong> {hoveredPoint.id}</p>
            <p><strong>State:</strong> {hoveredPoint.state}</p>
            <p><strong>Total Money Spent:</strong> ${hoveredPoint.total_money_spent.toFixed(2)}</p>
            <p><strong>ROI:</strong> {(hoveredPoint.predicted_roi * 100 - 100).toFixed(2)}%</p>
          </div>
        ) : (
          <p>Hover over a point to see details.</p>
        )}
      </div>

      {/* Bottom Right: Top ROI Customers */}
      <div className="top-roi">
        <h2>Top ROI Customers</h2>
        <ul>
          {customers
            .filter((customer) => customer.predicted_roi !== undefined)
            .sort((a, b) => b.predicted_roi - a.predicted_roi)
            .slice(0, 5)
            .map((customer) => (
              <li
                key={customer.id}
                onClick={() => {
                  handleFocusCustomer(customer)
                }} // Ensure the function is attached
              >
                Customer {customer.id} ({(customer.predicted_roi * 100 - 100).toFixed(2)}%)
              </li>
            ))}
        </ul>
      </div>

    </div>
  );
}

export default App;
